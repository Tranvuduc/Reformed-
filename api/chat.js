// api/chat.js — AI chat cho độc giả Reformed Vietnam.
// Vercel Serverless Function (Node, ES module). Cùng mẫu handler với api/tr.js:
//   export default async function handler(req, res) { ... }
//
// NGUYÊN TẮC $0 CỨNG (quyết định của David, 2026-11-15):
//  - Chỉ gọi Gemini free tier (Google AI Studio, không cần thẻ).
//  - Hết free tier -> Gemini trả 429 -> function trả 429 + câu "hết lượt hôm nay".
//  - Không có billing, không có dịch vụ trả phí nào được gọi từ đây.
//  - Không log câu hỏi của người dùng ra bất cứ đâu. Không dùng Vercel Blob.
//  - API key CHỈ đọc từ process.env.GEMINI_API_KEY (Vercel env var).
//    Chưa đặt key -> GET/POST đều trả 503 "not_ready", widget tự hiển thị
//    "tính năng đang được chuẩn bị".
//
// Luồng xử lý (không tốn token LLM khi trả được từ dữ liệu có sẵn):
//   1. Rate limit theo IP (bộ nhớ trong — xem ghi chú ở checkRateLimit).
//   2. Tìm sách theo tiêu đề/tác giả (data/books-lookup.json, 3.323 cuốn).
//   3. Khớp 95 câu Hỏi Đáp (data/answers-lookup.json) -> trả thẳng đáp án + link.
//   4. Gọi Gemini 2.5 Flash với system prompt khóa lập trường Cải Chánh.
//   5. Kiểm chứng mọi trích dẫn Kinh Thánh trong câu trả lời đối chiếu
//      dữ liệu 1934 (data/bible-refs.json, 66 sách / 1.189 chương / 31.102 câu).
//      Trích dẫn không tồn tại -> gỡ khỏi câu trả lời, ghi chú rõ.
//
// KHÔNG có RAG đọc nội dung sách trong bản này (dự án riêng, theo PLAN.md).
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
const MAX_Q_LEN = 500;          // tối đa 500 ký tự / câu hỏi
const HISTORY_TURNS = 2;        // giữ tối đa 2 lượt trao đổi gần nhất
const RATE_PER_HOUR = 10;       // mỗi IP: tối đa 10 tin / giờ
const RATE_PER_DAY = 50;        // mỗi IP: tối đa 50 tin / ngày
const GEMINI_TIMEOUT_MS = 25000;
const MAX_OUTPUT_TOKENS = 700;

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
// $0 thật sự là quota free tier của chính Gemini (429 -> tạm nghỉ).
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
function matchAnswers(question) {
  const qNorm = norm(question);
  const qToks = tokens(question);
  if (qToks.length === 0) return null;
  const idf = idfMap();
  const qWeight = qToks.reduce((s, t) => s + (idf.get(t) ?? 4.5), 0); // từ chưa từng thấy = rất hiếm
  const qSet = new Set(qToks);
  let best = null;
  let bestScore = 0;
  for (const e of loadData('answers-lookup.json')) {
    const eNorm = norm(e.q);
    // Khớp gần như nguyên câu -> nhận ngay.
    if (qNorm.length > 12 && (eNorm.includes(qNorm) || qNorm.includes(eNorm))) {
      return { entry: e, score: 1 };
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
    if (hit >= 2 && score > bestScore) { bestScore = score; best = e; }
  }
  if (best && bestScore >= 0.5) return { entry: best, score: bestScore };
  return null;
}

// ---------------------------------------------------------------- lớp 2: tìm sách theo tiêu đề
const BOOK_INTENT = /\b(sach|tim sach|tim cuon|gioi thieu sach|co sach nao)\b/;
function matchBooks(question) {
  const qNorm = norm(question);
  if (!BOOK_INTENT.test(qNorm)) return null;
  const keys = tokens(question).filter((t) => !['sach', 'cuon', 'quyen', 'nao', 'tim', 'gioi', 'thieu', 'viet', 'noi', 've', 'cua', 'doc', 'hay', 'tot'].includes(t));
  if (keys.length === 0) return null;
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
  const top = scored.slice(0, 3);
  // Cần ít nhất 1 từ khoá khớp tiêu đề (hit >= 2) để trả về.
  if (top.length === 0 || top[0].hit < 2) return null;
  return top.map((x) => x.b);
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
async function askGemini(question, history) {
  const key = process.env.GEMINI_API_KEY;
  if (!key) return { status: 'no_key' };
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
        system_instruction: { parts: [{ text: SYSTEM_PROMPT }] },
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
      return { status: 'error' };
    }
    console.error('[rv-chat] gemini fetch failed:', e && e.message ? String(e.message).slice(0, 120) : 'unknown');
    return { status: 'error' };
  } finally {
    clearTimeout(timer);
  }
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
      return json(res, 200, { ok: 1, ready: Boolean(process.env.GEMINI_API_KEY) });
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

    // Lớp 3: chưa có key -> báo "đang chuẩn bị" (widget tự xử lý).
    if (!process.env.GEMINI_API_KEY) {
      return json(res, 503, { error: 'not_ready', message: MSG_NOT_READY });
    }

    // Lớp 4: Gemini.
    const g = await askGemini(question, history);
    if (g.status === 'quota') {
      return json(res, 429, { error: 'quota', message: MSG_QUOTA });
    }
    if (g.status === 'no_key') {
      return json(res, 503, { error: 'not_ready', message: MSG_NOT_READY });
    }
    if (g.status !== 'ok') {
      return json(res, 500, { error: 'error', message: MSG_ERROR });
    }

    // Lớp 5: kiểm chứng trích dẫn Kinh Thánh rồi mới trả về.
    const v = verifyCitations(g.text);
    let answer = v.text;
    if (v.removed > 0) {
      answer += `\n\n— Đã gỡ ${v.removed} trích dẫn Kinh Thánh chưa kiểm chứng được.`;
    }
    return json(res, 200, {
      answer,
      source: 'gemini',
      removed_citations: v.removed,
    });
  } catch (e) {
    // Không bao giờ lộ stack trace / chi tiết lỗi ra ngoài.
    console.error('[rv-chat] handler error:', e && e.message ? String(e.message).slice(0, 120) : 'unknown');
    return json(res, 500, { error: 'error', message: MSG_ERROR });
  }
}
