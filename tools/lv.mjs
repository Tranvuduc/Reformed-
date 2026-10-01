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
      const r = await fetch(`https://librivox.org/api/feed/audiobooks/?author=%5E${encodeURIComponent(sur)}&format=json&extended=0&limit=100`, { headers: { "User-Agent": "reformed-vietnam-catalog" }, signal: AbortSignal.timeout(20000) });
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
// Genre pass: LibriVox religious works regardless of author.
for (const genre of ["Religion", "Christianity", "Sermons", "Bibles", "Christian Fiction", "Essays", "Philosophy"]) {
  for (let off = 0; off < 1500; off += 100) {
    let books = [];
    for (let t = 0; t < 3; t++) {
      try {
        const r = await fetch(`https://librivox.org/api/feed/audiobooks/?genre=%5E${encodeURIComponent(genre)}&format=json&extended=0&limit=100&offset=${off}`, { headers: { "User-Agent": "reformed-vietnam-catalog" } });
        if (r.ok) { books = (await r.json()).books || []; break; }
        if (r.status === 404) break;
      } catch {}
      await sleep(3000);
    }
    if (!books.length) break;
    for (const b of books) {
      if (!/english/i.test(b.language || "English") || !b.url_librivox || seen.has(b.url_librivox)) continue;
      const title = String(b.title).replace(/\s+/g, " ").trim();
      if (/poem|poetry|fairy|novel|romance|adventure|mystery|detective|comedy|opera|short stories|collection|dramatic|play\b/i.test(title)) continue;
      if (["Philosophy", "Essays", "Christian Fiction"].includes(genre) && !/god|christ|church|bible|gospel|sermon|faith|prayer|soul|saint|psalm|religio|salvation|holy|testament|heaven|sin\b|grace/i.test(title)) continue;
      seen.add(b.url_librivox);
      const a0 = (b.authors || [])[0]; const nm = a0 ? `${a0.first_name || ""} ${a0.last_name || ""}`.trim() || "Anonymous" : "Anonymous";
      let ai = an.indexOf(nm); if (ai < 0) { ai = an.length; an.push(nm); }
      out.push([ai, title.slice(0, 140), b.url_librivox.replace(/^https?:\/\/librivox\.org\//, ""), b.totaltime || ""]);
    }
    console.log("genre", genre, off, out.length);
    await sleep(600);
    if (books.length < 100) break;
  }
}
fs.writeFileSync("lv.json", JSON.stringify({ a: an, b: out }));
console.log("total", out.length);
