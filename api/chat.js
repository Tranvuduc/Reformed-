// api/chat.js — AI chat cho độc giả Reformed Vietnam.
// Vercel Serverless Function (Node, ES module). Cùng mẫu handler với api/tr.js:
//   export default async function handler(req, res) { ... }
//
// NGUYÊN TẮC $0 CỨNG (quyết định của David, 2026-11-15):
//  - Chỉ gọi free tier: Groq (chính) + Gemini (dự phòng), không cần thẻ.
//  - Hết free tier -> nhà cung cấp trả 429 -> function trả 429 + câu "hết lượt hôm nay".
//  - Không có billing, không có dịch vụ trả phí nào được gọi từ đây.
//  - Không log câu hỏi của người dùng ra bất cứ đâu. Không dùng Vercel Blob.
//  - API key CHỈ đọc từ process.env.GROQ_API_KEY / GEMINI_API_KEY (Vercel env var).
//    Chưa đặt key nào -> GET/POST đều trả 503 "not_ready", widget tự hiển thị
//    "tính năng đang được chuẩn bị".
//  - LÝ DO DÙNG GROQ (2026-11-15): Gemini free tier quá tải từ sáng 15/11
//    (5 timeout + 1×503 trong log Vercel, key vẫn tốt) nên câu tự do toàn
//    lỗi 500; David đưa key Groq để chat trả lời lại được. Groq là chính,
//    Gemini chỉ là dự phòng khi Groq lỗi HTTP; Groq timeout thì dừng luôn
//    (Gemini sáng nay cũng timeout nên thử tiếp chỉ làm người dùng chờ lâu hơn).
//
// Luồng xử lý (không tốn token LLM khi trả được từ dữ liệu có sẵn):
//   1. Rate limit theo IP (bộ nhớ trong — xem ghi chú ở checkRateLimit).
//   2. Tìm sách theo tiêu đề/tác giả (data/books-lookup.json, 3.323 cuốn).
//   3. Khớp 95 câu Hỏi Đáp (data/answers-lookup.json) -> trả thẳng đáp án + link.
//   4. Gọi Groq openai/gpt-oss-120b (chính, dự phòng 20b cùng nhà),
//      Gemini gemini-flash-latest (dự phòng) với system prompt khóa lập
//      trường Cải Chánh + ngữ cảnh từ trang (sách khớp, Hỏi Đáp khớp,
//      các mục chính) để trả lời có link thật thay vì chung chung.
//   5. Kiểm chứng mọi trích dẫn Kinh Thánh trong câu trả lời đối chiếu
//      dữ liệu 1934 (data/bible-refs.json, 66 sách / 1.189 chương / 31.102 câu).
//      Trích dẫn không tồn tại -> gỡ khỏi câu trả lời, ghi chú rõ.
//
// Chỉ lấy tiêu đề/tác giả sách + tóm tắt Hỏi Đáp làm ngữ cảnh cho LLM —
// KHÔNG đọc nội dung sách (dự án RAG đầy đủ là việc riêng, theo PLAN.md).
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

// ---------------------------------------------------------------- cấu hình
// LƯU Ý MODEL (2026-11-15, đã kiểm chứng live bằng key thật của David):
// model Flash có version cố định trước đây trả HTTP 404 "no longer available
// to new users" trên generateContent dù vẫn còn trong danh sách models. Dùng
// alias "gemini-flash-latest" (dòng Flash mới nhất, có trong danh sách models
// live). Nếu alias này cũng bị đổi trong tương lai, chỉ cần sửa 1 dòng MODEL này.
const MODEL = 'gemini-flash-latest';
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
// Groq (chính từ 2026-11-15): API tương thích OpenAI, model trả lời
// nhanh trên free tier. LƯU Ý MODEL (2026-11-15, đã kiểm chứng bằng log
// Vercel + docs Groq): 'llama-3.3-70b-versatile' ĐÃ BỊ GROQ NGỪNG cho
// free/developer từ 16/08/2026 (chỉ còn Enterprise) nên mọi lần gọi đều
// trả HTTP 404 model_not_found — key vẫn tốt (không 401/403), code đã
// live, chỉ sai tên model. Groq chỉ định thay thế là openai/gpt-oss-120b
// (chính) và openai/gpt-oss-20b (dự phòng cùng nhà); cả hai đều là
// Production trên free/developer. Vì tên model có thể bị ngừng tiếp,
// askGroq thử lần lượt cả hai model trước khi báo lỗi.
const GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions';
const GROQ_MODELS = ['openai/gpt-oss-120b', 'openai/gpt-oss-20b'];
const GROQ_TIMEOUT_MS = 8000;
const MAX_Q_LEN = 500;          // tối đa 500 ký tự / câu hỏi
const HISTORY_TURNS = 2;        // giữ tối đa 2 lượt trao đổi gần nhất
const RATE_PER_HOUR = 10;       // mỗi IP: tối đa 10 tin / giờ
const RATE_PER_DAY = 50;        // mỗi IP: tối đa 50 tin / ngày
const GEMINI_TIMEOUT_MS = 25000;
const MAX_OUTPUT_TOKENS = 1000;

const MSG_QUOTA = 'Hôm nay đã hết lượt trả lời miễn phí, mời bạn quay lại sau 0:00 giờ.';
const MSG_TOO_FAST = 'Bạn hỏi hơi nhanh, mời thử lại sau ít phút nhé.';
const MSG_NOT_READY = 'Tính năng chat AI đang được chuẩn bị, mời bạn quay lại sau.';
const MSG_ERROR = 'Có lỗi xảy ra, mời thử lại sau.';

const SYSTEM_PROMPT = [
  'Bạn là trợ lý AI của Thư viện Reformed Vietnam (reformedvietnam.com) — thư viện thần học Cải Chánh tiếng Việt.',
  'Chỉ trả lời theo thần học Cải Chánh (Tín điều Westminster / Tín điều 1689).',
  'Trả lời bằng tiếng Việt, ngắn gọn (tối đa khoảng 250 từ), giọng ấm áp, rõ ràng.',
  'Khi trích Kinh Thánh, chỉ dùng Bản dịch 1934 và ghi đúng dạng "Sách chương:câu" (ví dụ: Giăng 3:16, Rô-ma 8:28); chỉ trích những câu bạn thật sự chắc chắn, nếu không chắc thì nói "tôi không chắc về câu này" thay vì đoán. Không bịa trích dẫn.',
  'Khi nhắc tới một cuốn sách, chỉ nhắc sách có trong thư viện và ghi rõ tên sách + tác giả.',
  'Thuật ngữ bắt buộc: dùng "Đức Chúa Trời" (không dùng "Thiên Chúa"), "sự công chính" (không dùng "công bình" ngoài trích dẫn 1934 nguyên văn), "Chúa Giê-xu" (không dùng "Chúa Giê-su"), "Vương quốc Đức Chúa Trời", "Phúc Âm". Trích dẫn Kinh Thánh phải khớp nội dung câu đó — không gắn một câu Kinh Thánh vào một ý mà câu đó không nói.',
  'Khi mục TÀI LIỆU TRÊN TRANG liệt kê sách phù hợp, hãy nêu 1–3 cuốn (tên sách + tác giả + link đầy đủ) trong câu trả lời; khi có câu Hỏi Đáp phù hợp, dẫn link của nó.',
  'Không dùng dấu ** trong câu trả lời (không in đậm bằng markdown).',
  'Khi câu trả lời kèm mục TÀI LIỆU TRÊN TRANG, hãy dựa vào đó: giới thiệu đúng sách/câu trả lời có sẵn và ghi link đầy đủ dạng https://reformedvietnam.com/... Chỉ dùng link có trong tài liệu đó, tuyệt đối không bịa URL hay đoán slug. Nếu tài liệu không có gì liên quan, trả lời theo thần học Cải Chánh rồi gợi ý mục phù hợp của trang.',
  'Nếu câu hỏi là tư vấn mục vụ cá nhân, khủng hoảng, hôn nhân, y tế hay pháp lý, hãy từ chối lịch sự và khuyên gặp mục sư hoặc người có chuyên môn.',
  'Không bao giờ xưng mình là mục sư, không bao giờ nói câu trả lời đã được duyệt.',
  'Không trả lời về chính trị hay các chủ đề ngoài Kinh Thánh / thần học / sách.',
].join(' ');

// ---------------------------------------------------------------- tiện ích
function json(res, status, obj) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  return res.status(status).json(obj);
}

// Chuẩn hoá tiếng Việt để so khớp không dấu: bỏ dấu, đ->d, thường hoá.
function norm(s) {
  return String(s || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/đ/g, 'd')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

const STOPWORDS = new Set([
  'la', 'gi', 'cua', 'va', 'co', 'khong', 'the', 'nao', 'sao', 'ra', 've',
  'cho', 'voi', 'thi', 'ma', 'thi', 'neu', 'khi', 'de', 'duoc', 'mot', 'cac',
  'nhung', 'này', 'nay', 'do', 'day', 'kia', 'ay', 'xin', 'hoi', 'cho', 'toi',
  'muon', 'biet', 'tim', 'sach', 'cuon', 'quyen', 'vay', 'chinh', 'hay',
]);
function tokens(s) {
  return norm(s).split(' ').filter((t) => t.length > 2 && !STOPWORDS.has(t));
}

// Đọc JSON kèm theo function (lazy + cache trong bộ nhớ của instance).
const _cache = {};
function loadData(name) {
  if (!_cache[name]) {
    _cache[name] = JSON.parse(
      readFileSync(new URL(`./data/${name}`, import.meta.url), 'utf-8'),
    );
  }
  return _cache[name];
}

// ---------------------------------------------------------------- rate limit
// GHI CHÚ TRUNG THỰC: Vercel serverless có thể chạy nhiều instance song song,
// mỗi instance có bộ nhớ riêng, nên giới hạn này chỉ là "phanh" chống spam
// trong từng instance — không phải giới hạn toàn cục tuyệt đối. Lớp bảo vệ
// $0 thật sự là quota free tier của chính Groq/Gemini (429 -> tạm nghỉ).
const _hits = new Map(); // hashIP -> [timestampMs, ...]
const _salt = Math.random().toString(36).slice(2);
function clientIp(req) {
  const fwd = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  const real = String(req.headers['x-real-ip'] || '').trim();
  return fwd || real || 'unknown';
}
function ipHash(ip) {
  return createHash('sha256').update(_salt + '|' + ip).digest('hex').slice(0, 16);
}
function checkRateLimit(req) {
  const now = Date.now();
  const h = ipHash(clientIp(req));
  let arr = _hits.get(h) || [];
  arr = arr.filter((t) => now - t < 24 * 3600 * 1000); // chỉ giữ 24h gần nhất
  const lastHour = arr.filter((t) => now - t < 3600 * 1000).length;
  if (lastHour >= RATE_PER_HOUR || arr.length >= RATE_PER_DAY) {
    _hits.set(h, arr);
    return false;
  }
  arr.push(now);
  _hits.set(h, arr);
  if (_hits.size > 5000) { // chống phình bộ nhớ: xoá mục cũ nhất
    const first = _hits.keys().next().value;
    _hits.delete(first);
  }
  return true;
}

// ---------------------------------------------------------------- lớp 1: 95 câu Hỏi Đáp
// IDF theo 95 câu Hỏi Đáp: từ càng hiếm càng nặng. "Kinh", "Thánh", "trong"
// xuất hiện trong hàng chục câu nên gần như không có giá trị phân biệt;
// "tiền định", "khủng long" hiếm nên quyết định. Nhờ vậy câu hỏi ngắn
// 2-3 từ chung chung không khớp bừa vào một câu Hỏi Đáp dài.
let _idf = null;
function idfMap() {
  if (_idf) return _idf;
  const entries = loadData('answers-lookup.json');
  const df = new Map();
  for (const e of entries) {
    for (const t of new Set(tokens(e.q))) df.set(t, (df.get(t) || 0) + 1);
  }
  _idf = new Map();
  for (const [t, n] of df) _idf.set(t, Math.log(1 + entries.length / (1 + n)));
  return _idf;
}
function scoreAnswers(question) {
  const qNorm = norm(question);
  const qToks = tokens(question);
  if (qToks.length === 0) return [];
  const idf = idfMap();
  const qWeight = qToks.reduce((s, t) => s + (idf.get(t) ?? 4.5), 0); // từ chưa từng thấy = rất hiếm
  const qSet = new Set(qToks);
  const scored = [];
  for (const e of loadData('answers-lookup.json')) {
    const eNorm = norm(e.q);
    // Khớp gần như nguyên câu -> nhận ngay.
    if (qNorm.length > 12 && (eNorm.includes(qNorm) || qNorm.includes(eNorm))) {
      return [{ entry: e, score: 1 }];
    }
    const eToks = tokens(e.q);
    if (eToks.length === 0) continue;
    let hit = 0;
    let hitWeight = 0;
    for (const t of new Set(eToks)) {
      if (qSet.has(t)) { hit += 1; hitWeight += idf.get(t) ?? 4.5; }
    }
    // Điểm = tỉ trọng IDF của các từ khớp được / tổng trọng IDF của câu hỏi.
    const score = qWeight > 0 ? hitWeight / qWeight : 0;
    if (hit >= 2) scored.push({ entry: e, score });
  }
  scored.sort((x, y) => y.score - x.score);
  return scored;
}
function matchAnswers(question) {
  const scored = scoreAnswers(question);
  if (scored.length > 0 && scored[0].score >= 0.5) return scored[0];
  return null;
}

// ---------------------------------------------------------------- lớp 2: tìm sách theo tiêu đề
const BOOK_INTENT = /\b(sach|tim sach|tim cuon|gioi thieu sach|co sach nao)\b/;
// Từ không mang nghĩa phân biệt khi tìm sách.
const BOOK_KEY_EXCLUDE = ['sach', 'cuon', 'quyen', 'nao', 'tim', 'gioi', 'thieu', 'viet', 'noi', 've', 'cua', 'doc', 'hay', 'tot'];
function scoreBooks(question) {
  const keys = tokens(question).filter((t) => !BOOK_KEY_EXCLUDE.includes(t));
  if (keys.length === 0) return [];
  const scored = [];
  for (const b of loadData('books-lookup.json')) {
    const titleToks = new Set(tokens(b.t));
    const authorToks = new Set(tokens(b.a));
    let hit = 0;
    for (const k of keys) {
      if (titleToks.has(k)) hit += 2;       // khớp tiêu đề nặng hơn
      else if (authorToks.has(k)) hit += 1; // khớp tác giả
    }
    if (hit > 0) scored.push({ b, hit });
  }
  scored.sort((x, y) => y.hit - x.hit);
  return scored;
}
function matchBooks(question) {
  const qNorm = norm(question);
  if (!BOOK_INTENT.test(qNorm)) return null;
  const top = scoreBooks(question).slice(0, 3);
  // Cần ít nhất 1 từ khoá khớp tiêu đề (hit >= 2) để trả về.
  if (top.length === 0 || top[0].hit < 2) return null;
  return top.map((x) => x.b);
}

// ---------------------------------------------------------------- ngữ cảnh cho LLM: sách + Hỏi Đáp + mục của trang
// Duc 2026-11-15: "AI trả lời chung chung, không đọc được trang, không đưa
// link". Nguyên nhân: LLM chỉ nhận system prompt + lịch sử, không hề biết
// thư viện có sách gì. Hàm này đưa vào prompt: sách khớp từ khoá (chỉ tiêu
// đề/tác giả + link — KHÔNG đọc nội dung sách), Hỏi Đáp khớp (tóm tắt +
// link), và các mục chính của trang (đường dẫn đã kiểm có thật trong repo).
// Prompt thêm ~200-300 token/lần gọi tự do, vẫn $0 (free tier Groq/Gemini).
const SITE_SECTIONS = [
  ['Thư viện sách', 'https://reformedvietnam.com/thu-vien.html'],
  ['Kinh Thánh 1934 — đọc và tra cứu', 'https://reformedvietnam.com/kinh-thanh/'],
  ['Giáo lý Westminster (107 câu)', 'https://reformedvietnam.com/giao-ly/'],
  ['Bách khoa thần học', 'https://reformedvietnam.com/bach-khoa/'],
  ['Hỏi đáp', 'https://reformedvietnam.com/hoi-dap/'],
  ['Học viện (Thirdmill)', 'https://reformedvietnam.com/hoc-vien/'],
  ['Bài giảng', 'https://reformedvietnam.com/bai-giang/'],
  ['Thánh ca', 'https://reformedvietnam.com/thanh-ca/'],
  ['Tóm tắt sách', 'https://reformedvietnam.com/tom-tat-sach/'],
  ['Sách nói', 'https://reformedvietnam.com/sach-noi.html'],
  ['Suy ngẫm hằng ngày', 'https://reformedvietnam.com/suy-ngam/'],
];
function buildSiteContext(question) {
  const lines = ['TÀI LIỆU TRÊN TRANG reformedvietnam.com — chỉ dùng những mục dưới đây, tuyệt đối không bịa link hay đoán slug:'];
  // Ưu tiên sách có CỤM 2 từ khớp với câu hỏi ("cầu nguyện") trước sách chỉ
  // khớp từng từ rời ("câu hỏi" + "nguyên nhân" — bỏ dấu xong đều thành
  // "cau"/"nguyen" nên khớp rời rất dễ nhiễu). Không có sách nào khớp cụm
  // thì dùng lại danh sách khớp rời.
  const qKeys = tokens(question).filter((t) => !BOOK_KEY_EXCLUDE.includes(t));
  const qBigrams = new Set();
  for (let i = 0; i + 1 < qKeys.length; i++) qBigrams.add(`${qKeys[i]} ${qKeys[i + 1]}`);
  const scored = scoreBooks(question).filter((x) => x.hit >= 4);
  const withPhrase = scored.filter((x) => {
    const tToks = tokens(x.b.t);
    for (let i = 0; i + 1 < tToks.length; i++) {
      if (qBigrams.has(`${tToks[i]} ${tToks[i + 1]}`)) return true;
    }
    return false;
  });
  const books = (withPhrase.length > 0 ? withPhrase : scored).slice(0, 4);
  if (books.length > 0) {
    lines.push('Sách trong thư viện khớp với câu hỏi:');
    for (const { b } of books) {
      lines.push(`- ${b.t} — ${b.a} — https://reformedvietnam.com/ban-dich/${b.s}.html`);
    }
  }
  const qas = scoreAnswers(question).filter((x) => x.score >= 0.3).slice(0, 3);
  if (qas.length > 0) {
    lines.push('Câu hỏi-đáp đã có trên trang:');
    for (const { entry } of qas) {
      const excerpt = String(entry.a || '').replace(/\s+/g, ' ').slice(0, 120);
      lines.push(`- ${entry.q} — https://reformedvietnam.com/hoi-dap/${entry.s}.html (tóm tắt: ${excerpt}…)`);
    }
  }
  lines.push('Các mục chính của trang:');
  for (const [label, url] of SITE_SECTIONS) lines.push(`- ${label}: ${url}`);
  return lines.join('\n');
}

// ---------------------------------------------------------------- lớp 3: kiểm chứng trích dẫn Kinh Thánh 1934
// _refIndex: tên chuẩn hoá không dấu -> sách. Regex bắt tên sách DẠNG GỐC
// (có dấu, như model viết ra) + biến thể hay gặp; tra cứu thì chuẩn hoá
// không dấu nên "Rô-ma", "Rôma", "Rô ma" đều khớp cùng một sách.
let _refIndex = null; // normName -> { name, v:[...] }
function refIndex() {
  if (_refIndex) return _refIndex;
  _refIndex = new Map();
  for (const b of loadData('bible-refs.json')) {
    _refIndex.set(norm(b.name), b);
  }
  // Biến thể tên sách cũng tra được về sách chuẩn.
  for (const [canon, variants] of Object.entries(NAME_VARIANTS)) {
    const book = _refIndex.get(norm(canon));
    if (book) for (const v of variants) _refIndex.set(norm(v), book);
  }
  return _refIndex;
}
// Biến thể tên sách hay gặp (dạng gốc có dấu) -> tên chuẩn trong bible-refs.
const NAME_VARIANTS = {
  'Thi Thiên': ['Thánh Thi'],
  'Cô-rinh-tô': ['Côrintô'],
  'Tê-sa-lô-ni-ca': ['Têsalônica'],
  'Phi-líp': ['Philíp'],
  'Ê-phê-sô': ['Êphêsô'],
  'Hê-bơ-rơ': ['Hêbơrơ'],
};
function refRegex() {
  const seen = new Set();
  const forms = [];
  const add = (s) => {
    const k = s.toLowerCase();
    if (!seen.has(k)) { seen.add(k); forms.push(s); }
  };
  for (const b of loadData('bible-refs.json')) {
    const name = b.name;
    add(name);                                  // "Rô-ma"
    add(name.replace(/-/g, ''));                // "Rôma"
    add(name.replace(/-/g, ' '));               // "Rô ma"
    // Số La Mã: "I Giăng" cũng là "1 Giăng".
    const m = name.match(/^([123])\s+(.*)$/);
    if (m) add(['I', 'II', 'III'][Number(m[1]) - 1] + ' ' + m[2]);
    for (const v of NAME_VARIANTS[name] || []) add(v);
  }
  forms.sort((a, b) => b.length - a.length); // tên dài trước ("1 Giăng" trước "Giăng")
  const alt = forms.map((n) => n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  // Sách chương:câu, câu có thể là khoảng (16-17) hoặc qua chương (8:28-9:1).
  return new RegExp(
    `\\b(${alt})\\s+(\\d+)(?:\\s*:\\s*(\\d+)(?:\\s*[–-]\\s*(?:(\\d+)\\s*:\\s*)?(\\d+))?)?`,
    'gi',
  );
}
function verifyCitations(answer) {
  const idx = refIndex();
  const re = refRegex();
  let removed = 0;
  const cleaned = answer.replace(re, (match, bookRaw, chStr, vStr, endChStr, endVStr) => {
    // Số La Mã đầu tên sách -> số Ả Rập ("I Giăng" -> "1 Giăng").
    let key = norm(bookRaw).replace(/^(iii|ii|i) /, (mm) => ({ i: '1 ', ii: '2 ', iii: '3 ' })[mm.trim()] || mm);
    const book = idx.get(key);
    if (!book) { removed += 1; return ''; }
    const ch = parseInt(chStr, 10);
    if (ch < 1 || ch > book.v.length) { removed += 1; return ''; }
    if (vStr !== undefined) {
      const v = parseInt(vStr, 10);
      if (v < 1 || v > book.v[ch - 1]) { removed += 1; return ''; }
      if (endVStr !== undefined) {
        const endV = parseInt(endVStr, 10);
        const endCh = endChStr !== undefined ? parseInt(endChStr, 10) : ch;
        if (endCh < 1 || endCh > book.v.length || endV < 1 || endV > book.v[endCh - 1]) {
          removed += 1; return '';
        }
      }
    }
    return match; // tồn tại thật -> giữ nguyên
  });
  return { text: cleaned.replace(/[ \t]{2,}/g, ' ').trim(), removed };
}

// ---------------------------------------------------------------- lớp 4: gọi Gemini
async function askGemini(question, history, context) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) return { status: 'no_key' };
  const sysText = context ? `${SYSTEM_PROMPT}\n\n${context}` : SYSTEM_PROMPT;
  const contents = [];
  for (const h of history || []) {
    if (typeof h.q === 'string' && h.q.trim()) {
      contents.push({ role: 'user', parts: [{ text: h.q.slice(0, MAX_Q_LEN) }] });
    }
    if (typeof h.a === 'string' && h.a.trim()) {
      contents.push({ role: 'model', parts: [{ text: h.a.slice(0, 1500) }] });
    }
  }
  contents.push({ role: 'user', parts: [{ text: question }] });
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), GEMINI_TIMEOUT_MS);
  try {
    const r = await fetch(GEMINI_URL, {
      method: 'POST',
      signal: ctrl.signal,
      headers: {
        'Content-Type': 'application/json',
        'x-goog-api-key': key,
      },
      body: JSON.stringify({
        system_instruction: { parts: [{ text: sysText }] },
        contents,
        generationConfig: { temperature: 0.3, maxOutputTokens: MAX_OUTPUT_TOKENS },
      }),
    });
    if (r.status === 429) return { status: 'quota' };
    if (!r.ok) {
      // Không lộ nội dung lỗi của Google ra ngoài (có thể chứa chi tiết nội bộ).
      console.error('[rv-chat] gemini http', r.status);
      return { status: 'error' };
    }
    const data = await r.json();
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const text = parts.map((p) => p.text || '').join('').trim();
    if (!text) return { status: 'error' };
    return { status: 'ok', text };
  } catch (e) {
    if (e && e.name === 'AbortError') {
      console.error('[rv-chat] gemini timeout');
      return { status: 'error', timeout: true };
    }
    console.error('[rv-chat] gemini fetch failed:', e && e.message ? String(e.message).slice(0, 120) : 'unknown');
    return { status: 'error' };
  } finally {
    clearTimeout(timer);
  }
}

// ---------------------------------------------------------------- lớp 4b: gọi Groq (chính)
// API tương thích OpenAI: POST /openai/v1/chat/completions, header
// Authorization: Bearer <key>. Trả về { status, text } giống askGemini,
// thêm cờ timeout:true khi bị abort để handler biết mà dừng, đừng thử tiếp.
// Thử lần lượt GROQ_MODELS: model nào lỗi HTTP (404 model bị ngừng, 5xx...)
// thì thử model tiếp theo; hết quota (429) thì báo quota; timeout thì dừng.
async function askGroq(question, history, context) {
  const key = process.env.GROQ_API_KEY;
  if (!key) return { status: 'no_key' };
  const sysText = context ? `${SYSTEM_PROMPT}\n\n${context}` : SYSTEM_PROMPT;
  const messages = [{ role: 'system', content: sysText }];
  for (const h of history || []) {
    if (typeof h.q === 'string' && h.q.trim()) {
      messages.push({ role: 'user', content: h.q.slice(0, MAX_Q_LEN) });
    }
    if (typeof h.a === 'string' && h.a.trim()) {
      messages.push({ role: 'assistant', content: h.a.slice(0, 1500) });
    }
  }
  messages.push({ role: 'user', content: question });
  for (const model of GROQ_MODELS) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), GROQ_TIMEOUT_MS);
    try {
      const r = await fetch(GROQ_URL, {
        method: 'POST',
        signal: ctrl.signal,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${key}`,
        },
        body: JSON.stringify({
          model,
          messages,
          temperature: 0.3,
          max_tokens: MAX_OUTPUT_TOKENS,
        }),
      });
      if (r.status === 429) return { status: 'quota' };
      if (!r.ok) {
        // Không lộ nội dung lỗi của Groq ra ngoài (có thể chứa chi tiết nội bộ).
        console.error('[rv-chat] groq http', r.status, model);
        continue; // thử model tiếp theo
      }
      const data = await r.json();
      const text = String(data?.choices?.[0]?.message?.content || '').trim();
      if (!text) continue; // trả rỗng: thử model tiếp theo
      return { status: 'ok', text };
    } catch (e) {
      if (e && e.name === 'AbortError') {
        console.error('[rv-chat] groq timeout', model);
        return { status: 'error', timeout: true };
      }
      console.error('[rv-chat] groq fetch failed:', e && e.message ? String(e.message).slice(0, 120) : 'unknown');
      return { status: 'error' }; // lỗi mạng: cùng endpoint, thử tiếp cũng vậy
    } finally {
      clearTimeout(timer);
    }
  }
  return { status: 'error' };
}

// ---------------------------------------------------------------- handler (mẫu như api/tr.js)
async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let s = '';
  for await (const c of req) {
    s += c;
    if (s.length > 20000) throw new Error('big');
  }
  return s ? JSON.parse(s) : {};
}

export default async function handler(req, res) {
  try {
    // Preflight: widget dùng để biết function đã deploy + đã có key chưa.
    if (req.method === 'GET') {
      return json(res, 200, { ok: 1, ready: Boolean(process.env.GROQ_API_KEY || process.env.GEMINI_API_KEY) });
    }
    if (req.method !== 'POST') return res.status(405).end();

    const b = await readBody(req);
    const question = String(b.question || '').trim();
    if (!question || question.length > MAX_Q_LEN) {
      return json(res, 400, { error: 'bad', message: 'Câu hỏi phải từ 1 đến 500 ký tự.' });
    }
    const history = Array.isArray(b.history) ? b.history.slice(-HISTORY_TURNS) : [];

    if (!checkRateLimit(req)) {
      return json(res, 429, { error: 'rate_limited', message: MSG_TOO_FAST });
    }

    // Lớp 1: tìm sách theo tiêu đề/tác giả (ưu tiên trước Hỏi Đáp: câu hỏi
    // "có sách nào về X?" là ý định tìm sách, không phải hỏi khái niệm).
    const books = matchBooks(question);
    if (books) {
      const lines = books.map(
        (bk) => `• ${bk.t} — ${bk.a}`,
      );
      return json(res, 200, {
        answer: `Mình tìm thấy ${books.length} cuốn trong thư viện khớp với câu hỏi của bạn:\n${lines.join('\n')}\nBấm vào từng cuốn bên dưới để mở trang sách.`,
        source: 'books',
        books: books.map((bk) => ({
          title: bk.t, author: bk.a, url: `/ban-dich/${bk.s}.html`,
        })),
        removed_citations: 0,
      });
    }

    // Lớp 2: 95 câu Hỏi Đáp có sẵn (không tốn token LLM).
    const qa = matchAnswers(question);
    if (qa) {
      return json(res, 200, {
        answer: qa.entry.a,
        source: 'hoi-dap',
        link: `/hoi-dap/${qa.entry.s}.html`,
        link_label: 'Đọc câu trả lời đầy đủ',
        removed_citations: 0,
      });
    }

    // Lớp 3: chưa có key nào -> báo "đang chuẩn bị" (widget tự xử lý).
    if (!process.env.GROQ_API_KEY && !process.env.GEMINI_API_KEY) {
      return json(res, 503, { error: 'not_ready', message: MSG_NOT_READY });
    }

    // Lớp 4: gọi LLM — Groq trước (chính), Gemini dự phòng. Chỉ thử tiếp
    // khi lỗi là HTTP (401/5xx...); timeout thì dừng luôn vì nhà cung cấp
    // còn lại sáng nay cũng timeout, thử tiếp chỉ làm người dùng chờ lâu hơn.
    // Hết quota (429) ở nhà này thì thử nhà kia, cả hai hết mới báo hết lượt.
    // Kèm ngữ cảnh từ trang (sách + Hỏi Đáp + mục chính) để LLM trả lời có
    // link thật thay vì trả lời chung chung.
    const siteContext = buildSiteContext(question);
    const providers = [];
    if (process.env.GROQ_API_KEY) providers.push({ name: 'groq', fn: askGroq });
    if (process.env.GEMINI_API_KEY) providers.push({ name: 'gemini', fn: askGemini });
    let ai = null;
    let sawQuota = false;
    for (const p of providers) {
      const r = await p.fn(question, history, siteContext);
      if (r.status === 'ok') { ai = { text: r.text, source: p.name }; break; }
      if (r.status === 'quota') { sawQuota = true; continue; }
      if (r.timeout) break; // timeout: dừng, đừng thử tiếp
      // Lỗi HTTP khác: thử nhà cung cấp tiếp theo (nếu có).
    }
    if (!ai && sawQuota) {
      return json(res, 429, { error: 'quota', message: MSG_QUOTA });
    }
    if (!ai) {
      return json(res, 500, { error: 'error', message: MSG_ERROR });
    }

    // Lớp 5: kiểm chứng trích dẫn Kinh Thánh rồi mới trả về.
    const v = verifyCitations(ai.text);
    let answer = v.text;
    if (v.removed > 0) {
      answer += `\n\n— Đã gỡ ${v.removed} trích dẫn Kinh Thánh chưa kiểm chứng được.`;
    }
    return json(res, 200, {
      answer,
      source: ai.source,
      removed_citations: v.removed,
    });
  } catch (e) {
    // Không bao giờ lộ stack trace / chi tiết lỗi ra ngoài.
    console.error('[rv-chat] handler error:', e && e.message ? String(e.message).slice(0, 120) : 'unknown');
    return json(res, 500, { error: 'error', message: MSG_ERROR });
  }
}
