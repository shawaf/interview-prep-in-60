#!/usr/bin/env python3
"""Build the Vercel site from dsa-crash-course.html.

The source page is written in Claude-artifact format (body content only).
This script produces vercel-site/ with:

  index.html            full HTML document + Mermaid + service-worker registration
  sw.js                 offline cache (versioned by a hash of index.html)
  manifest.webmanifest  installable web app (PWA)
  icon.svg, icon-192.png, icon-512.png
  vercel.json           cache headers so updates roll out promptly

Usage:  python3 build.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "dsa-crash-course.html"
OUT = ROOT / "vercel-site"

FONTS_CSS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800"
             "&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap")
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"
ACCENT, DARK_BG = "#D97757", "#262624"

HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Interview prep in 60 minutes per subject: DSA, software engineering, distributed systems, senior track, AI engineering, mobile, frontend and behavioral rounds, with animations and practice tools. Works offline.">
<meta name="theme-color" content="{ACCENT}">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icon-192.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Prep in 60">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,-apple-system,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""

TAIL = f"""
<script src="{MERMAID}"></script>
<script>(function(){{var done=false,panel=document.getElementById('tab-crash');
function draw(){{if(done||!window.mermaid||!panel||panel.hidden||panel.closest('.subject').hidden)return;done=true;
  try{{mermaid.initialize({{startOnLoad:false,theme:matchMedia('(prefers-color-scheme: dark)').matches?'dark':'default'}});
    Promise.resolve(mermaid.run({{querySelector:'pre.mermaid'}})).catch(function(){{done=false;}});}}catch(e){{done=false;}}}}
new MutationObserver(draw).observe(document.body,{{subtree:true,attributes:true,attributeFilter:['hidden']}});draw();}})();</script>
<script>(function(){{
  var side=document.querySelector('.side .brand'),el=document.createElement('p');
  el.className='syncnote';el.id='net-status';if(side)side.insertAdjacentElement('afterend',el);
  function show(){{var off=!navigator.onLine,ready=!!(navigator.serviceWorker&&navigator.serviceWorker.controller);
    el.textContent=off?(ready?'● Offline: using the saved copy':'● Offline'):(ready?'✓ Available offline':'');}}
  addEventListener('online',show);addEventListener('offline',show);show();
  if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'||location.hostname==='127.0.0.1')){{
    addEventListener('load',function(){{navigator.serviceWorker.register('/sw.js').then(function(){{
      navigator.serviceWorker.ready.then(function(){{setTimeout(show,500);}});}}).catch(function(){{}});}});
    navigator.serviceWorker.addEventListener('controllerchange',show);}}
}})();</script>
</body>
</html>
"""

SW = """// Offline support: precache the app shell, then cache fonts/libraries as they're used.
const CACHE = 'prep60-__VERSION__';
const PRECACHE = ['/', '/manifest.webmanifest', '/icon.svg', '/icon-192.png', '/icon-512.png', '__MERMAID__', '__FONTS__'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(PRECACHE.map(u =>
    c.add(new Request(u, { mode: u.startsWith('/') ? 'same-origin' : 'no-cors' })).catch(() => null)))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('prep60-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
const CACHEABLE = /^(fonts\\.googleapis\\.com|fonts\\.gstatic\\.com|cdn\\.jsdelivr\\.net|cdnjs\\.cloudflare\\.com)$/;
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
"""

ICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
<rect width="512" height="512" rx="112" fill="{ACCENT}"/>
<text x="256" y="318" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="210" font-weight="800" fill="#fff">60</text>
<rect x="136" y="368" width="240" height="22" rx="11" fill="#fff" opacity=".85"/>
</svg>
"""


def png_icon(size: int, path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=ACCENT)
    font = None
    for name in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
                 "/System/Library/Fonts/Helvetica.ttc", "DejaVuSans-Bold.ttf"):
        try:
            font = ImageFont.truetype(name, int(size * 0.41))
            break
        except OSError:
            continue
    font = font or ImageFont.load_default()
    box = d.textbbox((0, 0), "60", font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((size - w) / 2 - box[0], size * 0.46 - h / 2 - box[1]), "60", font=font, fill="white")
    bw, bh = size * 0.47, size * 0.043
    d.rounded_rectangle([(size - bw) / 2, size * 0.72, (size + bw) / 2, size * 0.72 + bh], radius=bh / 2, fill=(255, 255, 255, 216))
    img.save(path)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    body = SRC.read_text(encoding="utf-8").strip("\n")
    html = HEAD + body + TAIL
    (OUT / "index.html").write_text(html, encoding="utf-8")
    version = hashlib.sha256(html.encode()).hexdigest()[:12]
    (OUT / "sw.js").write_text(SW.replace("__VERSION__", version).replace("__MERMAID__", MERMAID).replace("__FONTS__", FONTS_CSS), encoding="utf-8")
    manifest = {
        "name": "Interview Prep in 60", "short_name": "Prep in 60",
        "description": "Animated interview prep: DSA, SWE, distributed systems, senior, AI, mobile, frontend and behavioral.",
        "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": DARK_BG, "theme_color": ACCENT,
        "icons": [{"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml"},
                  {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
    }
    (OUT / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT / "icon.svg").write_text(ICON_SVG, encoding="utf-8")
    png_icon(192, OUT / "icon-192.png")
    png_icon(512, OUT / "icon-512.png")
    vercel = {"headers": [
        {"source": "/sw.js", "headers": [{"key": "Cache-Control", "value": "no-cache"},
                                          {"key": "Service-Worker-Allowed", "value": "/"}]},
        {"source": "/manifest.webmanifest", "headers": [{"key": "Content-Type", "value": "application/manifest+json"}]},
        {"source": "/", "headers": [{"key": "Cache-Control", "value": "no-cache"}]},
    ]}
    (OUT / "vercel.json").write_text(json.dumps(vercel, indent=2) + "\n", encoding="utf-8")
    print(f"wrote vercel-site/ (index.html {len(html):,} bytes, cache version {version})")


if __name__ == "__main__":
    main()
