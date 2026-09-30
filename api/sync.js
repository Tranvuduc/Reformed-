import { put, get } from '@vercel/blob';
import { Readable } from 'node:stream';
const OK = /^[a-z0-9]{20,40}$/;
async function body(req){
  if (req.body && typeof req.body === 'object') return req.body;
  let s=''; for await (const c of req) { s+=c; if (s.length>300000) throw new Error('big'); }
  return s ? JSON.parse(s) : {};
}
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  try {
    if (req.method === 'GET') {
      const c = String(req.query.c || '');
      if (!OK.test(c)) return res.status(400).json({ error: 'bad code' });
      const r = await get('sync/' + c + '.json', { access: 'private', useCache: false });
      if (!r || r.statusCode !== 200) return res.status(200).json({ saved: [], prog: {} });
      res.setHeader('Content-Type', 'application/json');
      return Readable.fromWeb(r.stream).pipe(res);
    }
    if (req.method === 'POST') {
      const b = await body(req);
      if (!OK.test(String(b.c || '')) || !Array.isArray(b.saved) || typeof b.prog !== 'object' || !b.prog)
        return res.status(400).json({ error: 'bad data' });
      const data = JSON.stringify({ saved: b.saved.slice(0, 5000), prog: b.prog });
      if (data.length > 250000) return res.status(413).json({ error: 'too big' });
      await put('sync/' + b.c + '.json', data, { access: 'private', allowOverwrite: true, addRandomSuffix: false, contentType: 'application/json' });
      return res.status(200).json({ ok: true });
    }
    res.status(405).end();
  } catch (e) {
    res.status(500).json({ error: String(e && e.message || e) });
  }
}
