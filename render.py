"""Ajaira Gyan static posts + carousels, brand v2 (modern editorial, 31 Oct 2026).
Renders 1080x1350 PNGs from a posts JSON.
Usage: python3 render.py posts/<date>.json posts
Photos: photos/<date>_<id>/00.jpg (cover / single post) and 01.jpg..05.jpg (carousel slides).
"""
import json, sys, pathlib, asyncio
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "node_modules/@fontsource"
BN = "০১২৩৪৫৬৭৮৯"
def bn(n, w=2): return "".join(BN[int(d)] for d in str(n).zfill(w))

def font(fam, file, w, style="normal"):
    return f"@font-face{{font-family:{fam};font-weight:{w};font-style:{style};src:url('file://{F}/{file}')}}"

CSS = "".join([
    font("Serif", "noto-serif-bengali/files/noto-serif-bengali-bengali-700-normal.woff2", 700),
    font("Serif", "noto-serif-bengali/files/noto-serif-bengali-bengali-800-normal.woff2", 800),
    font("Ital", "tiro-bangla/files/tiro-bangla-bengali-400-italic.woff2", 400, "italic"),
    font("Hind", "hind-siliguri/files/hind-siliguri-bengali-400-normal.woff2", 400),
    font("Hind", "hind-siliguri/files/hind-siliguri-bengali-600-normal.woff2", 600),
    font("Anek", "anek-bangla/files/anek-bangla-bengali-700-normal.woff2", 700),
    font("DM", "dm-sans/files/dm-sans-latin-500-normal.woff2", 500),
    font("DM", "dm-sans/files/dm-sans-latin-700-normal.woff2", 700),
]) + """
:root{--y:#FFC531;--y2:#FF9F1C;--k:#141414;--k2:#1F1A12;--p:#FAF6EC;--m:#B9B2A3}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:Hind,DM,sans-serif;color:var(--p)}
.c{width:1080px;height:1350px;position:relative;overflow:hidden;
   background:radial-gradient(120% 70% at 50% 0%,#2A2113 0%,var(--k) 60%);}
.c.paper{background:var(--p);color:var(--k)}
.paper .label{color:#9A6B00}.paper .label:before,.paper .label:after{background:#9A6B00}
.grain{position:absolute;inset:0;opacity:.07;pointer-events:none;
   background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.top{position:absolute;top:64px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;z-index:3}
.logo{display:flex;align-items:center;gap:14px;font:700 32px Anek}
.logo i{width:40px;height:40px;border-radius:50%;background:var(--y);display:inline-block;position:relative}
.logo i:after{content:"";position:absolute;inset:11px;border-radius:50%;background:var(--k)}
.paper .logo i:after{background:var(--p)}
.kick{font:700 22px DM;letter-spacing:.32em;text-transform:uppercase;color:var(--y)}
.paper .kick{color:#9A6B00}
.label{font:600 30px Hind;color:var(--y);display:flex;align-items:center;justify-content:center;gap:22px}
.label:before,.label:after{content:"";width:70px;height:2px;background:var(--y);opacity:.7}
h1{font:800 104px/1.32 Serif;letter-spacing:-.01em}
h1.m{font-size:84px} h1.s{font-size:72px}
h1 em,h1 mark{font:italic 400 1.08em/1 Ital;color:var(--y);background:none;padding:0}
.paper h1 em,.paper h1 mark{color:#C27C00}
p.sub{font:400 38px/1.55 Hind,DM,sans-serif;color:var(--m)} p.sub b{color:var(--p);font-weight:600}
.paper p.sub{color:#5C5547} .paper p.sub b{color:var(--k)}
.foot{position:absolute;left:80px;right:80px;bottom:58px;display:flex;justify-content:space-between;align-items:center;font:500 24px DM;color:var(--m);z-index:3}
.pill{font:600 28px Hind;color:var(--k);background:var(--y);border-radius:999px;padding:12px 30px 8px;display:inline-flex;gap:12px;align-items:center}
.ph{position:absolute;overflow:hidden;border-radius:36px;box-shadow:0 30px 80px rgba(0,0,0,.55)}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.ph:after{content:"";position:absolute;inset:0;border-radius:36px;box-shadow:inset 0 0 0 2px rgba(255,197,49,.25)}
.full{position:absolute;inset:0}.full img{width:100%;height:100%;object-fit:cover}
.full:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,20,20,.55) 0%,rgba(20,20,20,0) 22%,rgba(20,20,20,.15) 45%,rgba(20,20,20,.92) 72%,var(--k) 100%)}
.num{position:absolute;right:80px;font:italic 400 220px/1 Ital;color:var(--y);opacity:.95;z-index:3;text-shadow:0 10px 40px rgba(0,0,0,.6)}
.center{text-align:center}
"""

ARROW = '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def em(s):  # allow <mark> from older posts; render as italic accent
    return s

def page(cls, inner):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="c {cls}">{inner}<div class="grain"></div></div></body></html>')

def top(kick):
    return f'<div class="top"><div class="logo"><i></i>আজাইরা জ্ঞান</div><div class="kick">{kick}</div></div>'

def foot(left, right="@ajaira.gyan"):
    return f'<div class="foot"><span>{left}</span><span>{right}</span></div>'

def img(path):
    return f"file://{path}" if path and pathlib.Path(path).exists() else None

def build(p, photos):
    t = p["template"]
    kick = p.get("kicker", "")
    if t == "carousel":
        n = len(p["slides"]) + 2
        cov = img(photos / "00.jpg")
        out = []
        bg = f'<div class="full"><img src="{cov}"></div>' if cov else ""
        out.append(page("", bg + top(kick) +
            f'<div style="position:absolute;left:80px;right:80px;bottom:150px;z-index:3">'
            f'<div class="label" style="justify-content:flex-start;margin-bottom:26px">{p["tag"]}</div>'
            f'<h1>{em(p["cover"])}</h1>'
            f'<div style="margin-top:34px" class="pill">{p["cover_sub"]}{ARROW}</div></div>'
            + foot(f'{bn(1)} / {bn(n)}')))
        for i, s in enumerate(p["slides"], 1):
            h, b = s[0], s[1]
            ph = img(photos / f"{i:02d}.jpg")
            pos = s[2] if len(s) > 2 else "center"
            photo = (f'<div class="ph" style="left:80px;right:80px;top:520px;height:700px">'
                     f'<img src="{ph}" style="object-position:{pos}"></div>') if ph else ""
            out.append(page("", top(kick) +
                f'<div class="center" style="position:absolute;left:80px;right:80px;top:170px;z-index:3">'
                f'<div class="label">{bn(i)} · {p["tag"]}</div>'
                f'<h1 class="m" style="margin-top:22px">{em(h)}</h1>'
                f'<p class="sub" style="margin-top:14px">{b}</p></div>'
                + photo + foot(f'{bn(i+1)} / {bn(n)}', "সোয়াইপ করুন →")))
        out.append(page("", bg.replace('class="full"', 'class="full" style="filter:blur(6px) brightness(.55)"') + top(kick) +
            f'<div class="center" style="position:absolute;left:80px;right:80px;top:50%;transform:translateY(-50%);z-index:3">'
            f'<div class="label">তাহলে বলুন</div>'
            f'<h1 class="m" style="margin-top:24px">{em(p["cta"])}</h1>'
            f'<p class="sub" style="margin-top:22px">{p["cta_sub"]}</p></div>'
            + foot(f'{bn(n)} / {bn(n)}')))
        return out
    # single posts: engage / fact / tip — optional photo at photos/<id>/00.jpg
    ph = img(photos / "00.jpg")
    cls = "paper" if t == "fact" else ""
    photo = (f'<div class="ph" style="left:80px;right:80px;bottom:150px;height:470px"><img src="{ph}" style="object-position:{p.get("photo_pos", "center")}"></div>') if ph else ""
    hcls = "m" if t == "engage" else ""
    return [page(cls, top(kick) +
        f'<div style="position:absolute;left:80px;right:80px;top:200px;z-index:3">'
        f'<div class="label" style="justify-content:flex-start">{p["tag"]}</div>'
        f'<h1 class="{hcls}" style="margin-top:22px">{em(p["headline"]).replace("________", "<em>______</em>")}</h1>'
        f'<p class="sub" style="margin-top:24px">{p["body"]}</p>'
        f'<div class="pill" style="margin-top:34px">{p["foot"]}</div></div>'
        + photo + foot(p.get("footer_left", "")))]

async def main(src, out):
    src = pathlib.Path(src).resolve()
    data = json.loads(src.read_text())
    out = pathlib.Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for p in data["posts"]:
            key = f'{data["date"]}_{p["id"]}'
            for i, html in enumerate(build(p, ROOT / "photos" / key), 1):
                f = out / key / f"{i:02d}.html"
                f.parent.mkdir(exist_ok=True); f.write_text(html)
                await pg.goto(f"file://{f}"); await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(200)
                await pg.screenshot(path=str(f.with_suffix(".png")))
                f.unlink()
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
