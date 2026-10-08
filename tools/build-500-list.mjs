// Build the candidate list: shortest untranslated Reformed works on CCEL.
// Sources: (1) /index/author/A-Z inline work lists, (2) per-author pages.
// Filters: Reformed authors only, no stubs (<8KB), no commentary/sermon multi-volumes,
// no already-translated. Sort by size ascending -> tools/translate-500.json
import fs from 'node:fs';

const UA = { 'User-Agent': 'ReformedVietnamBot/1.0 (+https://reformed-vietnam.vercel.app)' };
const REFORMED = [
  'owen', 'baxter', 'bunyan', 'watson', 'flavel', 'spurgeon', 'ryle', 'bonar',
  'charnock', 'brooks', 'sibbes', 'boston', 'rutherford', 'doddridge', 'edwards',
  'knox', 'calvin', 'poole', 'gill', 'pink', 'hodge', 'warfield', 'berkhof',
  'machen', 'boettner', 'alleine', 'bayly', 'burroughs', 'chalmers', 'dagg',
  'fuller', 'guthrie', 'halyburton', 'ambrose', 'ames', "m'cheyne", 'mccheyne',
  'newton', 'palmer', 'plumer', 'rainsford', 'shedd', 'smeaton', 'thornwell',
  'whitefield', 'bridge', 'caryl', 'clarkson', 'goodwin', 'manton', 'gurnall',
  'vincent', 'witsius', 'turretin', 'brakel', 'durham', 'dickson', 'fisher',
  'colquhoun', 'bellamy', 'hopkins', 'emmons', 'dabney', 'leighton', 'traill',
  'toplady', 'venn', 'bickersteth', 'moule', 'candlish', 'cunningham', 'buchanan',
  'girardeau', 'adger', 'hoge', 'ridgley', 'witherspoon', 'davies', 'tennent',
  'finley', 'miller', 'breckinridge', 'alexander',
];
// index-matched slugs that are NOT Reformed (wrong person / tradition)
const DROP_AUTHOR = new Set([
  'alexander_alexandria', 'alexander_capp', 'alexander_lyc', 'alexander_w',
  'allen_j', 'ball', 'bruce', 'chadwick', 'denney', 'edwards_tc', 'findlay',
  'fisher', 'goodwin', 'gray_jm', 'hastings', 'james', 'leightonpullan',
  'miller', 'moffat', 'montgomery', 'moule', 'nave', 'pilcher', 'potts',
  'robertson', 'rutherford_a', 'rutherford_an', 'scrivener', 'taylor_jh',
  'taylor_vincent', 'terrill_jg', 'watson_ra', 'fuller',
]);
// manually verified author pages (CCEL index misses them)
const MANUAL_AUTHORS = [
  'warfield', 'henry', 'boston', 'rutherford', 'palmer', 'shedd', 'doddridge',
  'charnock', 'bayly', 'ambrose', 'ames', 'vincent', 'strong', 'machen',
];
const MIN_BYTES = 8000; // stub floor
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const clean = (s) => s.replace(/\s+/g, ' ').replace(/&amp;/g, '&')
  .replace(/&#039;/g, "'").replace(/&#230;/g, 'ae').replace(/&quot;/g, '"').trim();

const translated = new Set(
  JSON.parse(fs.readFileSync('translations/index.json', 'utf8')).map((b) => b.id).filter(Boolean));
const seen = new Map();
const badTitle = (t) => /commentar/i.test(t);

function addWork(slug, name, work, title) {
  work = work.toLowerCase();
  const id = `${slug}/${work}`;
  if (/^henry\/mhc/.test(id)) return; // Matthew Henry commentary split volumes (dup of mhc)
  if (translated.has(id) || seen.has(id)) return;
  seen.set(id, { id, title_en: clean(title), author_en: clean(name), author: slug, work });
}

// Phase 1: index pages (authors + inline works)
for (const L of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
  let html;
  try {
    const r = await fetch(`https://ccel.org/index/author/${L}`, { headers: UA, redirect: 'follow' });
    if (!r.ok) throw new Error(r.status);
    html = await r.text();
  } catch (e) { console.error('index skip', L, e.message); continue; }
  const blocks = html.split('<a id="author_link_');
  for (let b = 1; b < blocks.length; b++) {
    const blk = blocks[b];
    const am = blk.match(/^([a-z0-9_-]+)"[^>]*>([\s\S]*?)<\/a>/);
    if (!am) continue;
    const slug = am[1], name = clean(am[2]);
    if (DROP_AUTHOR.has(slug)) continue;
    if (!REFORMED.some((k) => name.toLowerCase().includes(k))) continue;
    const wm = blk.matchAll(new RegExp(`https://ccel\\.org/ccel/${slug}/([a-z0-9_.-]+)"\\s*>\\s*([^<]{2,140})\\s*</a>`, 'g'));
    for (const w of wm) addWork(slug, name, w[1], w[2]);
  }
  await sleep(150);
}
console.error('phase1 candidates:', seen.size);

// Phase 2: author pages (fuller work lists where available)
for (const au of MANUAL_AUTHORS) {
  let html;
  try {
    const r = await fetch(`https://www.ccel.org/ccel/${au}`, { headers: UA, redirect: 'follow' });
    if (!r.ok) throw new Error(r.status);
    html = await r.text();
  } catch (e) { console.error('skip author', au, e.message); continue; }
  const authorName = clean((html.match(/<h1[^>]*>([^<]{2,80})<\/h1>/) || [])[1] || au);
  const re = new RegExp(`<a[^>]+href="https?://ccel\\.org/ccel/${au}/([a-z0-9_.-]+)/\\1"[^>]*>([^<]{2,140})</a>`, 'gi');
  let m, n = 0;
  while ((m = re.exec(html))) { const before = seen.size; addWork(au, authorName, m[1], m[2]); if (seen.size > before) n++; }
  if (n) console.error(`author page ${au}: +${n} works`);
  await sleep(200);
}
console.error('total candidates:', seen.size);

// Phase 3: size via capped download
async function cappedSize(e, cap = 2000000) {
  const url = `https://ccel.org/ccel/${e.author[0]}/${e.author}/${e.work}/cache/${e.work}.txt`;
  try {
    const r = await fetch(url, { headers: UA, redirect: 'follow' });
    if (!r.ok || !r.body) return -1;
    const reader = r.body.getReader();
    let n = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      n += value.length;
      if (n >= cap) { try { await reader.cancel(); } catch {} break; }
    }
    return n >= MIN_BYTES ? n : -1;
  } catch { return -1; }
}
const list = [...seen.values()];
const out = [];
let i = 0;
await Promise.all(Array.from({ length: 8 }, async () => {
  while (i < list.length) {
    const e = list[i++];
    const bytes = await cappedSize(e);
    if (bytes > 0) {
      out.push({ ...e, bytes });
      if (out.length % 100 === 0) console.error('sized', out.length);
    }
  }
}));
out.sort((a, b) => a.bytes - b.bytes);
const top = out.slice(0, 500).map((e, k) => ({
  id: e.id, title_en: e.title_en, author_en: e.author_en,
  bytes: e.bytes, capped: e.bytes >= 2000000,
  words: Math.round(Math.min(e.bytes, 2000000) / 6), batch: Math.floor(k / 25) + 1,
}));
fs.writeFileSync('tools/translate-500.json', JSON.stringify(top, null, 1));
console.log(`wrote ${top.length} books from ${out.length} sized candidates`);
if (top.length) console.log(`#1: ${top[0].id} (${top[0].words}w) | #${top.length}: ${top[top.length - 1].id} (${top[top.length - 1].words}w)`);
const byBatch = {};
for (const e of top) byBatch[e.batch] = (byBatch[e.batch] || 0) + 1;
console.log('batches:', JSON.stringify(byBatch));
