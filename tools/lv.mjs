// Builds lv.json: LibriVox public-domain audiobooks by authors in ia.json.
// Needs network (librivox.org). Run by .github/workflows/audio.yml.
import fs from "node:fs";
const ia = JSON.parse(fs.readFileSync("ia.json", "utf8"));
const extra = ["John Bunyan","Charles Spurgeon","C. H. Spurgeon","John Calvin","Martin Luther","Jonathan Edwards","J. C. Ryle","Richard Baxter","John Newton","Andrew Murray","Thomas a Kempis","Augustine","Horatius Bonar","Isaac Watts","Matthew Henry","Brother Lawrence","John Wesley","George Whitefield","Charles Finney","D. L. Moody","Robert Murray McCheyne","Thomas Watson","John Owen","William Carey"];
const names = [...new Set([...ia.a, ...extra])];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const norm = (s) => String(s || "").toLowerCase().replace(/[^a-z ]/g, " ").replace(/\s+/g, " ").trim();
const out = [], seen = new Set(), an = [];
for (const name of names) {
  const parts = norm(name).split(" ");
  const sur = parts[parts.length - 1], first = parts[0];
  if (!sur || sur.length < 3) continue;
  let books = [];
  for (let t = 0; t < 3 && !books.length; t++) {
    try {
      const r = await fetch(`https://librivox.org/api/feed/audiobooks/?author=%5E${encodeURIComponent(sur)}&format=json&extended=0&limit=100`, { headers: { "User-Agent": "reformed-vietnam-catalog" } });
      if (r.ok) { const j = await r.json(); books = j.books || []; break; }
      if (r.status === 404) break;
    } catch {}
    await sleep(3000);
  }
  let ai = -1, n = 0;
  for (const b of books) {
    if (!/english/i.test(b.language || "English")) continue;
    const au = (b.authors || []).map((a) => norm(a.first_name + " " + a.last_name));
    if (!au.some((x) => x.endsWith(" " + sur) && (x.startsWith(first) || first.length === 1 && x[0] === first))) continue;
    if (!b.url_librivox || seen.has(b.url_librivox)) continue;
    seen.add(b.url_librivox);
    if (ai < 0) { ai = an.length; an.push(name); }
    out.push([ai, String(b.title).replace(/\s+/g, " ").trim().slice(0, 140), b.url_librivox.replace(/^https?:\/\/librivox\.org\//, ""), b.totaltime || ""]);
    n++;
  }
  console.log(name, n);
  await sleep(600);
}
fs.writeFileSync("lv.json", JSON.stringify({ a: an, b: out }));
console.log("total", out.length);
