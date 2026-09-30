// Builds dg.json: Desiring God books that really offer free PDF/EPUB downloads (verified by request).
// Needs network. Run by .github/workflows/dg.yml.
import fs from "node:fs";
const SLUGS = ["12-ways-your-phone-is-changing-you", "27-servants-of-sovereign-joy", "50-crucial-questions-about-manhood-and-womanhood", "acting-the-miracle", "adoniram-judson", "alive-to-wonder", "an-all-consuming-passion-for-jesus", "all-that-jesus-commanded", "amazing-grace-in-the-life-of-william-wilberforce", "andrew-fuller", "ask-pastor-john", "astonished-by-god", "battling-unbelief", "beyond-the-bounds", "bloodlines", "brothers-we-are-not-professionals", "a-camaraderie-of-confidence", "captive-to-glory", "charles-spurgeon", "the-christmas-we-didnt-expect", "the-collected-works-of-john-piper", "come-lord-jesus", "competing-spectacles", "contending-for-our-all", "coronavirus-and-christ", "counted-righteous-in-christ", "cross", "the-dangerous-duty-of-delight", "david-brainerd", "the-dawning-of-indestructible-joy", "designed-for-joy", "desiring-god", "disability-and-the-sovereign-goodness-of-god", "do-you-want-a-friend", "does-god-desire-all-to-be-saved", "dont-follow-your-heart", "dont-waste-your-cancer", "dont-waste-your-life", "esther", "exposing-the-dark-work-of-abortion", "expository-exultation", "faithful-women-and-their-extraordinary-god", "fifty-reasons-why-jesus-came-to-die", "filling-up-the-afflictions-of-christ", "finally-alive", "finish-the-mission", "five-points", "for-your-joy", "for-the-fame-of-gods-name", "foundations-for-lifelong-learning", "the-future-of-justification", "future-grace", "a-god-entranced-vision-of-all-things", "god-is-the-gospel", "god-technology-and-the-christian-life", "gods-passion-for-his-glory", "a-godward-heart", "a-godward-life", "good-news-of-great-joy", "habits-of-grace", "habits-of-grace-study-guide", "happily-ever-after", "a-holy-ambition", "how-to-stay-christian-in-seminary", "humbled", "a-hunger-for-god", "in-our-joy", "the-innkeeper", "jesus-the-only-way-to-god", "john-calvin-and-his-passion-for-the-majesty-of-god", "john-g-paton", "jonathan-edwards", "the-joy-project", "the-justification-of-god", "killjoys", "the-legacy-of-sovereign-joy", "lessons-from-a-hospital-bed", "let-the-nations-be-glad", "life-as-a-vapor", "lit", "a-little-theology-of-exercise", "living-in-the-light", "love-your-enemies", "love-to-the-uttermost", "the-marks-of-a-spiritual-leader", "martin-luther", "the-misery-of-job-and-the-mercy-of-god", "mom-enough", "most-of-all-jesus-loves-you", "newton-on-the-christian-life", "not-yet-married", "not-by-sight", "the-pastor-as-scholar-and-the-scholar-as-pastor", "a-peculiar-glory", "pierced-by-the-word", "the-pilgrims-progress", "the-pleasures-of-god", "portrait-of-calvin", "the-power-of-words-and-the-wonder-of-god", "preparing-for-marriage", "the-prodigals-sister", "providence", "reading-the-bible-supernaturally", "recovering-biblical-manhood-and-womanhood", "rethinking-retirement", "rich-wounds", "risk-is-right", "the-romantic-rationalist", "the-roots-of-endurance", "ruth-under-the-wings-of-god", "sanctification-in-the-everyday", "the-satisfied-soul", "the-scars-that-have-shaped-me", "seeing-beauty-and-saying-beautifully", "seeing-and-savoring-jesus-christ", "sex-race-and-the-sovereignty-of-god", "sex-and-the-supremacy-of-christ", "shaped-by-god", "spectacular-sins", "stand", "still-not-professionals", "suffering-and-the-sovereignty-of-god", "the-supremacy-of-christ-in-a-postmodern-world", "the-supremacy-of-god-in-preaching", "take-care-how-you-listen", "taste-and-see", "things-not-seen", "think", "think-it-not-strange", "thinking-loving-doing", "this-momentary-marriage", "treasuring-god-in-our-traditions", "a-tribute-to-my-father", "true-to-his-word", "velvet-steel", "what-is-saving-faith", "whats-the-difference", "when-i-dont-desire-god", "when-the-darkness-will-not-lift", "why-i-love-the-apostle-paul", "with-calvin-in-the-theater-of-god", "workers-for-your-joy", "your-sorrow-will-turn-to-joy"];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const H = { "User-Agent": "reformed-vietnam-catalog (reformedvn@gmail.com)" };
async function ok(url) {
  try {
    const r = await fetch(url, { headers: { ...H, Range: "bytes=0-0" }, redirect: "follow", signal: AbortSignal.timeout(25000) });
    const ct = r.headers.get("content-type") || "";
    try { await r.body?.cancel(); } catch {}
    return (r.status === 200 || r.status === 206) && /pdf|epub|zip|octet/i.test(ct);
  } catch { return false; }
}
const dec = (s) => s.replace(/&amp;/g, "&").replace(/&#0?39;|&rsquo;|&#8217;/g, "'").replace(/&quot;/g, '"').replace(/&#8211;|&ndash;/g, "-").replace(/&[a-z#0-9]+;/g, " ").trim();
const names = [], rows = [];
for (const slug of SLUGS) {
  const base = "https://www.desiringgod.org/books/" + slug;
  const pdf = await ok(base + ".pdf"), epub = await ok(base + ".epub");
  if (!pdf && !epub) { console.log("not free", slug); await sleep(300); continue; }
  let title = slug.replace(/-/g, " "), author = "Desiring God";
  try {
    const h = await (await fetch(base, { headers: H, signal: AbortSignal.timeout(25000) })).text();
    const t = h.match(/<meta property="og:title" content="([^"]+)"/i) || h.match(/<title>([^<|]+)/i);
    if (t) title = dec(t[1]).replace(/\s*[|\u2013-]\s*Desiring God.*$/i, "");
    const a = h.match(/href="\/authors\/[a-z0-9-]+"[^>]*>\s*([^<]{3,40})</i);
    if (a) author = dec(a[1]);
  } catch {}
  let ai = names.indexOf(author); if (ai < 0) { ai = names.length; names.push(author); }
  rows.push([ai, title.slice(0, 140), slug, (pdf ? 1 : 0) + (epub ? 2 : 0)]);
  console.log("free", slug, author);
  await sleep(400);
}
fs.writeFileSync("dg.json", JSON.stringify({ a: names, b: rows }));
console.log("total", rows.length);
