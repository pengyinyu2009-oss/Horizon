/* Horizon App service worker: app-shell cache-first, 版本号换版本即刷新 */
const VER = "hz-app-v2";
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
    Promise.all(keys.filter((k) => k !== VER).map((k) => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  if (!url.pathname.startsWith("/app/")) return;
  e.respondWith((async () => {
    const cached = await caches.match(e.request);
    const fresh = fetch(e.request).then((r) => {
      if (r.ok) {
        const copy = r.clone();
        caches.open(VER).then((c) => c.put(e.request, copy));
      }
      return r;
    }).catch(() => cached);
    return cached || fresh;
  })());
});
