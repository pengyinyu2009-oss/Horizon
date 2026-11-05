/* Horizon App service worker: 数据与脚本 network-first（每日更新即时可见），
   图标等静态资源 cache-first，离线兜底缓存。版本号换版本即刷新。 */
const VER = "hz-app-v7";
const SHELL = [
  "./", "./index.html", "./style.css", "./app.js", "./manifest.webmanifest",
  "./data/lessons.json", "./icons/icon-192.png", "./icons/icon-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(origin_cache(VER)));
  self.skipWaiting();
});

function origin_cache(name) {
  return caches.open(name);
}

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) =>
    Promise.all(keys.filter((k) => k !== VER).map((k) => caches.delete(k))))
    .then(() => self.clients.matchAll()).then((cls) => {
      cls.forEach((c) => c.postMessage({ type: "SW_UPDATED", ver: VER }));
    }));
  self.clients.claim();
});

const NET_FIRST = [
  "/app/app.js", "/app/style.css", "/app/index.html", "/app/sw.js", "/app/",
];

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  if (!url.pathname.startsWith("/app/")) return;
  const netFirst = url.pathname.endsWith(".json") || NET_FIRST.includes(url.pathname);
  e.respondWith((async () => {
    const cachePut = (r) => {
      const copy = r.clone();
      caches.open(VER).then((c) => c.put(e.request, copy));
    };
    if (netFirst) {
      try {
        const r = await fetch(e.request);
        if (r.ok) cachePut(r);
        return r;
      } catch {
        return (await caches.match(e.request)) || Response.error();
      }
    }
    const cached = await caches.match(e.request);
    const fresh = fetch(e.request).then((r) => {
      if (r.ok) cachePut(r);
      return r;
    }).catch(() => cached);
    return cached || fresh;
  })());
});
