#!/usr/bin/env python3
"""Build vercel-site/index.html from dsa-crash-course.html.

The source page is written in Claude-artifact format (body content only).
This wraps it in a full HTML document and adds Mermaid, which claude.ai
renders natively but a plain static host does not.

Usage:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "dsa-crash-course.html"
OUT = ROOT / "vercel-site" / "index.html"

HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Interview prep in 60 minutes per subject: DSA, software engineering, distributed systems, senior track, AI engineering, mobile and behavioral rounds, with animations and practice tools.">\n<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'

TAIL = '\n<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>\n<script>(function(){var done=false,panel=document.getElementById(\'tab-crash\');\nfunction draw(){if(done||!window.mermaid||!panel||panel.hidden||panel.closest(\'.subject\').hidden)return;done=true;\n  try{mermaid.initialize({startOnLoad:false,theme:matchMedia(\'(prefers-color-scheme: dark)\').matches?\'dark\':\'default\'});\n    Promise.resolve(mermaid.run({querySelector:\'pre.mermaid\'})).catch(function(){done=false;});}catch(e){done=false;}}\nnew MutationObserver(draw).observe(document.body,{subtree:true,attributes:true,attributeFilter:[\'hidden\']});draw();})();</script>\n</body>\n</html>\n'


def main() -> None:
    body = SRC.read_text(encoding="utf-8").strip("\n")
    OUT.write_text(HEAD + body + TAIL, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
