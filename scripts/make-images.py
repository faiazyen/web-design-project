#!/usr/bin/env python3
"""Write the vector images for web/images (avatars, venue scenes, logo, social card source).

Usage:  python3 scripts/make-images.py
These images are original vector drawings made by Claude Code (AI), in the Golden Hour palette.
No photos, no real people. Plain Python 3, standard library only.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "web" / "images"
(OUT / "avatars").mkdir(parents=True, exist_ok=True)
(OUT / "venues").mkdir(parents=True, exist_ok=True)

CREAM, INK, CORAL, SEA, GOLD = "#FFF7EC", "#1B2A41", "#C93A22", "#0B6E77", "#F2A33A"
VARIANTS = {  # background, figure, accent
    "a": (CORAL, CREAM, GOLD),
    "b": (SEA, CREAM, GOLD),
    "c": (GOLD, INK, CORAL),
}


def svg(w, h, body, label=None):
    role = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true"'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"%s>%s</svg>\n'
            % (w, h, w, h, role, body))


def person(cx, cy, r, fg, scale=1.0):
    """Head and shoulders, centred on cx, head centre at cy."""
    bw = r * 2.6
    top = cy + r + 4
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
            '<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s"/>'
            % (cx, cy, r, fg, cx - bw, 130, cx - bw, top, cx, top, cx + bw, top, cx + bw, 130, fg))


def avatar(kind, variant):
    bg, fg, ac = VARIANTS[variant]
    clip = '<clipPath id="c"><circle cx="60" cy="60" r="60"/></clipPath>'
    inner = '<rect width="120" height="120" fill="%s"/>' % bg
    if kind == "instructor":   # a dance pair
        inner += person(44, 50, 11, fg) + person(78, 46, 12, ac)
    elif kind == "dj":         # head, headphones, deck
        inner += person(60, 52, 15, fg)
        inner += '<path d="M40 52 A20 20 0 0 1 80 52" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % ac
        inner += '<rect x="33" y="48" width="9" height="16" rx="4" fill="%s"/><rect x="78" y="48" width="9" height="16" rx="4" fill="%s"/>' % (ac, ac)
        inner += '<rect x="26" y="98" width="68" height="14" rx="4" fill="%s"/><circle cx="46" cy="105" r="5" fill="%s"/><circle cx="74" cy="105" r="5" fill="%s"/>' % (ac, bg, bg)
    elif kind == "music":      # musician with a note
        inner += person(46, 52, 14, fg)
        inner += '<circle cx="88" cy="84" r="8" fill="%s"/><rect x="94" y="40" width="5" height="45" fill="%s"/><path d="M99 40 q18 6 12 24 q-4 -12 -12 -14 Z" fill="%s"/>' % (ac, ac, ac)
    else:                      # show team: a line of dancers
        inner += person(26, 56, 9, fg) + person(60, 46, 11, ac) + person(94, 56, 9, fg)
    return svg(120, 120, "<defs>%s</defs><g clip-path=\"url(#c)\">%s</g>" % (clip, inner))


def sky(id_, c1, c2, c3):
    return ('<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="0.6" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>' % (id_, c1, c2, c3))


def arena():
    body = '<defs>%s</defs><rect width="800" height="500" fill="url(#s)"/>' % sky("s", "#FFE8C7", "#FFC98B", GOLD)
    body += '<circle cx="580" cy="290" r="78" fill="%s"/>' % CORAL
    body += '<path d="M0 300 Q200 270 400 300 T800 296 V500 H0 Z" fill="%s"/><path d="M0 330 Q220 300 420 332 T800 326 V500 H0 Z" fill="#0A5961"/>' % SEA
    body += '<rect y="372" width="800" height="128" fill="#F6D9A8"/>'
    body += '<rect x="90" y="190" width="10" height="190" fill="%s"/><rect x="330" y="190" width="10" height="190" fill="%s"/>' % (INK, INK)
    body += '<path d="M70 190 L215 130 L360 190 Z" fill="%s"/>' % INK
    body += '<ellipse cx="215" cy="400" rx="190" ry="34" fill="#E9C48C"/>'
    for i in range(9):
        body += '<circle cx="%d" cy="%d" r="5" fill="#FFF7EC"/>' % (96 + i * 32, 196 - (i % 2) * 6)
    return svg(800, 500, body)


def pavilion():
    body = '<rect width="800" height="500" fill="#FFF1DC"/>'
    body += '<defs>%s</defs>' % sky("w", "#BFE3E6", "#7CC4C9", SEA)
    for i in range(4):
        x = 60 + i * 180
        body += '<rect x="%d" y="70" width="140" height="250" rx="10" fill="url(#w)" stroke="%s" stroke-width="8"/>' % (x, INK)
        body += '<line x1="%d" y1="195" x2="%d" y2="195" stroke="%s" stroke-width="5"/>' % (x, x + 140, INK)
    body += '<rect y="330" width="800" height="170" fill="#C98F5A"/>'
    for i in range(10):
        body += '<line x1="0" y1="%d" x2="800" y2="%d" stroke="#B67B47" stroke-width="3"/>' % (352 + i * 15, 352 + i * 15)
    for i in range(5):
        body += '<circle cx="%d" cy="42" r="9" fill="%s"/>' % (110 + i * 145, GOLD)
    return svg(800, 500, body)


def club():
    body = '<rect width="800" height="500" fill="#0D1B2A"/><defs>%s</defs>' % sky("g", "#14283C", "#0D1B2A", "#0D1B2A")
    body += '<rect width="800" height="330" fill="url(#g)"/>'
    for x, col in ((150, "#FF7B5C"), (400, "#57C7CE"), (650, "#F5B04C")):
        body += '<polygon points="%d,0 %d,380 %d,380" fill="%s" opacity="0.22"/>' % (x, x - 110, x + 110, col)
    body += '<circle cx="400" cy="60" r="26" fill="#FDF3E7"/><path d="M380 50 h40 M376 62 h48 M382 74 h36" stroke="#14283C" stroke-width="3"/>'
    body += '<rect x="250" y="250" width="300" height="70" rx="6" fill="#14283C" stroke="#57C7CE" stroke-width="3"/><circle cx="330" cy="285" r="22" fill="#0D1B2A" stroke="#FF7B5C" stroke-width="3"/><circle cx="470" cy="285" r="22" fill="#0D1B2A" stroke="#FF7B5C" stroke-width="3"/>'
    body += '<rect y="340" width="800" height="160" fill="#14283C"/>'
    for i in range(8):
        body += '<rect x="%d" y="352" width="80" height="62" fill="%s" opacity="0.5"/>' % (i * 100, "#1B3350" if i % 2 else "#0F2236")
    return svg(800, 500, body)


def logo():
    return svg(64, 64, '<defs>%s</defs><circle cx="32" cy="32" r="30" fill="url(#l)"/><path d="M4 42 Q18 34 32 42 T60 42 V64 H4 Z" fill="%s"/>' % (
        '<linearGradient id="l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (CORAL, GOLD), SEA))


def social():
    body = '<defs>%s</defs><rect width="1200" height="630" fill="url(#s)"/>' % sky("s", "#FFE8C7", "#FFC98B", GOLD)
    body += '<circle cx="900" cy="420" r="120" fill="%s"/>' % CORAL
    body += '<path d="M0 500 Q300 460 600 500 T1200 496 V630 H0 Z" fill="%s"/><path d="M0 548 Q320 508 640 550 T1200 544 V630 H0 Z" fill="#0A5961"/>' % SEA
    body += ('<text x="70" y="215" font-family="Georgia, serif" font-size="84" font-weight="700" fill="%s">Atardecer</text>'
             '<text x="70" y="295" font-family="Georgia, serif" font-size="56" font-weight="700" fill="%s">Bachata Festival</text>'
             '<text x="70" y="360" font-family="Arial, sans-serif" font-size="34" fill="%s">Valencia · 25–27 June 2027</text>'
             '<text x="70" y="406" font-family="Arial, sans-serif" font-size="30" fill="%s">Sea by day, club by night</text>') % (INK, INK, INK, INK)
    return svg(1200, 630, body)


def main():
    n = 0
    for kind in ("instructor", "dj", "music", "team"):
        for v in "abc":
            (OUT / "avatars" / ("%s-%s.svg" % (kind, v))).write_text(avatar(kind, v), encoding="utf-8"); n += 1
    for name, fn in (("arena-stage", arena), ("pabellon-brisa", pavilion), ("marea-club", club)):
        (OUT / "venues" / (name + ".svg")).write_text(fn(), encoding="utf-8"); n += 1
    (OUT / "logo.svg").write_text(logo(), encoding="utf-8")
    (OUT / "social-card.svg").write_text(social(), encoding="utf-8")
    print("wrote %d avatar and venue images, logo.svg and social-card.svg in %s" % (n, OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
