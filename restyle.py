"""Apply the vintage collage look (brown paper, kraft strips, gold nouveau type) to both pages.

Usage: python3 -I restyle.py <page.html> [<page.html> ...]
Replaces the font link and the colour-token blocks, appends theme overrides,
and adds the decorative layers around the page wrapper. Safe to run once per page.
"""
import random
import re
import sys

FONT_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..900,0..100,0..1;1,9..144,400..900,0..100,0..1'
             '&family=Macondo+Swash+Caps&family=Mulish:ital,wght@0,400;0,600;0,700;1,400'
             '&family=IBM+Plex+Mono:wght@400;500&family=Homemade+Apple&display=swap">')

GRAIN = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E"
         "%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .22 0'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")

TOKENS = f""":root {{
  /* One deliberate look: walnut-brown scrapbook page, kraft-paper strips, gold Art Nouveau type. Single theme by design. */
  --paper: #6A391B;
  --card: #5A2F15;
  --ink: #F1E0B8;
  --muted: #D3BA8C;
  --rule: #8C5C33;
  --line: transparent;
  --redline: #C9A46A;
  --spine: #E7C77F;
  --spine-ink: #48230F;
  --stamp: #F2D58C;
  --chip: #7A4524;
  --good: #D6E4A6;
  --warn: #F4B784;
  --star: #F2C24E;
  --kraft: #C9A46A;
  --kraft-deep: #A88049;
  --field: #4E2811;
  --grain: {GRAIN};
  --font-display: "Fraunces", "Iowan Old Style", Georgia, serif;
  --font-deco: "Macondo Swash Caps", "Fraunces", Georgia, serif;
  --font-body: "Mulish", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
  --font-script: "Homemade Apple", "Snell Roundhand", "Brush Script MT", cursive;
  color-scheme: dark;
}}
"""

OVERRIDES = """
/* ---------- Vintage collage theme ---------- */
body { background: var(--paper) var(--grain); background-attachment: fixed; color: var(--ink); font-family: var(--font-body); }
.wrap { position: relative; z-index: 1; }
.ink-bg { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.ink-bg p { position: absolute; left: -4%; width: 110%; margin: 0; font-family: var(--font-script); font-size: clamp(20px, 2.6vw, 34px); line-height: 1.9; color: var(--ink); opacity: .06; transform: rotate(-4deg); white-space: nowrap; }
.torn { position: relative; z-index: 2; filter: drop-shadow(0 3px 3px rgba(0, 0, 0, .35)); pointer-events: none; }
.torn span { display: block; height: 58px; background: var(--kraft) var(--grain); }
.torn.top span { clip-path: TOP_POLY; }
.torn.bottom { margin-top: 24px; filter: drop-shadow(0 -3px 3px rgba(0, 0, 0, .3)); }
.torn.bottom span { clip-path: BOTTOM_POLY; }

header.top { position: relative; }
header.top > * { position: relative; z-index: 1; }
header.top::after {
  content: ""; position: absolute; z-index: 0; right: -10px; top: -46px; width: 230px; height: 230px; border-radius: 50%;
  background: radial-gradient(circle, var(--ink) 34%, transparent 37%) 0 0 / 9px 9px;
  -webkit-mask: radial-gradient(circle, #000 18%, transparent 68%); mask: radial-gradient(circle, #000 18%, transparent 68%);
  opacity: .32; pointer-events: none;
}
@media (max-width: 640px) { header.top::after { width: 150px; height: 150px; top: -30px; } }

h1 { font-family: var(--font-display); font-variation-settings: "SOFT" 100, "WONK" 1; font-weight: 800; color: var(--spine); letter-spacing: -.01em; text-shadow: 0 2px 0 rgba(0, 0, 0, .18); }
.eyebrow { color: var(--kraft); }
.lede { color: var(--muted); }
.q, .panel h3, .shelf h2, .shelf-head h2 { font-family: var(--font-deco); font-weight: 400; color: var(--spine); letter-spacing: .01em; }
.q { font-size: 1.35rem; }
.q .n { color: var(--kraft); }
.drawer-title { font-family: var(--font-deco); text-transform: none; letter-spacing: .02em; font-size: 1.05rem; color: var(--spine); }
.ctitle, .solved h2 { font-family: var(--font-display); font-variation-settings: "SOFT" 100, "WONK" 0; font-weight: 700; color: var(--ink); }
.cauthor, .solved .by { color: var(--muted); }
.alt .t, .book .t, .shelf li .t { font-family: var(--font-display); font-variation-settings: "SOFT" 100; font-weight: 600; }
.tally b { font-family: var(--font-display); color: var(--spine); }
fieldset { border-bottom-color: var(--rule); }

/* Engraving frame: double gold rule, inset second line */
.catcard {
  background: var(--card) var(--grain); border-radius: 2px; margin: 8px;
  border: 2px solid var(--kraft); outline: 1px solid var(--kraft-deep); outline-offset: 6px;
  box-shadow: inset 0 0 0 6px var(--card), inset 0 0 0 7px var(--kraft-deep), 0 18px 36px -22px rgba(0, 0, 0, .7);
}
.catcard::after { content: "❦"; width: auto; height: auto; margin-left: -.5em; bottom: 14px; background: none; box-shadow: none; border-radius: 0; color: var(--kraft); font-size: 18px; line-height: 1; }
.cardmeta b, .meta b { color: var(--spine); }
.clues li .k { color: var(--kraft); }
.cover {
  border: 3px double var(--kraft); padding: 4px; background: var(--kraft-deep); border-radius: 1px;
  box-shadow: 0 0 0 1px var(--card), 0 0 0 3px var(--kraft-deep), 0 10px 20px -10px rgba(0, 0, 0, .7);
}
.cover.sm { padding: 2px; border-width: 2px; border-style: solid; box-shadow: 0 0 0 1px var(--kraft-deep); }
.spine { background: var(--spine); color: var(--spine-ink); border-radius: 1px; box-shadow: inset 0 0 0 2px var(--spine), inset 0 0 0 3px var(--spine-ink); }
.spine.unknown { background: transparent; color: var(--spine); border: 1.5px dashed var(--spine); box-shadow: none; }
.stamp { color: var(--stamp); border-color: var(--stamp); background: rgba(74, 37, 16, .75); }

.chip span { background: var(--chip); border-color: var(--kraft-deep); color: var(--ink); }
.chip:hover span { border-color: var(--spine); }
.chip input:checked + span { background: var(--spine); border-color: var(--spine); color: var(--spine-ink); }
button { border-color: var(--ink); color: var(--ink); }
button.primary { background: var(--spine); border-color: var(--spine); color: var(--spine-ink); }
button:hover:not(:disabled) { border-color: var(--spine); color: var(--spine); }
button.primary:hover:not(:disabled) { background: var(--ink); border-color: var(--ink); color: var(--spine-ink); }
button.link { color: var(--muted); }
button.link:hover:not(:disabled) { color: var(--ink); }
input[type=text], input[type=number], textarea, select { background: var(--field); border-color: var(--kraft-deep); color: var(--ink); }
input::placeholder, textarea::placeholder { color: var(--muted); opacity: .7; }
:focus-visible { outline-color: var(--stamp) !important; }

.alt { background: var(--card) var(--grain); border-color: var(--kraft-deep); border-top: 3px solid var(--kraft); }
.alt:hover { border-color: var(--spine); border-top-color: var(--spine); }
.tab { background: var(--chip); border-color: var(--kraft-deep); }
.tab[aria-selected="true"] { background: var(--spine); border-color: var(--spine); color: var(--spine-ink); }
.pip { background: var(--chip); }
.pip.on { background: var(--spine); }
.bar { background: var(--field); box-shadow: inset 0 0 0 1px var(--kraft-deep); }
.bar i { background: var(--spine); }
.miss { border-color: var(--kraft-deep); color: var(--muted); }
.howto { border-top-color: var(--rule); }
.shelf { position: relative; border-top: 0; padding-top: 30px; background: linear-gradient(var(--kraft), var(--kraft)) top / 100% 2px no-repeat; }
.shelf::before { content: "❦ ❦ ❦"; position: absolute; top: -12px; left: 50%; transform: translateX(-50%); padding: 0 14px; background: var(--paper); color: var(--kraft); letter-spacing: .35em; font-size: 15px; line-height: 24px; white-space: nowrap; }
.book, .shelf li { border-bottom-color: var(--rule); }
.stars button { color: var(--rule); }
.stars button.on, .stars button:hover { color: var(--star); }
footer { color: var(--muted); opacity: .85; }
"""

SCRIPT_LINES = [
    "return to the library by the fourteenth ~ renew twice",
    "chapter twelve: reread the letters before book club",
    "p. 213 underlined twice, the line about the river",
    "lend this one to Mama when I'm done",
    "started on the train, finished on the porch",
    "ask the librarian for the sequel, second shelf, left",
    "copy the first page into my notebook",
    "the ending made me sit very still",
]


def jagged(edge, seed):
    """A torn-paper clip-path. edge='bottom' tears the lower edge, 'top' the upper."""
    rnd = random.Random(seed)
    xs = [0]
    while xs[-1] < 100:
        xs.append(min(100, round(xs[-1] + rnd.uniform(1.2, 3.6), 2)))
    if edge == "bottom":
        pts = ["0% 0%", "100% 0%"] + [f"{x}% {round(rnd.uniform(52, 98), 1)}%" for x in reversed(xs)]
    else:
        pts = [f"{x}% {round(rnd.uniform(2, 48), 1)}%" for x in xs] + ["100% 100%", "0% 100%"]
    return "polygon(" + ", ".join(pts) + ")"


def restyle(path):
    s = open(path, encoding="utf-8").read()
    if "Vintage collage theme" in s:
        sys.exit(f"{path}: already restyled")
    s, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">', lambda m: FONT_LINK, s, count=1)
    assert n == 1, "font link"
    s, n = re.subn(r':root \{.*?\n\}\n@media \(prefers-color-scheme: dark\) \{.*?\n\}\n:root\[data-theme="dark"\] \{.*?\n\}\n',
                   lambda m: TOKENS, s, count=1, flags=re.S)
    assert n == 1, "token blocks"
    css = OVERRIDES.replace("TOP_POLY", jagged("bottom", 7)).replace("BOTTOM_POLY", jagged("top", 11))
    assert s.count("</style>") == 1
    s = s.replace("</style>", css + "</style>")
    lines = "".join(f'<p style="top:{6 + i * 12}%">{t} &nbsp;·&nbsp; {SCRIPT_LINES[(i + 3) % len(SCRIPT_LINES)]}</p>'
                    for i, t in enumerate(SCRIPT_LINES))
    assert s.count('<div class="wrap">') == 1
    s = s.replace('<div class="wrap">',
                  f'<div class="ink-bg" aria-hidden="true">{lines}</div>\n'
                  '<div class="torn top" aria-hidden="true"><span></span></div>\n<div class="wrap">')
    head, sep, tail = s.partition("\n<script>")
    assert sep and head.rstrip().endswith("</div>")
    s = head.rstrip() + '\n<div class="torn bottom" aria-hidden="true"><span></span></div>\n' + sep + tail
    open(path, "w", encoding="utf-8").write(s)
    print("restyled", path)


for p in sys.argv[1:]:
    restyle(p)
