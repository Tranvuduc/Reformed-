// Hybrid CI translator for the 500-book pipeline: Muse (Anthropic API) + Gemini (free).
// Usage: node tools/translate500.mjs <batch|auto> [muse|gemini|auto]
// - batch 1-4  -> Muse (shortest, most-read books: best quality)
// - batch 5-20 -> Gemini free tier ($0, slower)
// Output: translations/<author>-<work>.txt + appended translations/index.json entries.
// Resumable per chunk: translations/.tmp500/<slug>/NNNN.txt
// Token-cheap for the operator: all LLM work happens inside CI with API keys,
// never in the chat context.
import fs from 'node:fs';
import path from 'node:path';

const LIST = JSON.parse(fs.readFileSync('tools/translate-500.json', 'utf8'));
const gl = JSON.parse(fs.readFileSync('tools/glossary.json', 'utf8'));
const SYS = `You translate public-domain Reformed Christian literature from English into natural, reverent Vietnamese for Vietnamese Protestant (Tin Lành) readers. Rules: be faithful to the author; no additions, no commentary, no summaries; keep paragraph breaks exactly; keep all Scripture references; render Scripture quotations in the style of the Vietnamese 1934 Bible (Kinh Thánh Tiếng Việt 1934) where possible. Use this glossary: ${JSON.stringify(gl)}. Output only the translation, no explanations.`;

const AKEY = process.env.ANTHROPIC_API_KEY || '';
const GKEY = process.env.GEMINI_API_KEY || '';
const AMODEL = process.env.MODEL || 'claude-sonnet-5-5';
let GMODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const SOURCE_BASE = (process.env.SOURCE_BASE || 'https://ccel.org').replace(/\/$/, '');
const MOCK = process.env.MOCK_TRANSLATE === '1'; // test hook: no API calls
// Pick a working gemini model: probe candidates with a real tiny generateContent
// call and use the first that answers. Priority: GEMINI_MODEL env, models-list
// API (newest stable flash), hardcoded fallbacks. Never trust a name blindly.
async function pickGeminiModel() {
  if (MOCK) return;
  const cands = [];
  if (process.env.GEMINI_MODEL) cands.push(process.env.GEMINI_MODEL);
  try {
    const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=100',
      { headers: { 'x-goog-api-key': GKEY } });
    const j = await r.json();
    const ids = (j.models || []).filter((m) => (m.supportedGenerationMethods || []).includes('generateContent')).map((m) => m.name.replace('models/', ''));
    const ver = (x) => ((x.match(/^gemini-(\d+(?:\.\d+)?)-flash$/) || [])[1] || 0) * 1;
    for (const m of ids.filter((x) => ver(x) > 0).sort((a, b) => ver(b) - ver(a)))
      if (!cands.includes(m)) cands.push(m);
  } catch (e) { console.error('model list failed:', e.message); }
  for (const m of ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.0-flash-lite'])
    if (!cands.includes(m)) cands.push(m);
  for (const m of cands) {
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent`,
        { method: 'POST', headers: { 'x-goog-api-key': GKEY, 'content-type': 'application/json' },
          body: JSON.stringify({ contents: [{ parts: [{ text: 'ping' }] }], generationConfig: { maxOutputTokens: 1 } }) });
      if (r.ok) { GMODEL = m; console.log('gemini model:', m); return; }
      console.error(`model ${m} probe: HTTP ${r.status}`);
    } catch (e) { console.error(`model ${m} probe error:`, e.message); }
  }
  throw new Error('no working gemini model found');
}

let batchArg = process.argv[2] || 'auto';
let engineArg = (process.argv[3] || 'auto').toLowerCase();
const slugOf = (e) => `${e.id.split('/')[0]}-${e.id.split('/')[1]}`.toLowerCase().replace(/[^a-z0-9-]+/g, '-');
const doneFile = (e) => `translations/${slugOf(e)}.txt`;

function nextBatch() {
  for (let b = 1; b <= 200; b++) {
    const items = LIST.filter((e) => e.batch === b);
    if (items.length && items.some((e) => !fs.existsSync(doneFile(e)))) return b;
  }
  return 0;
}
const batch = batchArg === 'auto' ? nextBatch() : +batchArg;
if (!batch) { console.log('all 20 batches complete'); process.exit(0); }
if (engineArg === 'auto') engineArg = batch <= 4 ? 'muse' : 'gemini';
if (engineArg === 'muse' && !AKEY && !MOCK) { console.error('ANTHROPIC_API_KEY missing'); process.exit(1); }
if (engineArg === 'gemini' && !GKEY && !MOCK) { console.error('GEMINI_API_KEY missing'); process.exit(1); }
console.log(`batch ${batch}, engine ${engineArg}`);

const items = LIST.filter((e) => e.batch === batch && !fs.existsSync(doneFile(e)));
console.log(`${items.length} books to translate in batch ${batch}`);

async function museCall(text) {
  for (let t = 0; t < 4; t++) {
    try {
      const r = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'x-api-key': AKEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
        body: JSON.stringify({ model: AMODEL, max_tokens: 4096, system: SYS, messages: [{ role: 'user', content: text }] }),
      });
      if (r.ok) { const j = await r.json(); return j.content.map((c) => c.text || '').join(''); }
    } catch {}
    await new Promise((s) => setTimeout(s, 5000 * (t + 1)));
  }
  throw new Error('muse call failed');
}
async function geminiCall(text) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GMODEL}:generateContent`;
  let lastErr = 'unknown';
  for (let t = 0; t < 4; t++) {
    try {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'x-goog-api-key': GKEY, 'content-type': 'application/json' },
        body: JSON.stringify({ system_instruction: { parts: [{ text: SYS }] }, generationConfig: { temperature: 0.2, maxOutputTokens: 4096 }, contents: [{ parts: [{ text }] }] }),
      });
      if (r.ok) {
        const j = await r.json();
        const out = (j.candidates?.[0]?.content?.parts || []).map((p) => p.text || '').join('');
        if (out.trim()) return out;
        lastErr = 'empty response';
      } else {
        lastErr = `HTTP ${r.status} ${(await r.text().catch(() => '')).slice(0, 160)}`;
      }
    } catch (e) { lastErr = e.message; }
    await new Promise((s) => setTimeout(s, 8000 * (t + 1)));
  }
  throw new Error('gemini call failed: ' + lastErr);
}
const rawCall = engineArg === 'muse' ? museCall : geminiCall;
// MOCK_TRANSLATE=1: fake translation for pipeline testing (no API keys needed)
const call = MOCK
  ? async (text) => (text.startsWith('Give a short') ? 'Tựa Sách Thử Nghiệm' : '[VI] ' + text)
  : rawCall;
// Clean OCR text (archive.org): rejoin wrapped lines, drop IA boilerplate
function cleanOcr(t) {
  t = t.replace(/^[\s\S]*?https?:\/\/(www\.)?archive\.org\/details\/[^\n]*\n/, '');
  t = t.replace(/\f/g, '\n\n');
  t = t.replace(/(?<!\n)\n(?!\n)/g, ' ');
  t = t.replace(/[ \t]{2,}/g, ' ');
  t = t.replace(/\n{3,}/g, '\n\n');
  return t.trim();
}
// Split over-long paragraphs (OCR texts) at sentence boundaries
function splitLong(paras, maxLen = 2800) {
  const out = [];
  for (const p of paras) {
    if (p.length <= maxLen || p.length < 100) { out.push(p); continue; }
    const parts = p.match(/[^.!?]+[.!?]+["']?\s*/g) || [p];
    let cur = '';
    for (const s of parts) {
      if (cur.length + s.length > maxLen && cur) { out.push(cur.trim()); cur = ''; }
      cur += s;
    }
    if (cur.trim()) out.push(cur.trim());
  }
  return out.filter((s) => s.length > 0);
}
const pace = MOCK ? 0 : engineArg === 'gemini' ? 4000 : 1200; // stay under free-tier RPM
let lastCall = 0;
async function paced(text) {
  const wait = Math.max(0, lastCall + pace - Date.now());
  if (wait) await new Promise((r) => setTimeout(r, wait));
  lastCall = Date.now();
  return call(text);
}
if (engineArg === 'gemini') await pickGeminiModel();

const idxPath = 'translations/index.json';
const idx = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
const failures = [];
let chunksTotal = 0;
const MAXCHUNKS = 950;

for (const e of items) {
  const slug = slugOf(e);
  const tmpDir = `translations/.tmp500/${slug}`;
  fs.mkdirSync(tmpDir, { recursive: true });
  try {
    const [au, work] = e.id.split('/');
    const srcUrl = e.src || `${SOURCE_BASE}/ccel/${au[0]}/${au}/${work}/cache/${work}.txt`;
    let src = await (await fetch(srcUrl, { headers: { 'User-Agent': 'ReformedVietnamBot/1.0' }, redirect: 'follow' })).text();
    if (src.length < 1000) throw new Error('source too short');
    if (e.src) src = cleanOcr(src); // archive.org OCR cleanup
    if (src.length < 1000) throw new Error('source too short after cleanup');
    const chunks = [];
    let cur = '';
    for (const p of splitLong(src.split(/\n\s*\n/))) {
      if (cur.length + p.length > 1800 && cur) { chunks.push(cur); cur = ''; }
      cur += (cur ? '\n\n' : '') + p.trim();
    }
    if (cur) chunks.push(cur);
    let done = 0;
    for (let k = 0; k < chunks.length && chunksTotal < MAXCHUNKS; k++) {
      const f = path.join(tmpDir, String(k + 1).padStart(4, '0') + '.txt');
      if (!fs.existsSync(f)) {
        const tr = await paced(chunks[k]);
        fs.writeFileSync(f, tr);
        chunksTotal++;
      }
      done++;
    }
    if (done < chunks.length) { console.log(`${e.id}: paused at chunk ${done}/${chunks.length} (cap)`); break; }
    // assemble
    let out = '';
    for (let k = 0; k < chunks.length; k++) out += fs.readFileSync(path.join(tmpDir, String(k + 1).padStart(4, '0') + '.txt'), 'utf8') + '\n\n';
    fs.writeFileSync(doneFile(e), out.trim() + '\n');
    fs.rmSync(tmpDir, { recursive: true, force: true });
    // Vietnamese title: one cheap extra call
    let viTitle = e.title_en;
    try {
      const t = await paced(`Give a short, natural Vietnamese book title (max 8 words) for this Reformed Christian book: "${e.title_en}" by ${e.author_en}. Use Protestant Vietnamese vocabulary (Phúc Âm, Đức Chúa Trời, Hội Thánh). Output only the title, nothing else.`);
      if (t.trim().length < 80) viTitle = t.trim().replace(/^["']|["']$/g, '');
    } catch {}
    idx.push({ id: e.id, file: `${slug}.txt`, title: viTitle, orig: e.title_en, author: e.author_en, by: engineArg === 'muse' ? 'Muse' : 'Gemini', reviewed: false });
    fs.writeFileSync(idxPath, JSON.stringify(idx, null, 1));
    console.log(`OK ${e.id} (${chunks.length} chunks) -> ${viTitle}`);
  } catch (err) {
    console.error(`FAIL ${e.id}: ${err.message}`);
    failures.push({ id: e.id, error: err.message });
  }
}
if (failures.length) fs.writeFileSync('tools/translate-500-failures.json', JSON.stringify(failures, null, 1));
console.log(`batch ${batch} done: ${items.length - failures.length} ok, ${failures.length} failed, ${chunksTotal} chunks`);
