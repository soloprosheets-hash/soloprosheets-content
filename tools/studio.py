"""Studio look for SoloPro Sheets slides: device mockups, line icons and polish CSS.

Imported by render.py. Everything is drawn with HTML/CSS/inline SVG (no paid tools, no stock images).
Icons are original simple line drawings (24x24, stroke) made for this repo.
"""
import html, re

# ---------------------------------------------------------------- icons
_P = {
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "card": '<rect x="2.5" y="5.5" width="19" height="13" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/>',
    "phone": '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "shield": '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5z"/><path d="M4 20.5A2.5 2.5 0 006.5 23H20v-5"/>',
    "bank": '<path d="M3 9.5L12 4l9 5.5M4.5 10v8M9.5 10v8M14.5 10v8M19.5 10v8M3 21h18"/>',
    "tool": '<path d="M14.5 6.5a4 4 0 005 5L13 18l-3 3-4-4 3-3 6.5-6.5a4 4 0 01-1-1z"/>',
    "tweezers": '<path d="M7 3l4.2 13.5a1 1 0 001.6 0L17 3"/><path d="M9.8 12.2h4.4M12 17v4"/>',
    "lamp": '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0012 3z"/>',
    "shirt": '<path d="M8 3l4 2.5L16 3l5 3.5-2.5 4-2-1.2V21h-9V9.3l-2 1.2L3 6.5z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
    "euro": '<path d="M17.5 6.2A7 7 0 1017.5 17.8"/><path d="M4 10.2h9M4 13.8h9"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.3-4 4.3-6 8-6s6.7 2 8 6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.4-5.3 6.5-5.3s5.5 1.8 6.5 5.3"/><path d="M15.5 4.8a3.5 3.5 0 010 6.6M18 14.9c1.8.8 3 2.5 3.5 5.1"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "bell": '<path d="M6 16V11a6 6 0 1112 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 004 0"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.7 2.7L16.2 9.5"/>',
    "receipt": '<path d="M5 3h14v18l-2.4-1.5L14 21l-2-1.5-2 1.5-2.6-1.5L5 21z"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
    "repeat": '<path d="M4 11V9a3 3 0 013-3h12M16 3l3 3-3 3M20 13v2a3 3 0 01-3 3H5M8 21l-3-3 3-3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "wallet": '<path d="M3.5 7.5A2.5 2.5 0 016 5h12v3"/><rect x="3.5" y="8" width="17" height="12" rx="2.5"/><path d="M16.5 14h1.5"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
    "sparkle": '<path d="M12 3c.6 4.6 2.4 6.4 7 7-4.6.6-6.4 2.4-7 7-.6-4.6-2.4-6.4-7-7 4.6-.6 6.4-2.4 7-7zM19 16c.3 1.8 1 2.6 2.8 2.8-1.8.3-2.5 1-2.8 2.8-.3-1.8-1-2.5-2.8-2.8 1.8-.2 2.5-1 2.8-2.8z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0112 7.3a4.3 4.3 0 017.5 2.5C19.5 15.4 12 20 12 20z"/>',
    "message": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "box": '<path d="M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5z"/><path d="M3.5 7.5L12 12l8.5-4.5M12 12v9"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5.5 9.5V20h13V9.5"/><path d="M10 20v-5h4v5"/>',
    "x": '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
}
ICONS = sorted(_P)


def icon(name, cls="ic"):
    p = _P.get(name or "", _P["check"])
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round">{p}</svg>')


def _e(s):
    t = html.escape(str(s if s is not None else ""))
    t = re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', t)
    return t.replace("\n", "<br>")


# ---------------------------------------------------------------- mockups
GRID_LOGO = '<span class="mlogo">' + "<i></i>" * 9 + "</span>"


def sheet_screen(sc):
    """A spreadsheet-style app screen. sc: {app, tabs?, tab?, cols?, rows:[[a,b(,c)]], hi?: row index | [..],
    total?: [label, value], chip?}"""
    tabs = sc.get("tabs") or ([sc["tab"]] if sc.get("tab") else [])
    active = sc.get("tab") or (tabs[0] if tabs else "")
    tabs_h = "".join(f'<span class="{"on" if t == active else ""}">{_e(t)}</span>' for t in tabs)
    hi = sc.get("hi", [])
    hi = hi if isinstance(hi, list) else [hi]
    cols = sc.get("cols")
    head = ""
    if cols:
        head = '<div class="tr th">' + "".join(f"<span>{_e(c)}</span>" for c in cols) + "</div>"
    rows = ""
    for k, r in enumerate(sc.get("rows", [])):
        cells = "".join(f"<span>{_e(c)}</span>" for c in r)
        rows += f'<div class="tr{" hi" if k in hi else ""}">{cells}</div>'
    tot = ""
    if sc.get("total"):
        a, b = sc["total"]
        tot = f'<div class="tr tot"><span>{_e(a)}</span><span>{_e(b)}</span></div>'
    chip = f'<div class="chip">{_e(sc["chip"])}</div>' if sc.get("chip") else ""
    return (f'<div class="app">{GRID_LOGO}<div><b>{_e(sc.get("app", "Business Tracker"))}</b>'
            f'<small>{_e(sc.get("sub", "Google Sheets"))}</small></div></div>'
            + (f'<div class="tabs">{tabs_h}</div>' if tabs_h else "")
            + f'<div class="tbl">{head}{rows}{tot}</div>{chip}')


def dash_screen(sc):
    """Dashboard screen: kpis [[label, value]], bars [[label, number]] (heights relative), hi bar index."""
    kp = "".join(f'<div class="kpi"><small>{_e(a)}</small><b>{_e(b)}</b></div>' for a, b in sc.get("kpis", [])[:3])
    bars = sc.get("bars", [])
    mx = max([float(b) for _, b in bars] or [1]) or 1
    hi = sc.get("hi", -1)
    bh = "".join(f'<div class="bar{" on" if k == hi else ""}"><i style="height:{max(6, float(v) / mx * 100):.0f}%"></i>'
                 f'<small>{_e(l)}</small></div>' for k, (l, v) in enumerate(bars))
    return (f'<div class="app">{GRID_LOGO}<div><b>{_e(sc.get("app", "Dashboard"))}</b>'
            f'<small>{_e(sc.get("sub", "Google Sheets"))}</small></div></div>'
            f'<div class="kpis">{kp}</div>' + (f'<div class="bars">{bh}</div>' if bars else ""))


def phone(sc, cls=""):
    body = dash_screen(sc) if sc.get("kpis") else sheet_screen(sc)
    return (f'<div class="dev dphone {cls}"><div class="scr"><div class="sbar"><span>9:41</span><i></i>'
            f'<span class="sig">●●● ▮</span></div>{body}</div></div>')


def laptop(sc):
    body = dash_screen(sc) if sc.get("kpis") else sheet_screen(sc)
    return (f'<div class="dev dlaptop"><div class="lid"><div class="cam"></div><div class="scr">{body}</div></div>'
            f'<div class="base"></div></div>')


def badge(b):
    if not b:
        return ""
    if isinstance(b, str):
        b = {"text": b}
    return f'<div class="badge">{icon(b.get("icon", "sparkle"), "bi")}<span>{_e(b.get("text"))}</span></div>'


EXAMPLE_TAG = '<span class="extag">Illustration · example numbers</span>'


# ---------------------------------------------------------------- CSS
CSS = r"""
/* ---------- studio polish ---------- */
.page{isolation:isolate;overflow:hidden}
.page:before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(900px 700px at 105% -10%,var(--glow),transparent 60%),
             radial-gradient(700px 600px at -15% 110%,var(--glow2),transparent 60%)}
.page:after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;opacity:var(--dots);
  background-image:radial-gradient(var(--dotc) 1.6px,transparent 1.8px);background-size:34px 34px;
  -webkit-mask-image:linear-gradient(160deg,#000 0%,transparent 55%)}
.brand{font-size:27px;letter-spacing:-.01em}
.brand .count{display:flex;gap:7px;align-items:center}
.brand .count i{width:12px;height:12px;border-radius:6px;background:var(--line);opacity:.9}
.brand .count i.on{width:34px;background:var(--hi)}
.dark .brand .count i:not(.on){background:#2F6B68}
.amber .brand .count i:not(.on){background:#D99A1F}.amber .brand .count i.on{background:#0E3B3A}
footer .go{display:inline-flex;align-items:center;gap:12px;font-size:26px;padding:12px 24px;border-radius:999px;
  background:var(--card);color:var(--cardink);box-shadow:0 8px 24px rgba(14,59,58,.10)}
.dark footer .go{background:rgba(255,255,255,.08);color:#fff;box-shadow:none;border:1.5px solid rgba(255,255,255,.18)}
footer.final .go{font-size:34px;padding:16px 30px;background:var(--hi);color:#0E3B3A;border:0}
.amber footer.final .go{background:#0E3B3A;color:#fff}
.card,.compare .col,.formula .part,.example .rc{border:0!important;box-shadow:0 18px 50px -12px rgba(14,59,58,.22),0 2px 6px rgba(14,59,58,.06)}
.dark .card,.dark .formula .part{background:#14504D;box-shadow:0 18px 50px -12px rgba(0,0,0,.45)}
.mistake .good{outline:4px solid #3BB98A;outline-offset:-4px}
.checklist li{border-bottom:0;padding:calc(16px*var(--s)) calc(22px*var(--s));background:var(--card);border-radius:22px;
  box-shadow:0 10px 30px -10px rgba(14,59,58,.22)}
.dark .checklist li{background:#14504D;box-shadow:none}
.checklist ul{gap:calc(16px*var(--s))}
.checklist li i.icb{width:calc(76px*var(--s));height:calc(76px*var(--s));border-radius:20px;background:var(--tint);color:var(--head)}
.dark .checklist li i.icb{background:#0E3B3A;color:#F5B83D}
.checklist li i.icb svg{width:58%;height:58%}
.checklist li small{display:block;font-size:calc(30px*var(--s));color:var(--muted);font-weight:500;margin-top:4px}
.steps li b{box-shadow:0 8px 20px -6px rgba(14,59,58,.45)}
.extag{align-self:flex-start;font-size:21px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
  padding:8px 16px;border:1.5px dashed var(--line);border-radius:10px}
.dark .extag{border-color:#2F6B68}

/* ---------- devices ---------- */
.dev{position:relative;flex:none}
.dphone{width:calc(var(--pw)*var(--s));border-radius:calc(74px*var(--s));padding:calc(15px*var(--s));background:#0B1F1E;
  box-shadow:0 0 0 2px #2A3F3D inset,0 50px 90px -30px rgba(9,40,38,.55),0 18px 40px -18px rgba(9,40,38,.5)}
.dphone .scr{border-radius:calc(60px*var(--s));overflow:hidden;background:#F7FAF8;color:#0D2321;
  padding:calc(20px*var(--s)) calc(26px*var(--s)) calc(34px*var(--s));min-height:calc(var(--ph)*var(--s));font-size:calc(28px*var(--s))}
.dphone .sbar{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:calc(22px*var(--s));padding:0 calc(14px*var(--s)) calc(16px*var(--s))}
.dphone .sbar i{width:calc(120px*var(--s));height:calc(34px*var(--s));border-radius:20px;background:#0B1F1E}
.dphone .sbar .sig{font-size:calc(14px*var(--s));letter-spacing:1px}
.app{display:flex;gap:calc(16px*var(--s));align-items:center;margin-bottom:calc(18px*var(--s))}
.app b{display:block;font-family:InterDisplay;font-weight:800;font-size:calc(31px*var(--s));letter-spacing:-.01em;line-height:1.1}
.app small{display:block;font-size:calc(19px*var(--s));color:#6B807B;font-weight:600}
.mlogo{width:calc(48px*var(--s));height:calc(48px*var(--s));display:grid;grid-template-columns:repeat(3,1fr);gap:3px;padding:7px;border-radius:13px;background:#0E3B3A;flex:none}
.mlogo i{background:#fff;border-radius:2px}.mlogo i:nth-child(-n+3){background:#3BB98A}.mlogo i:last-child{background:#F5B83D}
.tabs{display:flex;gap:calc(8px*var(--s));margin-bottom:calc(16px*var(--s));flex-wrap:nowrap;overflow:hidden}
.tabs span{font-size:calc(19px*var(--s));font-weight:700;padding:calc(8px*var(--s)) calc(14px*var(--s));border-radius:999px;background:#E6EFEB;color:#4D6B64;white-space:nowrap}
.tabs span.on{background:#0E3B3A;color:#fff}
.tbl{background:#fff;border-radius:calc(22px*var(--s));overflow:hidden;box-shadow:0 1px 0 #DCE7E2,0 8px 24px -14px rgba(14,59,58,.35)}
.tr{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:center;padding:calc(15px*var(--s)) calc(20px*var(--s));
  font-size:calc(25px*var(--s));border-bottom:1.5px solid #EDF2F0}
.tr span:not(:first-child){font-weight:700;font-variant-numeric:tabular-nums;text-align:right}
.tr.th{background:#F1F6F4;font-size:calc(17px*var(--s));font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#6B807B}
.tr.hi{background:#FFF4D9;box-shadow:inset 6px 0 0 #F5B83D}
.tr.tot{background:#0E3B3A;color:#fff;font-family:InterDisplay;font-weight:800;font-size:calc(29px*var(--s));border:0}
.tr.tot span:last-child{color:#F5B83D}
.tbl .tr:has(span:nth-child(3)){grid-template-columns:1fr auto auto}
.chip{margin-top:calc(16px*var(--s));display:inline-flex;font-size:calc(20px*var(--s));font-weight:700;color:#0E3B3A;background:#D7F0E5;padding:calc(9px*var(--s)) calc(16px*var(--s));border-radius:999px}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:calc(10px*var(--s));margin-bottom:calc(14px*var(--s))}
.kpi{background:#fff;border-radius:calc(18px*var(--s));padding:calc(14px*var(--s)) calc(14px*var(--s));box-shadow:0 6px 18px -10px rgba(14,59,58,.35)}
.kpi small{display:block;font-size:calc(16px*var(--s));font-weight:700;color:#6B807B;text-transform:uppercase;letter-spacing:.05em}
.kpi b{display:block;font-family:InterDisplay;font-weight:900;font-size:calc(34px*var(--s));color:#0E3B3A;margin-top:4px;white-space:nowrap}
.kpi:first-child{background:#0E3B3A}.kpi:first-child b{color:#F5B83D}.kpi:first-child small{color:#A9DCC8}
.bars{display:flex;align-items:flex-end;gap:calc(12px*var(--s));height:calc(var(--bh)*var(--s));background:#fff;border-radius:calc(18px*var(--s));
  padding:calc(18px*var(--s)) calc(16px*var(--s)) calc(10px*var(--s));box-shadow:0 6px 18px -10px rgba(14,59,58,.35)}
.bar{flex:1;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px}
.bar i{width:100%;border-radius:8px 8px 3px 3px;background:#BFE3D3}
.bar.on i{background:#3BB98A}
.bar small{font-size:calc(15px*var(--s));font-weight:700;color:#6B807B}
.dlaptop{width:calc(var(--lw)*var(--s))}
.dlaptop .lid{background:#0B1F1E;border-radius:calc(30px*var(--s)) calc(30px*var(--s)) 0 0;padding:calc(22px*var(--s)) calc(22px*var(--s)) calc(26px*var(--s));position:relative;
  box-shadow:0 0 0 2px #2A3F3D inset}
.dlaptop .cam{position:absolute;top:calc(8px*var(--s));left:50%;width:8px;height:8px;border-radius:4px;background:#2A3F3D}
.dlaptop .scr{background:#F7FAF8;border-radius:calc(8px*var(--s));padding:calc(22px*var(--s));color:#0D2321;font-size:calc(24px*var(--s));--bh:200px}
.dlaptop .base{height:calc(28px*var(--s));margin:0 calc(-60px*var(--s));background:linear-gradient(#DCE3E0,#AEB9B5);border-radius:0 0 calc(40px*var(--s)) calc(40px*var(--s));
  box-shadow:0 40px 60px -26px rgba(9,40,38,.55);position:relative}
.dlaptop .base:before{content:"";position:absolute;left:50%;top:0;transform:translateX(-50%);width:18%;height:40%;background:#9AA6A2;border-radius:0 0 12px 12px}
.badge{position:absolute;display:flex;align-items:center;gap:14px;background:#fff;color:#0E3B3A;border-radius:22px;
  padding:calc(18px*var(--s)) calc(24px*var(--s));font-weight:800;font-size:calc(30px*var(--s));line-height:1.2;max-width:calc(380px*var(--s));
  box-shadow:0 24px 50px -16px rgba(9,40,38,.45)}
.badge .bi{flex:none;width:calc(46px*var(--s));height:calc(46px*var(--s));padding:9px;border-radius:14px;background:#F5B83D;color:#0E3B3A}

/* ---------- mockup layouts ---------- */
.devrow{display:flex;justify-content:center;position:relative;margin-top:calc(6px*var(--s));padding:0 calc(46px*var(--s))}
.mock main{justify-content:center;gap:calc(26px*var(--s))}
.mock h2{font-size:calc(72px*var(--s))}
.mock .sub{font-size:calc(38px*var(--s))}
.mock .devrow .badge{right:0;bottom:calc(70px*var(--s))}
.mock.tl .devrow .badge{right:auto;left:0}

.withdev main{justify-content:flex-start;gap:calc(26px*var(--s))}
.cover.withdev h1{font-size:calc(var(--h1)*.9*var(--s))}
.cvdev{position:absolute;right:calc(var(--pr) - 40px);bottom:calc(var(--pb) + 30px);transform:rotate(-7deg);transform-origin:bottom right}
.cvdev .badge{right:calc(100% - 40px*var(--s));left:auto;top:calc(210px*var(--s));white-space:nowrap}
.cta .cvdev{bottom:calc(var(--pb) + 130px)}
.withdev .sub{max-width:62%}
.cta.withdev h1{max-width:80%}
"""

# per-tone extras: glow colours, dots, tint
TONE_EXTRA = {
    "dark": dict(glow="rgba(59,185,138,.28)", glow2="rgba(245,184,61,.14)", dots=".22", dotc="#3E7D79", tint="#16504D"),
    "light": dict(glow="rgba(59,185,138,.22)", glow2="rgba(245,184,61,.18)", dots=".55", dotc="#C6DCD4", tint="#DDF1E8"),
    "cream": dict(glow="rgba(245,184,61,.28)", glow2="rgba(59,185,138,.14)", dots=".55", dotc="#EADBB9", tint="#FBE9C2"),
    "amber": dict(glow="rgba(255,255,255,.35)", glow2="rgba(14,59,58,.12)", dots=".35", dotc="#E0A22C", tint="#FFF3D6"),
}
