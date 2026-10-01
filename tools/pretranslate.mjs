// Pre-translate books into the shared cache by driving the real reader in headless Chromium.
// Usage: node tools/pretranslate.mjs "id1,id2" [maxPagesPerBook] [site]
import { chromium } from 'playwright';
import fs from 'node:fs';
const KEY = process.env.GEMINI_API_KEY || '';
const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const gl = JSON.parse(fs.readFileSync(new URL('./glossary.json', import.meta.url), 'utf8'));
const SYS = `You translate public-domain Reformed Christian literature from English into natural, reverent Vietnamese for Vietnamese Protestant readers. Be faithful to the author; no additions or commentary; keep Scripture references; render Scripture in the Vietnamese Bible style (Kinh Thánh Tiếng Việt 1934 wording where possible). Use this glossary: ${JSON.stringify(gl)}. You receive a JSON array of paragraphs; return a JSON array of strings with exactly the same length and order, one translation per paragraph.`;
let lastCall = 0;
async function gemini(src) {
  for (let a = 0; a < 6; a++) {
    const wait = Math.max(0, lastCall + 4500 - Date.now()); // ~13 req/min
    if (wait) await new Promise(r => setTimeout(r, wait));
    lastCall = Date.now();
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-goog-api-key': KEY },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: SYS }] },
          contents: [{ role: 'user', parts: [{ text: JSON.stringify(src) }] }],
          generationConfig: { responseMimeType: 'application/json', temperature: 0.2 }
        })
      });
      if (r.status === 429 || r.status >= 500) { await new Promise(r => setTimeout(r, 15000 * (a + 1))); continue; }
      if (!r.ok) throw new Error('gemini ' + r.status);
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
const deadline = Date.now() + 5.5 * 3600 * 1000;
const b = await chromium.launch();
for (const id of ids) {
  if (Date.now() > deadline) break;
  const ctx = await b.newContext({ viewport: { width: 420, height: 800 } });
  const p = await ctx.newPage();
  await p.addInitScript(() => { try { localStorage.setItem('rv.trm', '1'); localStorage.setItem('rv.lang', 'vi'); } catch (e) {} });
  if (KEY) await p.exposeFunction('__trBatch', gemini);
  let posts = 0, fails = 0;
  p.on('request', r => { if (r.method() === 'POST' && r.url().includes('/api/tr')) posts++; });
  try {
    await p.goto(`${site}/reader.html?id=${id}&p=0`, { waitUntil: 'domcontentloaded' });
    await p.waitForSelector('#sl', { timeout: 60000 });
    await p.waitForFunction(() => document.querySelector('#txt') && document.querySelector('#txt').innerText.length > 50, null, { timeout: 60000 });
    const total = await p.evaluate(() => +document.querySelector('#sl').max);
    const n = Math.min(total, maxP);
    console.log(`${id}: ${total} pages, doing ${n}`);
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
      if (!ok) { fails++; console.log(`  page ${i + 1} failed`); if (fails >= 3) { console.log('  too many failures, stopping book'); break; } await p.waitForTimeout(20000); continue; }
      await p.waitForTimeout(1200); // let POST fly
      if (i < n - 1) await p.click('#nx');
    }
    console.log(`${id}: done, ${posts} pages newly stored, ${fails} fails`);
  } catch (e) { console.log(`${id}: error ${String(e.message).slice(0, 120)}`); }
  await ctx.close();
}
await b.close();
