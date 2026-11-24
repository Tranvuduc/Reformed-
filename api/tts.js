// TTS proxy (Google Translate TTS). GET only, short upstream timeout, and a
// per-instance per-IP brake (120 req/hour). The brake is honest about its
// limits: Vercel serverless runs many instances with separate memory, so it
// is a spam brake, not a global quota — the real guards are the 200-char cap
// and the 30-day edge cache below.
const UPSTREAM_TIMEOUT_MS = 8000;
const TTS_PER_HOUR = 120;
const _hits = new Map(); // ip -> [timestampMs, ...]
function ipOf(req){
  const f = String((req.headers && (req.headers['x-forwarded-for'] || req.headers['x-real-ip'])) || '');
  return (f.split(',')[0] || 'unknown').trim().slice(0, 64);
}
function limited(ip){
  const now = Date.now(), arr = (_hits.get(ip) || []).filter(t => now - t < 3600000);
  if (arr.length >= TTS_PER_HOUR) return true;
  arr.push(now); _hits.set(ip, arr);
  if (_hits.size > 5000) { const k = _hits.keys().next().value; _hits.delete(k); }
  return false;
}
export default async function handler(req, res) {
  if (req.method !== 'GET') { res.setHeader('Allow', 'GET'); return res.status(405).end(); }
  if (limited(ipOf(req))) { res.setHeader('Retry-After', '3600'); return res.status(429).send('too many requests'); }
  const tl = req.query.tl === 'en' ? 'en' : 'vi';
  const q = String(req.query.q || '').slice(0, 200);
  if (q.trim().length < 1) return res.status(400).send('bad');
  const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=${tl}&q=${encodeURIComponent(q)}`;
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), UPSTREAM_TIMEOUT_MS);
  try {
    const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36', Referer: 'https://translate.google.com/' }, signal: ctl.signal });
    if (!r.ok) return res.status(502).send('upstream ' + r.status);
    const b = Buffer.from(await r.arrayBuffer());
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'public, s-maxage=2592000, max-age=86400');
    res.status(200).send(b);
  } catch (e) { res.status(502).send('error'); }
  finally { clearTimeout(timer); }
}
