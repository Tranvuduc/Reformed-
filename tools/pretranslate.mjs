// Pre-translate books into the shared cache by driving the real reader in headless Chromium.
// Usage: node tools/pretranslate.mjs "id1,id2" [maxPagesPerBook] [site]
import { chromium } from 'playwright';
import fs from 'node:fs';
const GKEY = process.env.GROQ_API_KEY || '';
const GROQ_MODEL = process.env.GROQ_MODEL || 'llama-3.3-70b-versatile';
const KEY = process.env.GEMINI_API_KEY || GKEY;
const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const gl = JSON.parse(fs.readFileSync(new URL('./glossary.json', import.meta.url), 'utf8'));
const SYS = `You translate public-domain Reformed Christian literature from English into natural, reverent Vietnamese for Vietnamese Protestant readers. Be faithful to the author; no additions or commentary; keep Scripture references; render Scripture in the Vietnamese Bible style (Kinh Thánh Tiếng Việt 1934 wording where possible). Use this glossary: ${JSON.stringify(gl)}. You receive a JSON array of paragraphs; return a JSON array of strings with exactly the same length and order, one translation per paragraph.`;
let lastCall = 0, lastErr = '';
let gModel = MODEL, qModel = GROQ_MODEL;
async function pickModels() {
  try {
    if (process.env.GEMINI_API_KEY) {
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
      const r = await fetch('https://api.groq.com/openai/v1/models', { headers: { authorization: 'Bearer ' + GKEY } });
      const j = await r.json();
      const ids = (j.data || []).map(m => m.id);
      lastErr = 'groq models: ' + ids.join(',').slice(0, 300);
      const pref = [GROQ_MODEL, 'llama-3.3-70b-versatile', 'openai/gpt-oss-120b', 'qwen/qwen3-32b', 'meta-llama/llama-4-scout-17b-16e-instruct', 'openai/gpt-oss-20b'];
      qModel = pref.find(x => ids.includes(x)) || ids.find(x => /llama|qwen|gpt-oss/.test(x) && !/guard|whisper|tts/.test(x)) || GROQ_MODEL;
    }
  } catch (e) { lastErr = 'list error ' + e.message; }
}
await pickModels();
async function groq(src) {
  for (let a = 0; a < 6; a++) {
    const wait = Math.max(0, lastCall + 20000 - Date.now()); // stay under free TPM
    if (wait) await new Promise(r => setTimeout(r, wait));
    lastCall = Date.now();
    try {
      const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: 'Bearer ' + GKEY },
        body: JSON.stringify({
          model: qModel, temperature: 0.2, max_completion_tokens: 8000, reasoning_effort: /gpt-oss/.test(qModel) ? 'low' : undefined,
          messages: [
            { role: 'system', content: SYS + ' Reply with ONLY a JSON object {"t":[...]} where t is the array of translations, no markdown fences.' },
            { role: 'user', content: JSON.stringify({ paragraphs: src }) }]
        })
      });
      if (r.status === 429 || r.status >= 500) { await new Promise(r => setTimeout(r, 30000 * (a + 1))); continue; }
      if (!r.ok) { lastErr = 'groq ' + r.status + ' ' + (await r.text()).replace(/\s+/g, ' ').replace(GKEY, '***').slice(0, 300); throw new Error(lastErr); }
      const j = await r.json();
      const c = j.choices[0].message.content || ''; const arr = JSON.parse(c.slice(c.indexOf('{'), c.lastIndexOf('}') + 1)).t;
      if (Array.isArray(arr) && arr.length === src.length && arr.every(x => typeof x === 'string' && x.trim())) return arr;
      throw new Error('bad shape');
    } catch (e) { if (a === 5) throw e; await new Promise(r => setTimeout(r, 8000)); }
  }
  throw new Error('groq failed');
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
      if (r.status === 429 || r.status >= 500) { lastErr = 'gemini ' + r.status; await new Promise(r => setTimeout(r, 15000 * (a + 1))); continue; }
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
const ids = (process.argv[2] || '').split(',').map(s => s.trim()).filter(Boolean);
const maxP = +process.argv[3] || 400;
const site = (process.argv[4] || 'https://reformed-vietnam.vercel.app').replace(/\/$/, '');
const BOT = process.env.BOT_NAME || 'bot';
const hist = [];
async function report(msg) { console.log(msg); hist.push(msg.slice(0, 420)); if (hist.length > 6) hist.shift(); msg = hist.join(' || '); try { await fetch(`${(process.argv[4] || 'https://reformed-vietnam.vercel.app').replace(/\/$/, '')}/api/tr`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ status: { bot: BOT, msg } }) }); } catch (e) {} }
const deadline = Date.now() + 5.5 * 3600 * 1000;
await report('start; models: ' + (process.env.GEMINI_API_KEY ? gModel : qModel) + ' | ' + lastErr);
const b = await chromium.launch();
for (const id of ids) {
  if (Date.now() > deadline) break;
  const ctx = await b.newContext({ viewport: { width: 420, height: 800 } });
  const p = await ctx.newPage();
  await p.addInitScript(() => { try { localStorage.setItem('rv.trm', '1'); localStorage.setItem('rv.lang', 'vi'); } catch (e) {} });
  if (KEY) await p.exposeFunction('__trBatch', process.env.GEMINI_API_KEY ? gemini : groq);
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
      for (let t = 0; t < 240; t++) {
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
