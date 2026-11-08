#!/usr/bin/env python3
"""Render SoloPro Sheets post images from a JSON spec.

Usage: python3 tools/render.py spec.json OUT_DIR

spec.json:
{
  "pin":    {"kicker": "Lash pricing", "title": "How to Price Lash Extensions So You Get Paid",
             "points": ["...", "...", "..."], "footer": "Free price calculator"},
  "slides": [{"title": "...", "body": "..."}, ... 5 items ...]
}

Writes OUT_DIR/pin.png (1000x1500) and OUT_DIR/slide-1.png ... (1080x1350).
Needs: pip-installed `playwright` with Chromium available.
"""
import json, sys, html, asyncio, pathlib

TEAL, MINT, AMBER, GROUND, INK, MUTED = "#0E3B3A", "#3BB98A", "#F5B83D", "#EEF8F2", "#0D2321", "#4D6B64"
LOGO = '<span class="logo">' + "<i></i>" * 9 + "</span>"
BASE = f"""*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,'Helvetica Neue',Arial,sans-serif;color:{INK}}}
.logo{{width:44px;height:44px;display:inline-grid;grid-template-columns:repeat(3,1fr);gap:3px;vertical-align:middle}}
.logo i{{background:{TEAL};border-radius:3px}}.logo i:nth-child(-n+3){{background:{MINT}}}.logo i:last-child{{background:{AMBER}}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:700;font-size:26px;color:{TEAL}}}"""

e = lambda s: html.escape(str(s or ""))


def pin_html(p):
    pts = "".join(f'<li><b>{i}</b><span>{e(t)}</span></li>' for i, t in enumerate(p.get("points", [])[:4], 1))
    return f"""<style>{BASE}
.page{{width:1000px;height:1500px;background:{GROUND};padding:90px 80px;display:flex;flex-direction:column;gap:48px}}
.k{{display:inline-block;background:{TEAL};color:#fff;font-weight:700;font-size:26px;padding:10px 22px;border-radius:999px;letter-spacing:.04em;text-transform:uppercase;align-self:flex-start}}
h1{{font-size:84px;line-height:1.04;letter-spacing:-2px;margin:0;color:{TEAL}}}
ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:26px}}
li{{display:flex;gap:24px;align-items:flex-start;background:#fff;border-radius:22px;padding:28px 30px;font-size:36px;line-height:1.3;border:2px solid #CFE0DA}}
li b{{flex:none;width:58px;height:58px;border-radius:50%;background:{AMBER};color:{TEAL};display:grid;place-items:center;font-size:32px}}
.f{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:30px;color:{MUTED}}}
.f strong{{color:{TEAL}}}</style>
<div class="page"><div class="brand">{LOGO}SoloPro Sheets</div><span class="k">{e(p.get('kicker'))}</span>
<h1>{e(p.get('title'))}</h1><ol>{pts}</ol>
<div class="f"><span>{e(p.get('footer') or 'Free price calculator')}</span><strong>payhip.com/soloprosheets</strong></div></div>"""


def slide_html(s, i, n):
    first = i == 1
    title_size = 92 if first else 64
    return f"""<style>{BASE}
.page{{width:1080px;height:1350px;background:{TEAL if first else GROUND};color:{'#fff' if first else INK};padding:96px 90px;display:flex;flex-direction:column;gap:44px}}
.brand{{color:{'#fff' if first else TEAL}}}
{'.logo i{background:#fff}' if first else ''}
.bar{{width:120px;height:14px;border-radius:7px;background:{AMBER};margin-top:auto}}
h1{{font-size:{title_size}px;line-height:1.05;letter-spacing:-2px;margin:0;color:{'#fff' if first else TEAL}}}
p{{font-size:{46 if first else 54}px;line-height:1.36;margin:0 0 auto;color:{'#CFEFE2' if first else INK};white-space:pre-line}}
.n{{display:flex;justify-content:space-between;font-size:30px;color:{'#9FD9C2' if first else MUTED}}}</style>
<div class="page"><div class="brand">{LOGO}SoloPro Sheets</div><span class="bar"></span><h1>{e(s.get('title'))}</h1><p>{e(s.get('body'))}</p>
<div class="n"><span>{'Swipe →' if i < n else 'Link in bio'}</span><span>{i}/{n}</span></div></div>"""


async def main(spec_path, out_dir):
    from playwright.async_api import async_playwright
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    written = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        if spec.get("pin"):
            pg = await b.new_page(viewport={"width": 1000, "height": 1500})
            await pg.set_content(pin_html(spec["pin"])); await pg.screenshot(path=str(out / "pin.png")); written.append("pin.png")
        slides = spec.get("slides") or []
        if slides:
            pg = await b.new_page(viewport={"width": 1080, "height": 1350})
            for i, s in enumerate(slides, 1):
                await pg.set_content(slide_html(s, i, len(slides))); fn = f"slide-{i}.png"
                await pg.screenshot(path=str(out / fn)); written.append(fn)
        await b.close()
    print(json.dumps(written))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2]))
