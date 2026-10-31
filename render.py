"""Render Ajaira Gyan static posts + carousels (1080x1350 PNG) from posts.json.
Usage: python3 render.py posts.json out_dir
"""
import json, sys, pathlib, asyncio
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "node_modules/@fontsource"
BN = "০১২৩৪৫৬৭৮৯"

def bn(n): return "".join(BN[int(d)] for d in str(n))

CSS = f"""
@font-face{{font-family:Anek;font-weight:800;src:url('file://{F}/anek-bangla/files/anek-bangla-bengali-800-normal.woff2')}}
@font-face{{font-family:Anek;font-weight:600;src:url('file://{F}/anek-bangla/files/anek-bangla-bengali-600-normal.woff2')}}
@font-face{{font-family:Hind;font-weight:400;src:url('file://{F}/hind-siliguri/files/hind-siliguri-bengali-400-normal.woff2')}}
@font-face{{font-family:Hind;font-weight:600;src:url('file://{F}/hind-siliguri/files/hind-siliguri-bengali-600-normal.woff2')}}
@font-face{{font-family:Hind;font-weight:700;src:url('file://{F}/hind-siliguri/files/hind-siliguri-bengali-700-normal.woff2')}}
@font-face{{font-family:Signika;font-weight:700;src:url('file://{F}/signika/files/signika-latin-700-normal.woff2')}}
@font-face{{font-family:Signika;font-weight:400;src:url('file://{F}/signika/files/signika-latin-400-normal.woff2')}}
:root{{--y:#FFC531;--k:#141414;--p:#FAF6EC}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:Hind,Signika,sans-serif;overflow:hidden}}
.c{{width:1080px;height:1350px;padding:90px 90px 80px;display:flex;flex-direction:column;position:relative}}
.paper{{background:var(--p);color:var(--k)}} .ink{{background:var(--k);color:var(--p)}} .yel{{background:var(--y);color:var(--k)}}
.tag{{align-self:flex-start;font:700 34px Hind;padding:10px 28px 6px;border-radius:999px;border:3px solid currentColor}}
.paper .tag{{background:var(--k);color:var(--y);border-color:var(--k)}}
.ink .tag{{background:var(--y);color:var(--k);border-color:var(--y)}}
.yel .tag{{background:var(--k);color:var(--y);border-color:var(--k)}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:44px}}
h1{{font:800 108px/1.38 Anek}} h1.s{{font-size:92px}}
mark{{background:var(--y);color:var(--k);padding:0 12px;border-radius:10px;line-height:1.1;white-space:nowrap;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.yel mark{{background:var(--k);color:var(--y)}}
p.b{{font:400 46px/1.55 Hind}} p.b b{{font-weight:700}}
.ink p.b b{{color:var(--y)}}
.foot{{font:600 36px/1.4 Hind;display:flex;align-items:center;gap:18px;padding-top:28px;border-top:3px solid currentColor}}
.brand{{display:flex;justify-content:space-between;align-items:center;margin-top:34px;font:700 30px Signika;opacity:.9}}
.brand .n{{font:700 34px Anek}}
.dot{{width:22px;height:22px;border-radius:50%;background:var(--y);display:inline-block;margin-right:12px;vertical-align:-2px}}
.yel .dot{{background:var(--k)}}
.blank{{display:inline-block;border-bottom:10px solid var(--k);width:260px;height:1px}}
.num{{align-self:flex-start;font:800 150px/1 Anek;color:var(--y);background:var(--k);border-radius:28px;padding:34px 46px 10px}}
.pg{{position:absolute;top:96px;right:90px;font:700 32px Signika}}
.arrow{{width:44px;height:44px}}
"""

ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DOWN = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'

def brand():
    return '<div class="brand"><span class="n"><span class="dot"></span>আজাইরা জ্ঞান</span><span>@ajaira.gyan</span></div>'

def page(cls, inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="c {cls}">{inner}</div></body></html>'

def build(p):
    t = p["template"]
    if t == "fact":
        return [page("paper", f'<div class="tag">{p["tag"]}</div><div class="mid"><h1>{p["headline"]}</h1><p class="b">{p["body"]}</p></div><div class="foot">{DOWN}{p["foot"]}</div>{brand()}')]
    if t == "tip":
        return [page("ink", f'<div class="tag">{p["tag"]}</div><div class="mid"><h1>{p["headline"]}</h1><p class="b">{p["body"]}</p></div><div class="foot">{p["foot"]}</div>{brand()}')]
    if t == "engage":
        h = p["headline"].replace("________", '<span class="blank"></span>')
        return [page("yel", f'<div class="tag">{p["tag"]}</div><div class="mid"><h1 class="s">{h}</h1><p class="b">{p["body"]}</p></div><div class="foot">{DOWN}{p["foot"]}</div>{brand()}')]
    if t == "carousel":
        n = len(p["slides"]) + 2
        out = [page("yel", f'<div class="tag">{p["tag"]}</div><div class="pg">{bn(1)}/{bn(n)}</div><div class="mid"><h1>{p["cover"]}</h1></div><div class="foot">{p["cover_sub"]}{ARROW}</div>{brand()}')]
        for i, (h, b) in enumerate(p["slides"], 1):
            out.append(page("paper", f'<div class="tag">{p["tag"]}</div><div class="pg">{bn(i+1)}/{bn(n)}</div><div class="mid" style="gap:30px"><div class="num">{bn(i)}</div><h1 class="s">{h}</h1><p class="b">{b}</p></div><div class="foot">সোয়াইপ করুন{ARROW}</div>{brand()}'))
        out.append(page("ink", f'<div class="tag">{p["tag"]}</div><div class="pg">{bn(n)}/{bn(n)}</div><div class="mid"><h1 class="s">{p["cta"]}</h1><p class="b">{p["cta_sub"]}</p></div>{brand()}'))
        return out
    raise ValueError(t)

async def main(src, out):
    data = json.loads(pathlib.Path(src).read_text())
    out = pathlib.Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for p in data["posts"]:
            for i, html in enumerate(build(p), 1):
                f = out / f'{data["date"]}_{p["id"]}' / f"{i:02d}.html"
                f.parent.mkdir(exist_ok=True); f.write_text(html)
                await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(150)
                await pg.screenshot(path=str(f.with_suffix(".png")))
                f.unlink()
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
