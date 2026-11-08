#!/usr/bin/env python3
"""Render SoloPro Sheets post images from a JSON spec (free, local: HTML/CSS -> PNG with Chromium).

Usage:
  python3 tools/render.py spec.json OUT_DIR [--format both|ig|tiktok] [--sheet]

Writes
  OUT_DIR/pin.png                1000x1500   (Pinterest, if "pin" given)
  OUT_DIR/slide-N.png            1080x1350   (Instagram 4:5)
  OUT_DIR/tiktok/slide-N.png     1080x1920   (TikTok 9:16, text kept out of the app's overlay zones)
  OUT_DIR/sheet.png              contact sheet of the Instagram slides (with --sheet), for review
Prints JSON: {"written": [...], "warnings": [...]}. Any warning = fix the copy and render again.

Spec (see agents/creative-director.md for when to use which layout):
{
  "theme": "teal" | "mint" | "cream",              # colour scheme for this post; rotate between posts
  "pin": {"kicker", "title", "points": [3-4], "footer"},
  "slides": [ {"layout": "<name>", ...fields}, ... ]  # 5-8 slides
}
Layouts and fields (text fields accept *word* to highlight it):
  cover      kicker, title, sub?, number?          number = huge figure above the title
  statement  title, sub?
  number     number, label, note?, source?
  steps      title, items: [str]                   2-5 items
  checklist  title, items: [str | {"text", "ok": bool}]
  compare    title, left: {label, items}, right: {label, items}   right = the better option
  mistake    title?, mistake, fix, why?
  formula    title, parts: [str], ops?: [str], result: str, note?
  question   title, answer, note?
  example    title, rows: [[label, value]], total: [label, value], note?   (note it is an example)
  summary    title, items?: [str]
  cta        title, sub?, action                   footer adds "Link in bio" (IG) or the store URL (TikTok)
  text       title, body                           plain fallback
Optional on any slide: "tone": "dark" | "light" | "cream" | "amber" to override the theme default.
"""
import asyncio, html, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "fonts"
STORE = "payhip.com/soloprosheets"

FORMATS = {
    # name: (width, height, top, right, bottom, left) safe padding in px
    "ig": (1080, 1350, 84, 88, 84, 88),
    "tiktok": (1080, 1920, 210, 170, 560, 90),
}

TONES = {
    "dark":  dict(bg="#0E3B3A", ink="#FFFFFF", head="#FFFFFF", muted="#A9DCC8", hi="#F5B83D", card="#16504D", cardink="#FFFFFF", line="#2B6461", logo="#FFFFFF", logo1="#3BB98A"),
    "light": dict(bg="#EEF8F2", ink="#0D2321", head="#0E3B3A", muted="#4D6B64", hi="#F5B83D", card="#FFFFFF", cardink="#0D2321", line="#CFE0DA", logo="#0E3B3A", logo1="#3BB98A"),
    "cream": dict(bg="#FFF6E4", ink="#1E2B28", head="#0E3B3A", muted="#6E6250", hi="#3BB98A", card="#FFFFFF", cardink="#1E2B28", line="#EEDDBA", logo="#0E3B3A", logo1="#F5B83D"),
    "amber": dict(bg="#F5B83D", ink="#0E3B3A", head="#0E3B3A", muted="#5A4511", hi="#FFFFFF", card="#FFF3D6", cardink="#0E3B3A", line="#D99A1F", logo="#0E3B3A", logo1="#FFFFFF"),
}
# default tone per layout, per theme (controlled variation: same system, different composition)
THEMES = {
    "teal":  {"cover": "dark", "statement": "dark", "summary": "dark", "cta": "amber", "_": "light"},
    "mint":  {"cover": "light", "statement": "dark", "summary": "dark", "cta": "dark", "_": "light"},
    "cream": {"cover": "amber", "statement": "dark", "question": "dark", "cta": "dark", "_": "cream"},
}


def esc(s):
    """Escape text; *word* -> highlighted span; newline -> <br>."""
    t = html.escape(str(s or ""))
    t = re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', t)
    return t.replace("\n", "<br>")


def font_css():
    f = lambda n: (FONTS / n).as_uri()
    faces = [("Inter", 400, "Inter-Regular.otf"), ("Inter", 500, "Inter-Medium.otf"), ("Inter", 600, "Inter-SemiBold.otf"),
             ("Inter", 700, "Inter-Bold.otf"), ("InterDisplay", 800, "InterDisplay-ExtraBold.otf"), ("InterDisplay", 900, "InterDisplay-Black.otf")]
    css = "".join(f"@font-face{{font-family:{n};font-weight:{w};src:url('{f(p)}')}}" for n, w, p in faces)
    return css + f"@font-face{{font-family:Lora;font-style:italic;font-weight:400 700;src:url('{f('Lora-Italic-Variable.ttf')}')}}"


def logo():
    return '<span class="logo">' + "<i></i>" * 9 + "</span>"


BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:var(--w);height:var(--h);overflow:hidden}
body{font-family:Inter,Arial,sans-serif;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased}
.page{position:relative;width:var(--w);height:var(--h);padding:var(--pt) var(--pr) var(--pb) var(--pl);display:flex;flex-direction:column;background:var(--bg)}
.brand{display:flex;align-items:center;gap:14px;font-weight:700;font-size:26px;color:var(--logo);flex:none}
.brand .count{margin-left:auto;font-weight:600;font-size:24px;color:var(--muted)}
.logo{width:40px;height:40px;display:inline-grid;grid-template-columns:repeat(3,1fr);gap:3px}
.logo i{background:var(--logo);border-radius:3px}.logo i:nth-child(-n+3){background:var(--logo1)}.logo i:last-child{background:#F5B83D}
main{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column;justify-content:center;gap:calc(40px*var(--s));padding:calc(36px*var(--s)) 0}
footer{flex:none;display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;color:var(--muted)}
footer .go{color:var(--head)}
footer.final .go{font-size:38px;font-weight:800}
h1,h2,.big,.num{font-family:InterDisplay,Inter,sans-serif;color:var(--head);letter-spacing:-0.025em;line-height:1.02}
h1{font-weight:900;font-size:calc(var(--h1)*var(--s))}
h2{font-weight:800;font-size:calc(80px*var(--s));line-height:1.06}
.sub{font-size:calc(44px*var(--s));line-height:1.35;color:var(--muted);font-weight:500}
.kicker{align-self:flex-start;font-weight:700;font-size:24px;letter-spacing:.08em;text-transform:uppercase;color:var(--bg);background:var(--head);padding:10px 20px;border-radius:999px}
.hl{color:var(--hiText,var(--head));background:linear-gradient(transparent 58%,var(--hi) 58%,var(--hi) 92%,transparent 92%);padding:0 .06em}
.dark .hl,.amber .hl{background:none;color:var(--hi);padding:0}
.serif{font-family:Lora,Georgia,serif;font-style:italic;font-weight:500}
.card{background:var(--card);color:var(--cardink);border:2px solid var(--line);border-radius:28px;padding:calc(34px*var(--s)) calc(38px*var(--s))}
.p{font-size:calc(50px*var(--s));line-height:1.34}
.small{font-size:calc(34px*var(--s));line-height:1.4;color:var(--muted)}
/* cover */
.cover main{justify-content:flex-end;gap:calc(34px*var(--s))}
.cover .num{font-weight:900;font-size:calc(300px*var(--s));line-height:.9;color:var(--hi)}
.cover.light .num,.cover.cream .num{color:var(--head)}
.cover .rule{width:140px;height:16px;border-radius:8px;background:var(--hi)}
/* statement */
.statement main{justify-content:center}
.statement h1{font-size:calc(var(--h1s)*var(--s))}
/* number */
.number main{justify-content:center}
.number .num{font-weight:900;font-size:calc(250px*var(--s));line-height:.95;color:var(--hi)}
.number.light .num,.number.cream .num{color:var(--head)}
.number .label{font-family:InterDisplay,Inter;font-weight:800;font-size:calc(64px*var(--s));line-height:1.12;color:var(--head)}
/* steps */
.steps ol{list-style:none;display:flex;flex-direction:column;gap:calc(22px*var(--s));position:relative}
.steps li{display:flex;gap:28px;align-items:center;font-size:calc(48px*var(--s));line-height:1.3;font-weight:500}
.steps li b{flex:none;width:calc(78px*var(--s));height:calc(78px*var(--s));border-radius:50%;display:grid;place-items:center;background:var(--head);color:var(--bg);font-family:InterDisplay;font-weight:900;font-size:calc(38px*var(--s))}
.steps li:last-child b{background:var(--hi);color:#0E3B3A}
/* checklist */
.checklist ul{list-style:none;display:flex;flex-direction:column;gap:calc(18px*var(--s))}
.checklist li{display:flex;gap:24px;align-items:center;font-size:calc(48px*var(--s));line-height:1.28;font-weight:500;padding-bottom:calc(18px*var(--s));border-bottom:2px dashed var(--line)}
.checklist li:last-child{border-bottom:0}
.checklist li i{flex:none;width:calc(60px*var(--s));height:calc(60px*var(--s));border-radius:16px;display:grid;place-items:center;font-style:normal;font-weight:900;font-size:calc(36px*var(--s));background:#3BB98A;color:#fff}
.checklist li.no i{background:#E26D5A}
.checklist li.no span{color:var(--muted)}
/* compare */
.compare .cols{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.compare .col{border-radius:28px;padding:calc(30px*var(--s)) calc(28px*var(--s));border:2px solid var(--line);background:var(--card);color:var(--cardink)}
.compare .col.good{background:#0E3B3A;color:#fff;border-color:#0E3B3A}
.compare .col h3{font-family:InterDisplay;font-weight:800;font-size:calc(44px*var(--s));margin-bottom:calc(20px*var(--s))}
.compare .col.bad h3{color:#B5543F}.compare .col.good h3{color:#F5B83D}
.compare .col li{list-style:none;font-size:calc(38px*var(--s));line-height:1.3;margin-bottom:calc(16px*var(--s));padding-left:40px;position:relative}
.compare .col.bad li:before{content:"✕";position:absolute;left:0;color:#B5543F;font-weight:900}
.compare .col.good li:before{content:"✓";position:absolute;left:0;color:#3BB98A;font-weight:900}
/* mistake */
.mistake .m{position:relative}
.mistake .tag{display:inline-block;font-weight:800;font-size:24px;letter-spacing:.1em;text-transform:uppercase;padding:8px 16px;border-radius:10px;margin-bottom:calc(16px*var(--s))}
.mistake .bad .tag{background:#F7D9D2;color:#9E3F2C}.mistake .good .tag{background:#3BB98A;color:#fff}
.mistake .bad .p{text-decoration:line-through;text-decoration-color:#E26D5A;text-decoration-thickness:5px;color:var(--muted)}
.mistake .good{border-color:#3BB98A;border-width:4px}
.mistake .good .p{font-weight:700}
/* formula */
.formula .eq{display:flex;flex-direction:column;gap:calc(14px*var(--s))}
.formula .part{background:var(--card);border:2px solid var(--line);border-radius:22px;padding:calc(22px*var(--s)) calc(30px*var(--s));font-size:calc(46px*var(--s));font-weight:600;color:var(--cardink)}
.formula .op{align-self:flex-start;margin-left:34px;width:calc(56px*var(--s));height:calc(56px*var(--s));border-radius:50%;background:var(--hi);color:#0E3B3A;display:grid;place-items:center;font-weight:900;font-size:calc(36px*var(--s))}
.formula .res{background:#0E3B3A;color:#fff;border-radius:22px;padding:calc(26px*var(--s)) calc(30px*var(--s));font-family:InterDisplay;font-weight:900;font-size:calc(58px*var(--s))}
.dark .formula .res,.formula.dark .res{background:#F5B83D;color:#0E3B3A}
/* question */
.question main{justify-content:center}
.question .ans{border-left:14px solid var(--hi);padding:calc(10px*var(--s)) 0 calc(10px*var(--s)) 34px}
.question .ans .p{font-weight:600;color:var(--ink)}
.question .q{font-size:calc(190px*var(--s));line-height:.8;color:var(--hi);font-family:InterDisplay;font-weight:900}
/* example */
.example .rc{background:var(--card);border:2px solid var(--line);border-radius:28px;padding:calc(30px*var(--s)) calc(38px*var(--s));color:var(--cardink)}
.example .row{display:flex;justify-content:space-between;gap:20px;font-size:calc(44px*var(--s));padding:calc(16px*var(--s)) 0;border-bottom:2px dashed var(--line)}
.example .row span:last-child{font-weight:700;font-variant-numeric:tabular-nums}
.example .tot{display:flex;justify-content:space-between;font-family:InterDisplay;font-weight:900;font-size:calc(60px*var(--s));padding-top:calc(22px*var(--s));color:var(--head)}
.example .tag{align-self:flex-start;font-size:22px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
/* summary */
.summary main{justify-content:center}
.summary ul{list-style:none;display:flex;flex-wrap:wrap;gap:16px}
.summary li{font-size:calc(32px*var(--s));font-weight:600;padding:12px 24px;border-radius:999px;border:2px solid var(--line);color:var(--ink)}
/* cta */
.cta main{justify-content:center}
.cta .btn{align-self:flex-start;display:inline-flex;align-items:center;gap:18px;background:#0E3B3A;color:#fff;font-weight:800;font-size:calc(42px*var(--s));padding:calc(26px*var(--s)) calc(40px*var(--s));border-radius:999px}
.cta.dark .btn{background:#F5B83D;color:#0E3B3A}
.text .p{white-space:normal}
"""


def tone_for(slide, theme, i, n):
    if slide.get("tone") in TONES:
        return slide["tone"]
    t = THEMES.get(theme, THEMES["teal"])
    lay = slide.get("layout") or ("cover" if i == 1 else "text")
    return t.get(lay, t["_"])


def body_html(s, i):
    lay = s.get("layout") or ("cover" if i == 1 else "text")
    g = lambda k: esc(s.get(k))
    if lay == "cover":
        parts = []
        if s.get("kicker"): parts.append(f'<span class="kicker">{g("kicker")}</span>')
        if s.get("number"): parts.append(f'<div class="num">{g("number")}</div>')
        else: parts.append('<span class="rule"></span>')
        parts.append(f"<h1>{g('title')}</h1>")
        if s.get("sub"): parts.append(f'<p class="sub">{g("sub")}</p>')
        return lay, "".join(parts)
    if lay == "statement":
        return lay, f"<h1>{g('title')}</h1>" + (f'<p class="sub serif">{g("sub")}</p>' if s.get("sub") else "")
    if lay == "number":
        out = f'<div class="num">{g("number")}</div><div class="label">{g("label")}</div>'
        if s.get("note"): out += f'<p class="sub">{g("note")}</p>'
        if s.get("source"): out += f'<p class="small">Source: {g("source")}</p>'
        return lay, out
    if lay == "steps":
        li = "".join(f"<li><b>{k}</b><span>{esc(t)}</span></li>" for k, t in enumerate(s.get("items", []), 1))
        return lay, f"<h2>{g('title')}</h2><ol>{li}</ol>"
    if lay == "checklist":
        li = ""
        for it in s.get("items", []):
            it = it if isinstance(it, dict) else {"text": it, "ok": True}
            ok = it.get("ok", True)
            li += f'<li class="{"" if ok else "no"}"><i>{"✓" if ok else "✕"}</i><span>{esc(it.get("text"))}</span></li>'
        return lay, f"<h2>{g('title')}</h2><ul>{li}</ul>"
    if lay == "compare":
        col = lambda c, cls: f'<div class="col {cls}"><h3>{esc(c.get("label"))}</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in c.get("items", [])) + "</ul></div>"
        return lay, f"<h2>{g('title')}</h2><div class='cols'>{col(s.get('left', {}), 'bad')}{col(s.get('right', {}), 'good')}</div>"
    if lay == "mistake":
        out = f"<h2>{g('title')}</h2>" if s.get("title") else ""
        out += f'<div class="card m bad"><span class="tag">Mistake</span><p class="p">{g("mistake")}</p></div>'
        out += f'<div class="card m good"><span class="tag">Do this</span><p class="p">{g("fix")}</p></div>'
        if s.get("why"): out += f'<p class="small">{g("why")}</p>'
        return lay, out
    if lay == "formula":
        parts, ops = s.get("parts", []), s.get("ops") or ["+"] * max(0, len(s.get("parts", [])) - 1)
        eq = ""
        for k, p in enumerate(parts):
            eq += f'<div class="part">{esc(p)}</div>'
            if k < len(parts) - 1: eq += f'<div class="op">{esc(ops[k] if k < len(ops) else "+")}</div>'
        eq += f'<div class="op">=</div><div class="res">{g("result")}</div>'
        out = f"<h2>{g('title')}</h2><div class='eq'>{eq}</div>"
        if s.get("note"): out += f'<p class="small">{g("note")}</p>'
        return lay, out
    if lay == "question":
        out = f'<div class="q">?</div><h2>{g("title")}</h2><div class="ans"><p class="p">{g("answer")}</p></div>'
        if s.get("note"): out += f'<p class="small">{g("note")}</p>'
        return lay, out
    if lay == "example":
        rows = "".join(f'<div class="row"><span>{esc(a)}</span><span>{esc(b)}</span></div>' for a, b in s.get("rows", []))
        tl = s.get("total") or ["", ""]
        out = f'<span class="tag">Example numbers</span><h2>{g("title")}</h2><div class="rc">{rows}<div class="tot"><span>{esc(tl[0])}</span><span>{esc(tl[1])}</span></div></div>'
        if s.get("note"): out += f'<p class="small">{g("note")}</p>'
        return lay, out
    if lay == "summary":
        out = f"<h1 style='font-size:calc(96px*var(--s))'>{g('title')}</h1>"
        if s.get("items"): out += "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in s["items"]) + "</ul>"
        return lay, out
    if lay == "cta":
        out = f"<h1 style='font-size:calc(100px*var(--s))'>{g('title')}</h1>"
        if s.get("sub"): out += f'<p class="sub">{g("sub")}</p>'
        out += f'<span class="btn">{g("action") or "Get the free calculator"} →</span>'
        return lay, out
    return "text", f"<h2>{g('title')}</h2><p class='p'>{g('body')}</p>"


def slide_html(s, i, n, theme, fmt):
    w, h, pt, pr, pb, pl = FORMATS[fmt]
    tone = tone_for(s, theme, i, n)
    lay, inner = body_html(s, i)
    v = TONES[tone]
    tall = fmt == "tiktok"
    h1 = 118 if tall else 112
    h1s = 104 if tall else 96
    if i < n:
        foot = f'<footer><span class="go">Swipe →</span><span></span></footer>'
    else:
        foot = f'<footer class="final"><span class="go">{"Link in bio ↗" if fmt == "ig" else STORE}</span><span></span></footer>'
    vars_ = ";".join(f"--{k}:{val}" for k, val in v.items())
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}
:root{{--w:{w}px;--h:{h}px;--pt:{pt}px;--pr:{pr}px;--pb:{pb}px;--pl:{pl}px;--s:1;--h1:{h1}px;--h1s:{h1s}px;{vars_}}}
{BASE}</style></head><body>
<div class="page {lay} {tone}"><div class="brand">{logo()}SoloPro Sheets<span class="count">{i}/{n}</span></div>
<main class="{lay} {tone}">{inner}</main>{foot}</div></body></html>"""


def pin_html(p, theme):
    pts = "".join(f'<li><b>{k}</b><span>{esc(t)}</span></li>' for k, t in enumerate(p.get("points", [])[:4], 1))
    v = TONES["cream" if theme == "cream" else "light"]
    vars_ = ";".join(f"--{k}:{val}" for k, val in v.items())
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}
:root{{--w:1000px;--h:1500px;--pt:90px;--pr:80px;--pb:80px;--pl:80px;--s:1;--h1:84px;--h1s:84px;{vars_}}}
{BASE}
.pin main{{justify-content:flex-start;gap:calc(44px*var(--s))}}
.pin h1{{font-size:calc(88px*var(--s))}}
.pin ol{{list-style:none;display:flex;flex-direction:column;gap:calc(24px*var(--s))}}
.pin li{{display:flex;gap:24px;align-items:center;background:#fff;border-radius:22px;padding:calc(26px*var(--s)) 30px;font-size:calc(36px*var(--s));line-height:1.3;border:2px solid var(--line)}}
.pin li b{{flex:none;width:58px;height:58px;border-radius:50%;background:#F5B83D;color:#0E3B3A;display:grid;place-items:center;font-size:30px}}
.pin footer strong{{color:#0E3B3A}}</style></head><body>
<div class="page pin"><div class="brand">{logo()}SoloPro Sheets</div>
<main class="pin"><span class="kicker">{esc(p.get('kicker'))}</span><h1>{esc(p.get('title'))}</h1><ol>{pts}</ol></main>
<footer><span>{esc(p.get('footer') or 'Free price calculator')}</span><strong>{STORE}</strong></footer></div></body></html>"""


FIT_JS = """() => {
  const m = document.querySelector('main'); const r = document.documentElement;
  let s = 1;
  const over = () => m.scrollHeight > m.clientHeight + 1 || m.scrollWidth > m.clientWidth + 1;
  while (over() && s > 0.72) { s = +(s - 0.04).toFixed(2); r.style.setProperty('--s', s); }
  let wide = [...m.querySelectorAll('*')].some(e => e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflow !== 'visible');
  return {scale: s, overflow: over(), words: (m.innerText.match(/\\S+/g) || []).length};
}"""

async def show(pg, doc, out):
    """Load HTML from a file next to the output so local fonts/images (file://) are allowed."""
    f = out / ".render.html"; f.write_text(doc)
    await pg.goto(f.as_uri()); await pg.evaluate("document.fonts.ready")


WORD_LIMIT = {"cover": 18, "statement": 22, "number": 26, "question": 34, "cta": 26}


async def main(spec_path, out_dir, fmt="both", sheet=False):
    from playwright.async_api import async_playwright
    spec = json.loads(pathlib.Path(spec_path).read_text())
    theme = spec.get("theme", "teal")
    out = pathlib.Path(out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    written, warnings = [], []
    slides = spec.get("slides") or []
    n = len(slides)
    if slides and not 3 <= n <= 10:
        warnings.append(f"{n} slides: use 5-8")
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        if spec.get("pin"):
            pg = await b.new_page(viewport={"width": 1000, "height": 1500})
            await show(pg, pin_html(spec["pin"], theme), out)
            r = await pg.evaluate(FIT_JS)
            if r["overflow"]: warnings.append("pin: text does not fit")
            await pg.screenshot(path=str(out / "pin.png")); written.append("pin.png")
        fmts = ["ig", "tiktok"] if fmt == "both" else [fmt]
        for f in fmts:
            w, h = FORMATS[f][:2]
            d = out if f == "ig" else out / "tiktok"; d.mkdir(parents=True, exist_ok=True)
            pg = await b.new_page(viewport={"width": w, "height": h})
            for i, s in enumerate(slides, 1):
                await show(pg, slide_html(s, i, n, theme, f), out)
                r = await pg.evaluate(FIT_JS)
                lay = s.get("layout") or ("cover" if i == 1 else "text")
                if r["overflow"]: warnings.append(f"{f} slide {i} ({lay}): text does not fit, shorten it")
                elif r["scale"] < 0.85: warnings.append(f"{f} slide {i} ({lay}): text shrunk to {int(r['scale']*100)}%, consider shortening")
                lim = WORD_LIMIT.get(lay, 40)
                if f == "ig" and r["words"] > lim + 4:  # +4 for brand/footer words
                    warnings.append(f"slide {i} ({lay}): {r['words']} words, aim for under {lim}")
                fn = d / f"slide-{i}.png"; await pg.screenshot(path=str(fn)); written.append(str(fn.relative_to(out)))
        if sheet and slides:
            imgs = "".join(f'<img src="{(out / f"slide-{i}.png").as_uri()}">' for i in range(1, n + 1))
            cols = min(n, 4); rows = -(-n // cols)
            pg = await b.new_page(viewport={"width": cols * 540 + (cols + 1) * 20, "height": rows * 675 + (rows + 1) * 20})
            await show(pg, f"<body style='margin:0;background:#ccc;display:grid;grid-template-columns:repeat({cols},540px);gap:20px;padding:20px'>"
                                 f"<style>img{{width:540px;height:675px;display:block}}</style>{imgs}</body>", out)
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(out / "sheet.png")); written.append("sheet.png")
        await b.close()
    (out / ".render.html").unlink(missing_ok=True)
    print(json.dumps({"written": written, "warnings": warnings}, indent=1))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    fmt = "both"
    for fl in flags:
        if fl.startswith("--format="): fmt = fl.split("=", 1)[1]
    if "--format" in flags:  # allow "--format ig"
        k = sys.argv.index("--format"); fmt = sys.argv[k + 1]; args = [a for a in args if a != fmt]
    asyncio.run(main(args[0], args[1], fmt, "--sheet" in flags))
