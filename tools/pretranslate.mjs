// Pre-translate books into the shared cache by driving the real reader in headless Chromium.
// Usage: node tools/pretranslate.mjs "id1,id2" [maxPagesPerBook] [site]
import { chromium } from 'playwright';
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
