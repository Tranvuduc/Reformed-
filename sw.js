const V = "rv-v1";
const SHELL = ["/", "/index.html", "/style.css", "/app.js", "/reader.html", "/favicon.svg", "/manifest.webmanifest", "/lo-trinh.html", "/hom-nay.html"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(V).then((c) => Promise.allSettled(SHELL.map((u) => c.add(u)))).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V && k !== "rv-books").map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
const NETONLY = /\/api\/(sync|tr)/;
self.addEventListener("fetch", (e) => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin !== location.origin || NETONLY.test(u.pathname)) return;
  // books text: cache for offline reading, refresh in background
  const store = /\/api\/text/.test(u.pathname) ? "rv-books" : V;
  e.respondWith(caches.open(store).then(async (c) => {
    const hit = await c.match(r, { ignoreSearch: false });
    const net = fetch(r).then((res) => { if (res.ok) c.put(r, res.clone()); return res; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    const res = await net;
    if (res) return res;
    if (r.mode === "navigate") return (await caches.match("/index.html")) || new Response("Offline", { status: 503 });
    return new Response("", { status: 504 });
  }));
});
