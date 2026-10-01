// Pre-translate books into the shared cache by driving the real reader in headless Chromium.
// Usage: node tools/pretranslate.mjs "id1,id2" [maxPagesPerBook] [site]
import { chromium } from 'playwright';
import fs from 'node:fs';
const GKEY = process.env.GROQ_API_KEY || '';
const GROQ_MODEL = process.env.GROQ_MODEL || 'llama-3.3-70b-versatile';
const PROV = process.env.PROVIDER || (process.env.GEMINI_API_KEY ? 'gemini' : 'groq');
const IS_GEMINI = PROV === 'gemini';
const OAI = {
  groq: { url: 'https://api.groq.com/openai/v1', key: GKEY, gap: 16000, budget: 2000, max: 3600 },
  mistral: { url: 'https://api.mistral.ai/v1', key: process.env.MISTRAL_API_KEY || '', gap: 3000, budget: 5000, max: 7000 },
  cerebras: { url: 'https://api.cerebras.ai/v1', key: process.env.CEREBRAS_API_KEY || '', gap: 7000, budget: 3500, max: 6000 }
}[PROV] || null;
const KEY = IS_GEMINI ? (process.env.GEMINI_API_KEY || GKEY) : (OAI ? OAI.key : GKEY);
const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const gl = JSON.parse(fs.readFileSync(new URL('./glossary.json', import.meta.url), 'utf8'));
const SYS = `You translate public-domain Reformed Christian literature from English into natural, reverent Vietnamese for Vietnamese Protestant readers. Be faithful to the author; no additions or commentary; keep Scripture references; render Scripture in the Vietnamese Bible style (Kinh Thánh Tiếng Việt 1934 wording where possible). Use this glossary: ${JSON.stringify(gl)}. You receive a JSON array of paragraphs; return a JSON array of strings with exactly the same length and order, one translation per paragraph.`;
let lastCall = 0, lastErr = '';
let gModel = MODEL, qModel = GROQ_MODEL;
async function pickModels() {
  try {
    if (IS_GEMINI) {
      const r = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=100', { headers: { 'x-goog-api-key': KEY } });
      const j = await r.json();
      const ids = (j.models || []).filter(m => (m.supportedGenerationMethods || []).includes('generateContent')).map(m => m.name.replace('models/', ''));
      lastErr = 'gemini models: ' + ids.join(',').slice(0, 300);
      const ver = x => (x.match(/^gemini-(\d+(?:\.\d+)?)-flash$/) || [0, 0])[1] * 1;
      const stable = ids.filter(x => ver(x) > 0).sort((a, b) => ver(b) - ver(a));
      const pref = [process.env.GEMINI_MODEL_FORCE, stable[0], 'gemini-flash-latest', 'gemini-3-flash-preview', MODEL];
      gModel = pref.find(x => x && ids.includes(x)) || ids.find(x => /flash/.test(x) && !/image|tts|live|preview/.test(x)) || ids[0] || MODEL;
      if (!r.ok) lastErr = 'gemini list ' + r.status + ' ' + JSON.stringify(j).slice(0, 250).replace(KEY, '***');
    } else {
      const r = await fetch(OAI.url + '/models', { headers: { authorization: 'Bearer ' + OAI.key } });
      const j = await r.json();
      const ids = (j.data || []).map(m => m.id);
      lastErr = 'groq models: ' + ids.join(',').slice(0, 300);
      if (PROV === 'mistral' || PROV === 'cerebras') {
        const want = process.env.MODEL_FORCE || (PROV === 'mistral' ? 'mistral-large-latest' : 'gpt-oss-120b');
        qModel = ids.includes(want) ? want : (ids.find(x => /large|120b|235b|70b|medium|small/.test(x) && !/embed|ocr|moderation|vision|code/.test(x)) || ids[0] || want);
        return;
      }
      const pref = [GROQ_MODEL, 'llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 'qwen/qwen3-32b', 'meta-llama/llama-4-scout-17b-16e-instruct', 'openai/gpt-oss-20b'];
      qModel = pref.find(x => ids.includes(x)) || ids.find(x => /llama|qwen|gpt-oss/.test(x) && !/guard|whisper|tts/.test(x)) || GROQ_MODEL;
    }
  } catch (e) { lastErr = 'list error ' + e.message; }
}
await pickModels();
async function groq1(src) {
  for (let a = 0; a < 6; a++) {
    const wait = Math.max(0, lastCall + OAI.gap - Date.now()); // stay under free TPM
    if (wait) await new Promise(r => setTimeout(r, wait));
    lastCall = Date.now();
    try {
      const r = await fetch(OAI.url + '/chat/completions', {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: 'Bearer ' + OAI.key },
        body: JSON.stringify({
          model: qModel, temperature: 0.2, [PROV === 'mistral' ? 'max_tokens' : 'max_completion_tokens']: OAI.max, reasoning_effort: /gpt-oss/.test(qModel) ? 'low' : undefined,
          messages: [
            { role: 'system', content: SYS + ' Reply with ONLY a JSON object {"t":[...]} where t is the array of translations, no markdown fences.' },
            { role: 'user', content: JSON.stringify({ paragraphs: src }) }]
        })
      });
      if (r.status === 429 || r.status >= 500) { await new Promise(r => setTimeout(r, 30000 * (a + 1))); continue; }
      if (!r.ok) { lastErr = 'groq ' + r.status + ' ' + (await r.text()).replace(/\s+/g, ' ').replace(OAI.key, '***').slice(0, 300); throw new Error(lastErr); }
      const j = await r.json();
      const c = j.choices[0].message.content || ''; const arr = JSON.parse(c.slice(c.indexOf('{'), c.lastIndexOf('}') + 1)).t;
      if (Array.isArray(arr) && arr.length === src.length && arr.every(x => typeof x === 'string' && x.trim())) return arr;
      throw new Error('bad shape');
    } catch (e) { if (a === 5) throw e; await new Promise(r => setTimeout(r, 8000)); }
  }
  throw new Error('groq failed');
}
async function groq(src) {
  // free-tier TPM is ~8k: send small sub-batches (~2000 chars of English each)
  const out = []; let cur = [], n = 0;
  const flush = async () => { if (cur.length) { out.push(...await groq1(cur)); cur = []; n = 0; } };
  for (const p of src) { if (n + p.length > OAI.budget && cur.length) await flush(); cur.push(p); n += p.length; }
  await flush(); return out;
}
async function gemini(src) {
  for (let a = 0; a < 6; a++) {
    const wait = Math.max(0, lastCall + 4500 - Date.now()); // ~13 req/min
    if (wait) await new Promise(r => setTimeout(r, wait));
    lastCall = Date.now();
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${gModel}:generateContent`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-goog-api-key': KEY },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: SYS }] },
          contents: [{ role: 'user', parts: [{ text: JSON.stringify(src) }] }],
          generationConfig: { responseMimeType: 'application/json', temperature: 0.2 }
        })
      });
      if (r.status === 429 || r.status >= 500 || r.status === 404) { lastErr = 'gemini ' + r.status + ' ' + gModel; if (r.status !== 429) { const alt = ['gemini-flash-latest', 'gemini-3-flash-preview', 'gemini-2.5-flash-lite', 'gemini-2.5-pro']; gModel = alt[(alt.indexOf(gModel) + 1) % alt.length]; } await new Promise(r => setTimeout(r, 15000 * (a + 1))); continue; }
      if (!r.ok) { lastErr = 'gemini ' + r.status + ' ' + (await r.text()).replace(/\s+/g, ' ').replace(KEY, '***').slice(0, 300); throw new Error(lastErr); }
      const j = await r.json();
      const t = j.candidates?.[0]?.content?.parts?.map(x => x.text).join('') || '';
      const arr = JSON.parse(t);
      if (Array.isArray(arr) && arr.length === src.length && arr.every(x => typeof x === 'string' && x.trim())) return arr;
      throw new Error('bad shape');
    } catch (e) { if (a === 5) throw e; await new Promise(r => setTimeout(r, 5000)); }
  }
  throw new Error('gemini failed');
}
let ids = (process.argv[2] || '').split(',').map(s => s.trim()).filter(Boolean);
if (process.env.SHARD) { const [i, n] = process.env.SHARD.split('/').map(Number); ids = ids.filter((_, k) => k % n === i); }
const maxP = +process.argv[3] || 400;
const site = (process.argv[4] || 'https://reformed-vietnam.vercel.app').replace(/\/$/, '');
const BOT = (process.env.BOT_NAME || 'bot').toLowerCase().replace(/[^a-z0-9-]/g, '-').slice(0, 20);
const hist = [];
async function report(msg) { console.log(msg); hist.push(msg.slice(0, 420)); if (hist.length > 6) hist.shift(); msg = hist.join(' || '); try { await fetch(`${(process.argv[4] || 'https://reformed-vietnam.vercel.app').replace(/\/$/, '')}/api/tr`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ status: { bot: BOT, msg } }) }); } catch (e) {} }
const deadline = Date.now() + 5.5 * 3600 * 1000;
await report('start; models: ' + (IS_GEMINI ? gModel : (PROV + ':' + qModel)) + ' | ' + lastErr);
const b = await chromium.launch();
for (const id of ids) {
  if (Date.now() > deadline) break;
  const ctx = await b.newContext({ viewport: { width: 420, height: 800 } });
  const p = await ctx.newPage();
  await p.addInitScript(() => { try { localStorage.setItem('rv.trm', '1'); localStorage.setItem('rv.lang', 'vi'); } catch (e) {} });
  if (KEY) await p.exposeFunction('__trBatch', IS_GEMINI ? gemini : groq);
  let posts = 0, fails = 0;
  p.on('request', r => { if (r.method() === 'POST' && r.url().includes('/api/tr')) posts++; });
  try {
    await p.goto(`${site}/reader.html?id=${id}&p=0`, { waitUntil: 'domcontentloaded' });
    await p.waitForSelector('#sl', { timeout: 60000 });
    await p.waitForFunction(() => document.querySelector('#txt') && document.querySelector('#txt').innerText.length > 50, null, { timeout: 60000 });
    const total = await p.evaluate(() => +document.querySelector('#sl').max);
    const n = Math.min(total, maxP);
    await report(`${id}: ${total} pages, doing ${n}`);
    for (let i = 0; i < n; i++) {
      if (Date.now() > deadline) break;
      // wait until translation of this page finishes (status shows "Bản dịch máy" or failure text)
      let ok = false;
      for (let t = 0; t < (KEY ? 1200 : 240); t++) {
        const s = await p.evaluate(() => { const e = document.querySelector('#trs'); return e && !e.hidden ? e.textContent : ''; });
        if (/Bản dịch máy/.test(s)) { ok = true; break; }
        if (/Không dịch được/.test(s)) break;
        await p.waitForTimeout(500);
      }
      if (!ok) { fails++; await report(`${id} page ${i + 1} failed; status=` + (await p.evaluate(() => (document.querySelector('#trs') || {}).textContent)) + ' last=' + lastErr); if (fails >= 3) { console.log('  too many failures, stopping book'); break; } await p.waitForTimeout(20000); continue; }
      await p.waitForTimeout(1200); // let POST fly
      if (i < n - 1) await p.click('#nx');
    }
    await report(`${id}: done, ${posts} stored, ${fails} fails`);
  } catch (e) { await report(`${id}: error ${String(e.message).slice(0, 120)}`); }
  await ctx.close();
}
await b.close();
