// Offline support: precache the app shell, then cache fonts/libraries as they're used.
const CACHE = 'prep60-d5df14c877ca';
const PRECACHE = ['/', '/manifest.webmanifest', '/icon.svg', '/icon-192.png', '/icon-512.png', 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js', 'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(PRECACHE.map(u =>
    c.add(new Request(u, { mode: u.startsWith('/') ? 'same-origin' : 'no-cors' })).catch(() => null)))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('prep60-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
const CACHEABLE = /^(fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)$/;
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {                       // pages: network first (fresh), cache when offline/slow
    e.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const res = await Promise.race([fetch(req), new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 4000))]);
        if (res && res.ok) cache.put('/', res.clone());
        return res;
      } catch (err) {
        return (await cache.match('/')) || Response.error();
      }
    })());
    return;
  }
  if (url.origin === location.origin || CACHEABLE.test(url.host)) {   // assets: cache first, refresh in background
    e.respondWith(caches.open(CACHE).then(async cache => {
      const hit = await cache.match(req);
      const net = fetch(req).then(res => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; })
        .catch(() => hit || Response.error());
      return hit || net;
    }));
  }
});
