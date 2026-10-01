// Builds pg.json: Project Gutenberg theology/religion books via the Gutendex API.
// Run by .github/workflows/pg.yml (needs network).
import fs from "node:fs";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const nk = (t) => t.toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 45);
const BAD = /travel|geograph|grammar|arithmetic|railroad|catalog|directory|almanac|genealog|poem|poetical|poetry|novel|romance|fairy|adventure|detective|mystery|opera|comedy|play\b|story of|tales?\b|stories|dictionary|lexicon|periodical|magazine|reader\b|primer|textbook|cookery|cook book|medicine|magic|occult|spiritualis|theosoph|mormon|koran|buddh|hindu|catholic encyclopedia|vulgate|douay|latin|\bgreek\b|\bgerman\b|\bfrench\b/i;
const TOPICS = ["theology", "christian", "sermons", "bible", "puritan", "reformation", "religion", "prayer", "church", "gospel", "devotion", "calvinism", "presbyterian", "baptist", "missions", "christianity"];
const names = [], rows = [], seen = new Set(), seenId = new Set();
for (const topic of TOPICS) {
  let url = `https://gutendex.com/books?topic=${encodeURIComponent(topic)}&languages=en&sort=popular`;
  for (let page = 0; page < 12 && url; page++) {
    let j = null;
    for (let t = 0; t < 3 && !j; t++) {
      try { const r = await fetch(url, { headers: { "User-Agent": "reformed-vietnam-catalog" } }); if (r.ok) j = await r.json(); else await sleep(4000); } catch { await sleep(4000); }
    }
    if (!j) break;
    let n = 0;
    for (const b of j.results || []) {
      const title = String(b.title || "").replace(/\s+/g, " ").trim();
      const k = nk(title);
      if (!title || title.length < 5 || BAD.test(title) || seen.has(k) || seenId.has(b.id) || (b.download_count || 0) < 60) continue;
      if (!(b.formats && (b.formats["application/epub+zip"] || b.formats["text/html"]))) continue;
      const a0 = (b.authors || [])[0];
      let nm = a0 ? String(a0.name).replace(/\s*\(.*?\)\s*/g, " ").replace(/^(.*?),\s*(.*)$/, "$2 $1").replace(/\s+/g, " ").trim() : "Anonymous";
      let ai = names.indexOf(nm); if (ai < 0) { ai = names.length; names.push(nm); }
      const y = a0 && a0.death_year ? Math.min(a0.death_year, 1929) - 10 : 0;
      seen.add(k); seenId.add(b.id); n++;
      rows.push([ai, title.slice(0, 140), b.id, y > 0 ? y : 0, 1]);
    }
    console.log(topic, page, n, rows.length);
    url = j.next; await sleep(700);
  }
}
fs.writeFileSync("pg.json", JSON.stringify({ a: names, b: rows }));
console.log("total", rows.length);
