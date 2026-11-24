// Shared machine-translation cache (Vercel Blob) for reader.html.
//
// SECURITY MODEL (Quality & Reliability 1.0, P0 fix):
// The old code let any client POST {id,h,t} and store ARBITRARY text as the
// cached "translation" of any book/segment (first-write-wins, so the poison
// could never be overwritten). That is now closed. The client never sends
// translation text to this endpoint any more; it sends only the SOURCE
// paragraphs {id,h,src}, and the SERVER:
//   1. checks h == hsh(src) (same hash the reader uses),
//   2. fetches the canonical source text itself (CCEL, same URL as api/text.js)
//      and verifies the source paragraphs really come from that book
//      (whitespace-normalised substring check),
//   3. translates the verified source itself with the same free providers the
//      reader uses (Google gtx, then MyMemory fallback),
//   4. caches ONLY that server-produced translation, first-write-wins.
// An attacker can at most ask the server to (re)translate genuine source
// text; they can never choose the cached text. The reader's display is
// unaffected when this fails: it already has its own local translation.
// Bot/admin writes (status reports, and direct cache writes used to correct a
// poisoned entry) require Authorization: Bearer <TR_WRITE_TOKEN> (Vercel env
// var, never shipped to the browser). If the env var is unset those branches
// answer 503, i.e. fail closed. GET stays public: reading the cache is the
// point of it.
// POST has a per-instance per-IP brake (120/hour). Like api/chat.js, this is
// honest about its limits: serverless runs many instances with separate
// memory, so it is a spam brake, not a global quota.
import { put, get, list } from '@vercel/blob';
import { Readable } from 'node:stream';
const ID = /^[a-z0-9_-]{1,60}\/[a-z0-9_.-]{1,80}$/i, H = /^[a-z0-9]{4,16}$/;
const key = (id, h) => 'tr/' + id.replace('/', '__') + '/' + h + '.json';
const MAX_SRC_TOTAL = 12000;   // reader pages are <= ~4200 chars; bound server work
const MAX_SRC_ITEMS = 400;
const CCEL_TIMEOUT_MS = 6000;
const TR_TIMEOUT_MS = 8000;    // per translation chunk
const POST_PER_HOUR = 120;
const _hits = new Map(); // ip -> [timestampMs, ...]
function ipOf(req) {
  const f = String((req.headers && (req.headers['x-forwarded-for'] || req.headers['x-real-ip'])) || '');
  return (f.split(',')[0] || 'unknown').trim().slice(0, 64);
}
function limited(ip) {
  const now = Date.now(), arr = (_hits.get(ip) || []).filter(t => now - t < 3600000);
  if (arr.length >= POST_PER_HOUR) return true;
  arr.push(now); _hits.set(ip, arr);
  if (_hits.size > 5000) { const k = _hits.keys().next().value; _hits.delete(k); }
  return false;
}
function authed(req) {
  const tok = process.env.TR_WRITE_TOKEN;
  if (!tok) return false;
  const h = String((req.headers && (req.headers.authorization || req.headers.Authorization)) || '');
  return h === 'Bearer ' + tok;
}
// Same hash as reader.html hsh(): djb2 over src.join("\n").
function hsh(a) {
  var s = a.join("\n"), h = 5381, h2 = 0;
  for (var k = 0; k < s.length; k++) { h = ((h << 5) + h + s.charCodeAt(k)) >>> 0; h2 = (h2 * 31 + s.charCodeAt(k)) >>> 0; }
  return h.toString(36) + h2.toString(36);
}
// Same chunker as reader.html splitC(): split into <=max sentence pieces.
function splitC(t, max) {
  var out = [], c = "";
  t.split(/(?<=[.!?])\s+(?=[A-Z"“‘(\d])/).forEach(function (x) {
    while (x.length > max) { if (c) { out.push(c); c = ""; } var k = x.lastIndexOf(" ", max); if (k < 200) k = max; out.push(x.slice(0, k)); x = x.slice(k).trim(); }
    if (c && c.length + x.length + 1 > max) { out.push(c); c = ""; }
    c += (c ? " " : "") + x;
  });
  if (c) out.push(c);
  return out;
}
async function body(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let s = ''; for await (const c of req) { s += c; if (s.length > 120000) { const e = new Error('big'); e.status = 413; throw e; } }
  return s ? JSON.parse(s) : {};
}
function norm(s) { return String(s).replace(/\s+/g, ' ').trim(); }
async function fetchCanonical(id) {
  const [au, slug] = id.split('/');
  const url = `https://ccel.org/ccel/${au.charAt(0)}/${au}/${slug}/cache/${slug}.txt`;
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), CCEL_TIMEOUT_MS);
  try {
    const r = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': 'ReformedVietnamReader/1.0' }, signal: ctl.signal });
    if (!r.ok) return null;
    const t = await r.text();
    if (t.length > 12000000) return null;
    return t;
  } catch (e) { return null; }
  finally { clearTimeout(timer); }
}
function srcVerified(src, canonical) {
  const can = norm(canonical);
  if (!can) return false;
  const joined = norm(src.join(' '));
  if (joined.length > 20 && can.includes(joined)) return true;
  const long = src.map(norm).filter(x => x.length >= 30);
  if (!long.length) return joined.length > 0 && can.includes(joined);
  let hit = 0;
  for (const x of long) if (can.includes(x)) hit++;
  return hit >= 1 && hit / long.length >= 0.8;
}
async function gtx(chunk) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), TR_TIMEOUT_MS);
  try {
    const r = await fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + encodeURIComponent(chunk), { signal: ctl.signal });
    if (!r.ok) return null;
    const j = await r.json();
    const o = (j[0] || []).map(function (x) { return x[0]; }).join('');
    return o ? o : null;
  } catch (e) { return null; }
  finally { clearTimeout(timer); }
}
async function myMemory(chunk) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), TR_TIMEOUT_MS);
  try {
    const r = await fetch('https://api.mymemory.translated.net/get?langpair=en|vi&q=' + encodeURIComponent(chunk.slice(0, 480)), { signal: ctl.signal });
    if (!r.ok) return null;
    const j = await r.json();
    if (j.responseStatus != 200) return null;
    return j.responseData && j.responseData.translatedText ? j.responseData.translatedText : null;
  } catch (e) { return null; }
  finally { clearTimeout(timer); }
}
async function translateChunk(chunk) {
  return (await gtx(chunk)) || (await myMemory(chunk));
}
async function translateSrc(src) {
  // Concurrency 3, like the reader's getTr2; whole job bounded by a deadline.
  const jobs = [];
  for (const p of src) for (const ch of splitC(p, 1400)) jobs.push(ch);
  const out = new Array(jobs.length);
  let next = 0;
  async function worker() {
    while (next < jobs.length) {
      const k = next++;
      const v = await translateChunk(jobs[k]);
      if (!v) throw new Error('no translator');
      out[k] = v;
    }
  }
  const done = Promise.all([worker(), worker(), worker()]);
  const timeout = new Promise((_, rej) => setTimeout(() => rej(new Error('deadline')), 9000));
  await Promise.race([done, timeout]);
  // Reassemble per paragraph (chunks were joined with " ", like the reader).
  const res = [];
  let i = 0;
  for (const p of src) { const n = splitC(p, 1400).length; res.push(out.slice(i, i + n).join(' ')); i += n; }
  return res;
}
export default async function handler(req, res) {
  try {
    if (req.method === 'GET' && req.query.stats) {
      const st = {}; try { const r0 = await list({ prefix: 'status/', limit: 50 }); for (const b of r0.blobs) { const g = await get(b.pathname, { access: 'private', useCache: false }); if (g && g.statusCode === 200) st[b.pathname.slice(7, -5)] = await new Response(g.stream).text(); } } catch (e) {}
      // Không còn liệt kê toàn bộ blob tr/ (tốn nhiều thao tác Blob nâng cao); chỉ trả trạng thái bot.
      res.setHeader('Cache-Control', 'public, s-maxage=3600');
      return res.status(200).json({ status: st });
    }
    if (req.method === 'GET') {
      const id = String(req.query.id || ''), h = String(req.query.h || '');
      if (!ID.test(id) || !H.test(h)) return res.status(400).json({ error: 'bad' });
      const r = await get(key(id, h), { access: 'private', useCache: false });
      if (!r || r.statusCode !== 200) { res.setHeader('Cache-Control', 'no-store'); return res.status(404).json({ miss: 1 }); }
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Cache-Control', 'public, s-maxage=86400, max-age=3600');
      return Readable.fromWeb(r.stream).pipe(res);
    }
    if (req.method === 'POST') {
      res.setHeader('Cache-Control', 'no-store');
      if (limited(ipOf(req))) { res.setHeader('Retry-After', '3600'); return res.status(429).json({ error: 'too many requests' }); }
      const b = await body(req);
      // --- admin/bot branch: bearer token required (TR_WRITE_TOKEN env var) ---
      if (b.status || b.overwrite) {
        if (!authed(req)) return res.status(process.env.TR_WRITE_TOKEN ? 401 : 503).json({ error: process.env.TR_WRITE_TOKEN ? 'unauthorized' : 'not_ready' });
        if (b.status && /^[a-z0-9-]{2,20}$/.test(String(b.status.bot || ''))) {
          await put('status/' + b.status.bot + '.json', JSON.stringify({ t: new Date().toISOString(), msg: String(b.status.msg || '').slice(0, 1500) }), { access: 'private', allowOverwrite: true, addRandomSuffix: false, contentType: 'application/json' });
          return res.status(200).json({ ok: 1 });
        }
        if (b.overwrite) {
          const id = String(b.id || ''), h = String(b.h || ''), t = b.t;
          if (!ID.test(id) || !H.test(h) || !Array.isArray(t) || !t.length || t.length > 400) return res.status(400).json({ error: 'bad' });
          let tot = 0;
          for (const x of t) { if (typeof x !== 'string' || !x.trim() || x.length > 6000) return res.status(400).json({ error: 'bad item' }); tot += x.length; }
          if (tot > 100000) return res.status(413).json({ error: 'big' });
          await put(key(id, h), JSON.stringify(t), { access: 'private', allowOverwrite: true, addRandomSuffix: false, contentType: 'application/json' });
          return res.status(200).json({ ok: 1 });
        }
        return res.status(400).json({ error: 'bad' });
      }
      // --- reader branch: client sends SOURCE only; server translates + caches ---
      const id = String(b.id || ''), h = String(b.h || ''), src = b.src;
      if (!ID.test(id) || !H.test(h) || !Array.isArray(src) || !src.length || src.length > MAX_SRC_ITEMS) return res.status(400).json({ error: 'bad' });
      if (id.indexOf('vn/') === 0) return res.status(400).json({ error: 'not translatable' });
      let tot = 0;
      for (const x of src) { if (typeof x !== 'string' || !x.trim() || x.length > 6000) return res.status(400).json({ error: 'bad item' }); tot += x.length; }
      if (tot > MAX_SRC_TOTAL) return res.status(413).json({ error: 'big' });
      if (hsh(src) !== h) return res.status(400).json({ error: 'bad hash' });
      const canonical = await fetchCanonical(id);
      if (!canonical) return res.status(502).json({ error: 'source unavailable' });
      if (!srcVerified(src, canonical)) return res.status(400).json({ error: 'source mismatch' });
      const k = key(id, h);
      const ex = await get(k, { access: 'private', useCache: false }).catch(() => null);
      if (ex && ex.statusCode === 200) return res.status(200).json({ ok: 1, kept: 1 }); // first write wins
      let t;
      try { t = await translateSrc(src); }
      catch (e) { return res.status(502).json({ error: 'translate failed' }); }
      try {
        await put(k, JSON.stringify(t), { access: 'private', allowOverwrite: false, addRandomSuffix: false, contentType: 'application/json' });
      } catch (e) { return res.status(200).json({ ok: 1, kept: 1 }); } // lost the race: first write wins
      return res.status(200).json({ ok: 1 });
    }
    res.status(405).end();
  } catch (e) {
    if (e && e.status) return res.status(e.status).json({ error: 'error' });
    res.status(500).json({ error: 'error' });
  }
}
