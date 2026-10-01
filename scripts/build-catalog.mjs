// Builds ia.json: public-domain Reformed/Puritan texts from the Internet Archive.
// Run: node scripts/build-catalog.mjs   (needs Node 18+, network access to archive.org)
import fs from "node:fs";
import { reformedOnly } from "../tools/exclude.mjs";
const AUTHORS = ["Calvin, John","Owen, John","Baxter, Richard","Bunyan, John","Flavel, John","Watson, Thomas","Gurnall, William","Boston, Thomas","Edwards, Jonathan","Hodge, Charles","Ryle, J. C.","Spurgeon, C. H.","Bonar, Horatius","Kuyper, Abraham","Berkhof, Louis","Bavinck, Herman","Warfield, Benjamin","Machen, J. Gresham","Vos, Geerhardus","Shedd, William","Dabney, Robert","Thornwell, James","Girardeau, John","Bridges, Charles","Brooks, Thomas","Sibbes, Richard","Goodwin, Thomas","Charnock, Stephen","Manton, Thomas","Ames, William","Perkins, William","Rutherford, Samuel","Gillespie, George","Binning, Hugh","Durham, James","Guthrie, William","Ussher, James","Howe, John","Bates, William","Alleine, Joseph","Alleine, Richard","Swinnock, George","Bolton, Robert","Burroughs, Jeremiah","Caryl, Joseph","Case, Thomas","Poole, Matthew","Henry, Matthew","Gill, John","Doddridge, Philip","Whitefield, George","Wesley, John","Newton, John","Cowper, William","Toplady, Augustus","Romaine, William","Venn, Henry","Simeon, Charles","Scott, Thomas","Cecil, Richard","Chalmers, Thomas","Duff, Alexander","Cunningham, William","Candlish, Robert","Bannerman, James","Bannerman, D. D.","Buchanan, James","Bonar, Andrew","M'Cheyne, Robert","Kennedy, John","Macleod, Donald","Smeaton, George","Fairbairn, Patrick","Hengstenberg, Ernst","Alexander, Archibald","Alexander, J. A.","Alexander, J. W.","Breckinridge, Robert","Boyce, James","Broadus, John","Dagg, John L.","Fuller, Andrew","Carey, William","Booth, Abraham","Keach, Benjamin","Kiffin, William","Knollys, Hanserd","Zwingli, Ulrich","Bullinger, Heinrich","Beza, Theodore","Bucer, Martin","Melanchthon, Philip","Luther, Martin","Knox, John","Tyndale, William","Latimer, Hugh","Cranmer, Thomas","Ridley, Nicholas","Jewel, John","Hooker, Richard","Turretin, Francis","Witsius, Herman","Voetius, Gisbertus","Owen, John, 1616-1683","Schaff, Philip","Hall, Robert","Haldane, Robert","Haldane, James","Murray, Andrew","Moody, Dwight","Pink, Arthur","Miller, Samuel","Plumer, William","Smyth, Thomas","Palmer, Benjamin","Blaikie, William","Kuiper, R. B.","Orr, James","Boettner, Loraine","Craig, Samuel","Warfield, B. B.","Bunyan, John, 1628-1688","Traill, Robert","Erskine, Ebenezer","Erskine, Ralph","Fisher, Edward","Marshall, Walter","Hopkins, Ezekiel","Leighton, Robert","Halyburton, Thomas","Willison, John","Vincent, Thomas","Doolittle, Thomas","Henry, Philip","Heywood, Oliver","Janeway, James","Mather, Cotton","Mather, Increase","Cotton, John","Hooker, Thomas","Shepard, Thomas","Bellamy, Joseph","Hopkins, Samuel","Dwight, Timothy","Nettleton, Asahel","Finney, Charles","Beecher, Lyman","Storrs, Richard"];
const Q = (a) => `creator:("${a}") AND mediatype:texts AND year:[1 TO 1929] AND downloads:[15 TO 99999999] AND -access-restricted-item:true AND (language:eng OR language:English)`;
const AMBIG = new Set(["Haldane, James","Duff, Alexander","Miller, Samuel","Murray, Andrew","Hall, Robert","Scott, Thomas","Wesley, John","Cowper, William","Craig, Samuel","Smyth, Thomas","Palmer, Benjamin","Orr, James","Storrs, Richard","Hopkins, Samuel","Cotton, John","Cecil, Richard","Bates, William","Poole, Matthew","Henry, Philip","Vincent, Thomas","Case, Thomas","Kennedy, John","Macleod, Donald","Blaikie, William","Guthrie, William","Buchanan, James","Fisher, Edward","Marshall, Walter","Leighton, Robert","Mather, Increase","Dwight, Timothy","Fuller, Andrew","Booth, Abraham","Shedd, William","Newton, John","Simeon, Charles"]);
const THEO = /god|christ|gospel|sermon|church|bible|faith|doctrin|divin|theolog|scriptur|salvation|grace|prayer|psalm|testament|covenant|saint|soul|sin\b|holy|spirit|religio|christian|puritan|reformat|works|writings|commentar|preach|pastor|minister|catechis|creed|heaven|death|life of|memoir|epistle|romans|hebrews|matthew|john\b|revelation|providence|repent|conversion|election|predestin|justif|sanctif|gospel/i;
const nk = (t) => t.toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 45);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const books = JSON.parse(fs.readFileSync("books.json", "utf8"));
const seen = new Set();
books.authors.forEach((a) => a.books.forEach((b) => seen.add(nk(b[1]))));
(books.extra || []).forEach((b) => seen.add(nk(b.en.t)));
const names = [], rows = [];
for (const a of [...new Set(AUTHORS)]) {
  const url = "https://archive.org/advancedsearch.php?" + new URLSearchParams({ q: Q(a), rows: "300", output: "json", sort: "downloads desc" }) +
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
    if (!title || title.length < 4 || seen.has(k) || !ok(d) || (AMBIG.has(a) && !THEO.test(title)) || /travel|geograph|grammar|arithmetic|railroad|catalog|directory|almanac|genealog|visitation|poem|poetical|poetry|primitive remed|medicine|medical|novel|romance/i.test(title)) continue;
    const f = [].concat(d.format || []).join("|");
    const pdf = /PDF/i.test(f) ? 1 : 0, epub = /EPUB/i.test(f) ? 1 : 0;
    if (!pdf && !epub) continue;
    seen.add(k);
    if (ai < 0) { ai = names.length; names.push(a.replace(/^(.*), (.*)$/, "$2 $1").replace(/, \d.*$/, "")); }
    rows.push([ai, title.slice(0, 140), d.identifier, +String(d.year || 0).slice(0, 4) || 0, pdf + epub * 2]);
    if (++n >= 150) break;
  }
  console.log(a, n);
  await sleep(800);
}
// Subject-based pass: public-domain theology texts regardless of author (quality gate: downloads, pdf/epub, title filter).
const OFF = /liguori|ligouri|aquinas|newman|pohle|catholic church|frassinetti|nageleisen|spirago|de sales|john of the cross|bonaventure|loyola|bellarmine|batiffol|manning|fielding smith|joseph smith|brigham young|mormon|latter[- ]day|mary baker|eddy|watchtower|blavatsky|theosoph|swedenborg|machiavelli|cardinal/i;
const OFFT = /\b(rosary|purgatory|novena|parish priest|mormon|latter[- ]day|breviary|benediction|sacred heart|our lady|immaculate|stations of the cross|roman missal|summa|spiritualis[mt]|theosoph|christian science|gout|coins|cookery|surgery|diseases|rheumat\w*)\b/i;
const BAD = /travel|geograph|grammar|arithmetic|railroad|catalog|directory|almanac|genealog|visitation|poem|poetical|poetry|primitive remed|medicine|medical|novel|romance|periodical|magazine|report of|annual|proceedings|minutes|statutes|laws of|journal of|dictionary|lexicon|directory|school|textbook|reader\b|primer|hymn-?book|songs?\b|music|volume \d+ of \d+/i;
const SUBJ = [
  '("Reformed Church" OR "Presbyterian Church" OR Calvinism OR Puritans OR "Reformed (Dutch) Church" OR Predestination OR "Westminster Assembly")',
  '("Theology, Doctrinal" OR Atonement OR Justification OR Sanctification OR "Holy Spirit" OR Trinity OR "Christian life" OR "Salvation")',
  '(Sermons OR "Bible. N.T. -- Commentaries" OR "Bible. O.T. -- Commentaries" OR "Bible -- Commentaries" OR "Bible. N.T. -- Criticism, interpretation" OR Psalms)',
  '("Devotional literature" OR Prayer OR "Christian biography" OR Catechisms OR Reformation OR "Church history" OR Baptists OR Missions OR Evangelicalism)'
];
const nameIdx = new Map(names.map((n, i) => [n, i]));
const seenId = new Set(rows.map((r) => r[2]));
for (const sj of SUBJ) {
  for (let page = 1; page <= 2; page++) {
    const q = `${sj} AND mediatype:texts AND year:[1 TO 1929] AND downloads:[40 TO 99999999] AND -access-restricted-item:true AND language:eng`;
    const url = "https://archive.org/advancedsearch.php?" + new URLSearchParams({ q, rows: "1000", page: String(page), output: "json", sort: "downloads desc" }) +
      ["identifier", "title", "creator", "year", "downloads", "format"].map((f) => "&fl[]=" + f).join("");
    let docs = [];
    for (let t = 0; t < 3 && !docs.length; t++) {
      try { const r = await fetch(url); if (r.ok) docs = (await r.json()).response.docs; else await sleep(4000); } catch { await sleep(4000); }
    }
    let n = 0;
    for (const d of docs) {
      const title = (Array.isArray(d.title) ? d.title[0] : d.title || "").replace(/\s+/g, " ").trim();
      const k = nk(title);
      if (!title || title.length < 5 || seen.has(k) || seenId.has(d.identifier) || BAD.test(title)) continue;
      const f = [].concat(d.format || []).join("|");
      const pdf = /PDF/i.test(f) ? 1 : 0, epub = /EPUB/i.test(f) ? 1 : 0;
      if (!pdf && !epub) continue;
      const c0 = [].concat(d.creator || [])[0] || "Unknown";
      if (OFF.test(String(c0)) || OFFT.test(title)) continue;
      const nm = String(c0).replace(/,\s*\d{3,4}.*$/, "").replace(/^(.*?),\s*(.*)$/, "$2 $1").replace(/\s+/g, " ").trim().slice(0, 60) || "Unknown";
      if (!nameIdx.has(nm)) { nameIdx.set(nm, names.length); names.push(nm); }
      seen.add(k); seenId.add(d.identifier);
      rows.push([nameIdx.get(nm), title.slice(0, 140), d.identifier, +String(d.year || 0).slice(0, 4) || 0, pdf + epub * 2]);
      n++;
    }
    console.log("subject pass", page, n);
    await sleep(1500);
    if (docs.length < 1000) break;
  }
}
// Verify the guessed download links; keep the item (its archive.org page always works) but drop dead PDF/EPUB flags.
const head = async (u) => { for (let t = 0; t < 2; t++) { try { const r = await fetch(u, { method: "HEAD", redirect: "follow" }); if (r.status === 404) return false; if (r.ok) return true; } catch {} await sleep(500); } return true; };
let bad = 0, idx = 0;
await Promise.all(Array.from({ length: 16 }, async () => {
  while (idx < rows.length) {
    const r = rows[idx++]; let f = r[4];
    if (f & 1 && !(await head(`https://archive.org/download/${r[2]}/${r[2]}.pdf`))) { f &= ~1; bad++; }
    if (f & 2 && !(await head(`https://archive.org/download/${r[2]}/${r[2]}.epub`))) { f &= ~2; bad++; }
    r[4] = f;
  }
}));
console.log("dead download links removed:", bad);
fs.writeFileSync("ia.json", JSON.stringify(reformedOnly(names, rows, true)));
console.log("total", rows.length);
