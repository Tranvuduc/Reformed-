// Builds lv.json: LibriVox audiobooks (Internet Archive collection "librivoxaudio") by authors in ia.json.
// Needs network (archive.org). Run by .github/workflows/audio.yml.
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
  let docs = [];
  for (let t = 0; t < 3 && !docs.length; t++) {
    try {
      const url = "https://archive.org/advancedsearch.php?" + new URLSearchParams({ q: `collection:librivoxaudio AND creator:(${sur})`, rows: "100", output: "json" }) + ["identifier", "title", "creator", "runtime", "language"].map((f) => "&fl[]=" + f).join("");
      const r = await fetch(url, { headers: { "User-Agent": "reformed-vietnam-catalog" }, signal: AbortSignal.timeout(25000) });
      if (r.ok) { docs = (await r.json()).response.docs || []; break; }
    } catch {}
    await sleep(3000);
  }
  let ai = -1, n = 0;
  for (const d of docs) {
    const lang = [].concat(d.language || []).join(" ");
    if (lang && !/eng/i.test(lang)) continue;
    const au = [].concat(d.creator || []).map(norm);
    if (!au.some((x) => x.split(" ").includes(sur) && (x.split(" ").includes(first) || first.length === 1 && x.split(" ").some((w) => w[0] === first)))) continue;
    const title = String([].concat(d.title || [d.identifier])[0]).replace(/\s+/g, " ").trim();
    const link = "details/" + d.identifier;
    if (seen.has(d.identifier)) continue;
    seen.add(d.identifier);
    if (ai < 0) { ai = an.length; an.push(name); }
    out.push([ai, title.slice(0, 140), link, [].concat(d.runtime || "")[0] || ""]);
    n++;
  }
  console.log(name, n);
  await sleep(600);
}
fs.writeFileSync("lv.json", JSON.stringify({ a: an, b: out }));
console.log("total", out.length);
