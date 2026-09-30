// Builds ia.json: public-domain Reformed/Puritan texts from the Internet Archive.
// Run: node scripts/build-catalog.mjs   (needs Node 18+, network access to archive.org)
import fs from "node:fs";
const AUTHORS = ["Calvin, John","Owen, John","Baxter, Richard","Bunyan, John","Flavel, John","Watson, Thomas","Gurnall, William","Boston, Thomas","Edwards, Jonathan","Hodge, Charles","Ryle, J. C.","Spurgeon, C. H.","Bonar, Horatius","Kuyper, Abraham","Berkhof, Louis","Bavinck, Herman","Warfield, Benjamin","Machen, J. Gresham","Vos, Geerhardus","Shedd, William","Dabney, Robert","Thornwell, James","Girardeau, John","Bridges, Charles","Brooks, Thomas","Sibbes, Richard","Goodwin, Thomas","Charnock, Stephen","Manton, Thomas","Ames, William","Perkins, William","Rutherford, Samuel","Gillespie, George","Binning, Hugh","Durham, James","Guthrie, William","Ussher, James","Howe, John","Bates, William","Alleine, Joseph","Alleine, Richard","Swinnock, George","Bolton, Robert","Burroughs, Jeremiah","Caryl, Joseph","Case, Thomas","Poole, Matthew","Henry, Matthew","Gill, John","Doddridge, Philip","Whitefield, George","Wesley, John","Newton, John","Cowper, William","Toplady, Augustus","Romaine, William","Venn, Henry","Simeon, Charles","Scott, Thomas","Cecil, Richard","Chalmers, Thomas","Duff, Alexander","Cunningham, William","Candlish, Robert","Bannerman, James","Bannerman, D. D.","Buchanan, James","Bonar, Andrew","M'Cheyne, Robert","Kennedy, John","Macleod, Donald","Smeaton, George","Fairbairn, Patrick","Hengstenberg, Ernst","Alexander, Archibald","Alexander, J. A.","Alexander, J. W.","Breckinridge, Robert","Boyce, James","Broadus, John","Dagg, John L.","Fuller, Andrew","Carey, William","Booth, Abraham","Keach, Benjamin","Kiffin, William","Knollys, Hanserd","Zwingli, Ulrich","Bullinger, Heinrich","Beza, Theodore","Bucer, Martin","Melanchthon, Philip","Luther, Martin","Knox, John","Tyndale, William","Latimer, Hugh","Cranmer, Thomas","Ridley, Nicholas","Jewel, John","Hooker, Richard","Turretin, Francis","Witsius, Herman","Voetius, Gisbertus","Owen, John, 1616-1683","Schaff, Philip","Hall, Robert","Haldane, Robert","Haldane, James","Murray, Andrew","Moody, Dwight","Pink, Arthur","Miller, Samuel","Plumer, William","Smyth, Thomas","Palmer, Benjamin","Blaikie, William","Kuiper, R. B.","Orr, James","Boettner, Loraine","Craig, Samuel","Warfield, B. B.","Bunyan, John, 1628-1688","Traill, Robert","Erskine, Ebenezer","Erskine, Ralph","Fisher, Edward","Marshall, Walter","Hopkins, Ezekiel","Leighton, Robert","Halyburton, Thomas","Willison, John","Vincent, Thomas","Doolittle, Thomas","Henry, Philip","Heywood, Oliver","Janeway, James","Mather, Cotton","Mather, Increase","Cotton, John","Hooker, Thomas","Shepard, Thomas","Bellamy, Joseph","Hopkins, Samuel","Dwight, Timothy","Nettleton, Asahel","Finney, Charles","Beecher, Lyman","Storrs, Richard"];
const Q = (a) => `creator:("${a}") AND mediatype:texts AND year:[1 TO 1929] AND downloads:[15 TO 99999999] AND -access-restricted-item:true AND (language:eng OR language:English)`;
const nk = (t) => t.toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 45);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const books = JSON.parse(fs.readFileSync("books.json", "utf8"));
const seen = new Set();
books.authors.forEach((a) => a.books.forEach((b) => seen.add(nk(b[1]))));
(books.extra || []).forEach((b) => seen.add(nk(b.en.t)));
const names = [], rows = [];
for (const a of [...new Set(AUTHORS)]) {
  const url = "https://archive.org/advancedsearch.php?" + new URLSearchParams({ q: Q(a), rows: "60", output: "json", sort: "downloads desc" }) +
    ["identifier", "title", "creator", "year", "downloads", "format"].map((f) => "&fl[]=" + f).join("");
  let docs = [];
  for (let t = 0; t < 3 && !docs.length; t++) {
    try { const r = await fetch(url); if (r.ok) docs = (await r.json()).response.docs; else await sleep(3000); } catch { await sleep(3000); }
  }
  const [sur, rest] = a.split(",").map((x) => x.trim().toLowerCase());
  const given = (rest || "").split(/[ .]+/).filter((w) => w.length > 1)[0] || "";
  const ok = (d) => [].concat(d.creator || []).some((c) => { const l = String(c).toLowerCase().trim(); return l.startsWith(sur + ", " + given) || l.startsWith(sur + "," + given); });
  let ai = -1, n = 0;
  for (const d of docs) {
    const title = (Array.isArray(d.title) ? d.title[0] : d.title || "").replace(/\s+/g, " ").trim();
    const k = nk(title);
    if (!title || title.length < 4 || seen.has(k) || !ok(d) || /travel|geograph|grammar|arithmetic|railroad|catalog|directory|almanac|genealog|visitation/i.test(title)) continue;
    const f = [].concat(d.format || []).join("|");
    const pdf = /PDF/i.test(f) ? 1 : 0, epub = /EPUB/i.test(f) ? 1 : 0;
    if (!pdf && !epub) continue;
    seen.add(k);
    if (ai < 0) { ai = names.length; names.push(a.replace(/^(.*), (.*)$/, "$2 $1").replace(/, \d.*$/, "")); }
    rows.push([ai, title.slice(0, 140), d.identifier, +String(d.year || 0).slice(0, 4) || 0, pdf + epub * 2]);
    if (++n >= 40) break;
  }
  console.log(a, n);
  await sleep(800);
}
fs.writeFileSync("ia.json", JSON.stringify({ a: names, b: rows }));
console.log("total", rows.length);
