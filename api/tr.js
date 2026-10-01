import { put, get } from '@vercel/blob';
import { Readable } from 'node:stream';
const ID = /^[a-z0-9_-]{1,60}\/[a-z0-9_.-]{1,80}$/i, H = /^[a-z0-9]{4,16}$/;
const key = (id, h) => 'tr/' + id.replace('/', '__') + '/' + h + '.json';
async function body(req){
  if (req.body && typeof req.body === 'object') return req.body;
  let s=''; for await (const c of req) { s+=c; if (s.length>120000) throw new Error('big'); }
  return s ? JSON.parse(s) : {};
}
export default async function handler(req, res) {
  try {
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
      const b = await body(req);
      const id = String(b.id || ''), h = String(b.h || ''), t = b.t;
      if (!ID.test(id) || !H.test(h) || !Array.isArray(t) || !t.length || t.length > 400) return res.status(400).json({ error: 'bad' });
      let tot = 0;
      for (const x of t) { if (typeof x !== 'string' || !x.trim() || x.length > 6000) return res.status(400).json({ error: 'bad item' }); tot += x.length; }
      if (tot > 100000) return res.status(413).json({ error: 'big' });
      const k = key(id, h);
      const ex = await get(k, { access: 'private', useCache: false }).catch(() => null);
      if (ex && ex.statusCode === 200) return res.status(200).json({ ok: 1, kept: 1 }); // first write wins
      await put(k, JSON.stringify(t), { access: 'private', allowOverwrite: false, addRandomSuffix: false, contentType: 'application/json' });
      return res.status(200).json({ ok: 1 });
    }
    res.status(405).end();
  } catch (e) {
    res.status(500).json({ error: String(e && e.message || e) });
  }
}
