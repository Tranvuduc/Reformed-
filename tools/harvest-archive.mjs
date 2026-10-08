// Harvest public-domain Reformed works from archive.org.
// For each author: advancedsearch -> metadata -> year<1930 (PD) -> _djvu.txt size.
// Output: tools/archive-books.json — [{id, title_en, author_en, year, bytes, src}]
// Dedupe against translations/index.json + tools/translate-500.json by normalized title.
import fs from 'node:fs';

const UA = { 'User-Agent': 'ReformedVietnamBot/1.0 (+https://reformed-vietnam.vercel.app)' };
const AUTHORS = [
  'Spurgeon, C. H.', 'Ryle, J. C.', 'Bonar, Horatius', 'Bonar, Andrew',
  'Winslow, Octavius', 'Newton, John', 'Edwards, Jonathan', 'Owen, John',
  'Baxter, Richard', 'Bunyan, John', 'Watson, Thomas', 'Flavel, John',
  'Charnock, Stephen', 'Sibbes, Richard', 'Brooks, Thomas', 'Burroughs, Jeremiah',
  'Manton, Thomas', 'Goodwin, Thomas', 'Howe, John', 'Bates, William',
  'Vincent, Thomas', 'Bridge, William', 'Caryl, Joseph', 'Clarkson, David',
  'Boston, Thomas', 'Rutherford, Samuel', 'McCheyne, Robert Murray',
  'Chalmers, Thomas', 'Candlish, Robert Smith', 'Cunningham, William',
  'Buchanan, James', 'Hodge, Charles', 'Hodge, A. A.',
  'Warfield, Benjamin Breckinridge', 'Shedd, William G. T.',
  'Dabney, Robert Lewis', 'Thornwell, James Henley', 'Palmer, Benjamin Morgan',
  'Plumer, William S.', 'Boyce, James Petigru', 'Dagg, John Leadley',
  'Fuller, Andrew', 'Calvin, John', 'Knox, John', 'Bullinger, Heinrich',
  'Ursinus, Zacharias', 'Henry, Matthew', 'Poole, Matthew', 'Gill, John',
  'Booth, Abraham', 'Keach, Benjamin', 'Kiffin, William',
  'Toplady, Augustus', 'Romaine, William', 'Hervey, James', 'Grimshaw, William',
  'Berridge, John', 'Whitefield, George',
];
const TITLE_SEARCHES = [
  'Belgic Confession', 'Canons of Dort', 'Westminster Larger Catechism',
  'Baptist Confession 1689', 'Scots Confession', 'Heidelberg Catechism',
  'Lectures to My Students', 'The Soul Winner', 'Attributes of God',
  'Golden Booklet', 'Sinners in the Hands of an Angry God',
  'Words to Winners of Souls', 'Cardiphonia',
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();

async function jget(url) {
  const r = await fetch(url, { headers: UA });
  if (!r.ok) throw new Error(r.status + ' ' + url);
  return r.json();
}

// existing titles for dedupe
const have = new Set();
for (const b of JSON.parse(fs.readFileSync('translations/index.json', 'utf8')))
  have.add(norm(b.title || '')), have.add(norm(b.orig || ''));
for (const b of JSON.parse(fs.readFileSync('tools/translate-500.json', 'utf8')))
  have.add(norm(b.title_en || ''));

const found = new Map(); // identifier -> {identifier,title,creator,date}
async function search(q) {
  const url = 'https://archive.org/advancedsearch.php?q=' + encodeURIComponent(q + ' AND mediatype:texts')
    + '&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=date&rows=200&output=json';
  try {
    const d = await jget(url);
    for (const doc of d.response.docs) {
      if (!found.has(doc.identifier)) found.set(doc.identifier, doc);
    }
  } catch (e) { console.error('search fail:', q.slice(0, 40), e.message); }
  await sleep(300);
}
for (const a of AUTHORS) await search(`creator:"${a}"`);
for (const t of TITLE_SEARCHES) await search(`title:"${t}"`);
console.error('unique identifiers:', found.size);

const out = [];
// resume: skip identifiers already saved from a previous partial run
let prior = [];
try { prior = JSON.parse(fs.readFileSync('tools/archive-books.json', 'utf8')); } catch {}
const doneIds = new Set(prior.map((b) => b.id));
for (const b of prior) out.push({ ...b, _key: '' });
if (prior.length) console.error('resuming, already have', prior.length);
function checkpoint() {
  const clean = [...out].sort((a, b) => a.bytes - b.bytes)
    .map(({ _key, ...r }) => r);
  fs.writeFileSync('tools/archive-books.json', JSON.stringify(clean, null, 1));
}
let i = 0;
const list = [...found.values()].filter((d) => !doneIds.has('arch/' + d.identifier));
await Promise.all(Array.from({ length: 8 }, async () => {
  while (i < list.length) {
    const doc = list[i++];
    try {
      const meta = await jget(`https://archive.org/metadata/${doc.identifier}`);
      const md = meta.metadata || {};
      const year = parseInt(String(md.date || '').slice(0, 4));
      if (!(year >= 1500 && year < 1930)) continue; // PD filter
      const files = meta.files || [];
      const txt = files.find((f) => f.name.endsWith('_djvu.txt')) || files.find((f) => f.name.endsWith('_text.txt'));
      if (!txt || !txt.size || txt.size < 8000) continue;
      const title = doc.title || md.title || doc.identifier;
      const key = norm(title) + '|' + norm(doc.creator || md.creator || '');
      if (have.has(norm(title))) continue;
      // skip if same normalized title already collected
      if (out.some((o) => o._key === key)) continue;
      out.push({
        id: 'arch/' + doc.identifier, title_en: String(title).slice(0, 120),
        author_en: String(doc.creator || md.creator || 'Unknown').slice(0, 60),
        year, bytes: txt.size, words: Math.round(txt.size / 6),
        src: `https://archive.org/download/${doc.identifier}/${txt.name}`,
        _key: key,
      });
      if (out.length % 25 === 0) { console.error('kept', out.length); checkpoint(); }
    } catch (e) { /* skip */ }
    await sleep(120);
  }
}));
checkpoint();
const clean = JSON.parse(fs.readFileSync('tools/archive-books.json', 'utf8'));
console.log(`wrote ${clean.length} archive.org books`);
if (clean.length) console.log(`shortest: ${clean[0].title_en.slice(0, 50)} (${clean[0].words}w)`);
