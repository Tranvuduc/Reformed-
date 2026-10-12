const V = "rv-v3";
const OFFLINE = "rv-offline-v1"; // explicit user downloads (kept separate from auto cache)
const SHELL = ["/", "/index.html", "/style.css", "/app.js", "/reader.html", "/favicon.svg", "/manifest.webmanifest", "/lo-trinh.html", "/hom-nay.html"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(V).then((c) => Promise.allSettled(SHELL.map((u) => c.add(u)))).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== V && k !== "rv-books" && k !== OFFLINE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("message", (e) => {
  if (e.data === "skipWaiting") { self.skipWaiting(); return; }
  const d = e.data || {};
  if (d.type === "offline-dl" && d.url) {
    e.waitUntil(caches.open(OFFLINE).then((c) => fetch(d.url).then((r) => {
      if (!r.ok) throw new Error("bad");
      return c.put(d.url, r);
    })).then(() => (e.source && e.source.postMessage({ ok: 1, url: d.url })))
      .catch(() => (e.source && e.source.postMessage({ ok: 0, url: d.url }))));
  } else if (d.type === "offline-rm" && d.url) {
    e.waitUntil(caches.open(OFFLINE).then((c) => c.delete(d.url)).then(() => (e.source && e.source.postMessage({ ok: 1, url: d.url }))));
  } else if (d.type === "offline-has" && d.url) {
    e.waitUntil(caches.open(OFFLINE).then((c) => c.match(d.url)).then((m) => (e.source && e.source.postMessage({ ok: 1, url: d.url, has: !!m }))));
  }
});
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
  // Explicitly downloaded books (rv-offline-v1) are served first when present.
  e.respondWith((async () => {
    const c = await caches.open(store);
    const hit = await c.match(r, { ignoreSearch: false });
    let offHit = null;
    if (store === "rv-books") {
      try { offHit = await caches.open(OFFLINE).then((oc) => oc.match(r, { ignoreSearch: false })); } catch (e2) {}
    }
    const net = fetch(r).then((res) => {
      if (res.ok) {
        c.put(r, res.clone());
        if (store === "rv-books") caches.open(OFFLINE).then((oc) => oc.match(r, { ignoreSearch: false }).then((m) => { if (m) oc.put(r, res.clone()); }).catch(() => {}));
      }
      return res;
    }).catch(() => null);
    if (offHit) { e.waitUntil(net); return offHit; }
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || new Response("", { status: 504 });
  })());
});
