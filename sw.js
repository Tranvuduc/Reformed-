const V = "rv-v3";
const SHELL = ["/", "/index.html", "/style.css", "/app.js", "/reader.html", "/favicon.svg", "/manifest.webmanifest", "/lo-trinh.html", "/hom-nay.html"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(V).then((c) => Promise.allSettled(SHELL.map((u) => c.add(u)))).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V && k !== "rv-books").map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("message", (e) => { if (e.data === "skipWaiting") self.skipWaiting(); });
const NETONLY = /\/api\/(sync|tr|tts)/;
self.addEventListener("fetch", (e) => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin !== location.origin || NETONLY.test(u.pathname)) return;
  const store = /\/api\/text|^\/txt\//.test(u.pathname) ? "rv-books" : V;
  // Navigations: network-first so new deploys show immediately; fall back to cache offline.
  if (r.mode === "navigate") {
    e.respondWith(fetch(r).then((res) => { if (res.ok) { const k = res.clone(); caches.open(store).then((c) => c.put(r, k)); } return res; })
      .catch(async () => (await caches.match(r)) || (await caches.match("/index.html"))));
    return;
  }
  // Static assets, JSON, book text: stale-while-revalidate — instant load, refresh in background.
  e.respondWith(caches.open(store).then(async (c) => {
    const hit = await c.match(r, { ignoreSearch: false });
    const net = fetch(r).then((res) => { if (res.ok) c.put(r, res.clone()); return res; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response("", { status: 504 });
  }));
});
