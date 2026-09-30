const OK = /^[a-z0-9_-]+\/[a-z0-9_.-]+$/i;
export default async function handler(req, res) {
  const id = String(req.query.id || '');
  if (!OK.test(id)) return res.status(400).send('bad id');
  const [au, slug] = id.split('/');
  const url = `https://ccel.org/ccel/${au.charAt(0)}/${au}/${slug}/cache/${slug}.txt`;
  try {
    const r = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': 'ReformedVietnamReader/1.0' } });
    if (!r.ok) return res.status(404).send('not found');
    const t = await r.text();
    if (t.length > 12000000) return res.status(413).send('too big');
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=604800, stale-while-revalidate=86400');
    res.status(200).send(t);
  } catch (e) { res.status(502).send('upstream error'); }
}
