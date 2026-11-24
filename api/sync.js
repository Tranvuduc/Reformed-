import { put, get } from '@vercel/blob';
import { Readable } from 'node:stream';
const OK = /^[a-z0-9]{20,40}$/;
const MAX_PROG_KEYS = 5000;
const MAX_SAVED = 5000;
async function body(req){
  if (req.body && typeof req.body === 'object') return req.body;
  let s=''; for await (const c of req) { s+=c; if (s.length>700000) throw new Error('big'); }
  return s ? JSON.parse(s) : {};
}
// A missing blob (first sync for this code) is a legitimate empty state, not a
// failure. Anything else that keeps us from reading storage is reported as 503
// so the client never mistakes "storage unavailable" for "user has no data".
function isNotFound(e){
  if (!e) return false;
  if (e.statusCode === 404 || e.status === 404) return true;
  if (e.name === 'BlobNotFoundError') return true;
  return /not found/i.test(String(e.message || ''));
}
function unavailable(res){ res.setHeader('Retry-After', '30'); return res.status(503).json({ error: 'unavailable' }); }
// Validate + sanitise the progress map: plain object, bounded keys, values are
// {s?: string, p?: 0..100, t?: number} only. Unknown fields are dropped.
function cleanProg(p){
  if (typeof p !== 'object' || !p || Array.isArray(p)) return null;
  const keys = Object.keys(p);
  if (keys.length > MAX_PROG_KEYS) return null;
  const out = {};
  for (const k of keys){
    if (typeof k !== 'string' || k.length > 200) return null;
    const v = p[k];
    if (typeof v !== 'object' || !v || Array.isArray(v)) return null;
    const o = {};
    if (v.s !== undefined){ if (typeof v.s !== 'string') return null; o.s = v.s.slice(0, 20); }
    if (v.p !== undefined){ if (typeof v.p !== 'number' || !isFinite(v.p)) return null; o.p = Math.max(0, Math.min(100, v.p)); }
    if (v.t !== undefined){ if (typeof v.t !== 'number' || !isFinite(v.t) || v.t < 0) return null; o.t = v.t; }
    out[k] = o;
  }
  return out;
}
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    if (req.method === 'GET') {
      const c = String(req.query.c || '');
      if (!OK.test(c)) return res.status(400).json({ error: 'bad code' });
      let r;
      try {
        r = await get('sync/' + c + '.json', { access: 'private', useCache: false });
      } catch (e) {
        if (isNotFound(e)) return res.status(200).json({ saved: [], prog: {}, hl: {}, empty: true });
        return unavailable(res);
      }
      if (!r) return res.status(200).json({ saved: [], prog: {}, hl: {}, empty: true });
      if (r.statusCode === 404) return res.status(200).json({ saved: [], prog: {}, hl: {}, empty: true });
      if (r.statusCode !== 200) return unavailable(res);
      res.setHeader('Content-Type', 'application/json');
      return Readable.fromWeb(r.stream).pipe(res);
    }
    if (req.method === 'POST') {
      let b;
      try { b = await body(req); } catch (e) {
        return res.status(e && e.message === 'big' ? 413 : 400).json({ error: e && e.message === 'big' ? 'too big' : 'bad data' });
      }
      if (!OK.test(String(b.c || '')) || !Array.isArray(b.saved))
        return res.status(400).json({ error: 'bad data' });
      const prog = cleanProg(b.prog);
      if (prog === null) return res.status(400).json({ error: 'bad data' });
      const saved = b.saved.filter(function (x) { return typeof x === 'string' && x.length > 0 && x.length <= 200; }).slice(0, MAX_SAVED);
      let hl = {};
      if (b.hl && typeof b.hl === 'object' && !Array.isArray(b.hl)) {
        for (const k of Object.keys(b.hl).slice(0, 300)) {
          if (!/^[a-z0-9_-]+\/[a-z0-9_.-]+$/i.test(k) || !Array.isArray(b.hl[k])) continue;
          hl[k] = b.hl[k].slice(0, 1000).filter(h => h && Number.isInteger(h.g)).map(h => ({ g: h.g, q: String(h.q || '').slice(0, 200), c: h.c | 0, n: String(h.n || '').slice(0, 2000), d: h.d ? 1 : 0, t: +h.t || 0 }));
        }
      }
      const data = JSON.stringify({ saved: saved, prog: prog, hl });
      if (data.length > 600000) return res.status(413).json({ error: 'too big' });
      try {
        await put('sync/' + b.c + '.json', data, { access: 'private', allowOverwrite: true, addRandomSuffix: false, contentType: 'application/json' });
      } catch (e) {
        // Storage failed: never claim success for a write that was not persisted.
        // The client shows a calm "not synced yet, will retry" state and retries
        // with backoff; local progress in the browser is unaffected.
        return unavailable(res);
      }
      return res.status(200).json({ ok: true });
    }
    res.status(405).end();
  } catch (e) {
    // Unexpected failure: 503, never a false success.
    return unavailable(res);
  }
}
