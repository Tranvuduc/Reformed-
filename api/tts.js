export default async function handler(req, res) {
  const tl = req.query.tl === 'en' ? 'en' : 'vi';
  const q = String(req.query.q || '').slice(0, 200);
  if (q.trim().length < 1) return res.status(400).send('bad');
  const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=${tl}&q=${encodeURIComponent(q)}`;
  try {
    const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36', Referer: 'https://translate.google.com/' } });
    if (!r.ok) return res.status(502).send('upstream ' + r.status);
    const b = Buffer.from(await r.arrayBuffer());
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'public, s-maxage=2592000, max-age=86400');
    res.status(200).send(b);
  } catch (e) { res.status(502).send('error'); }
}
