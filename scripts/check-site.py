#!/usr/bin/env python3
"""Offline checks of the built site (web/). Standard library only.

Checks: every internal link and image resolves (files and #anchors), tags are balanced, titles and descriptions are unique,
JSON-LD parses and its names/dates/prices appear as visible text, no external requests (scripts, styles, images),
sitemap lists existing files, colour contrast of the Golden Hour pairs (Day and Night).
Usage: python3 scripts/check-site.py   (exit code 1 when something fails)
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urlparse, unquote

WEB = Path(__file__).resolve().parent.parent / "web"
VOID = {"meta", "link", "img", "input", "br", "hr", "source", "area", "base", "col", "wbr"}
errors = []


def err(msg):
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.links, self.assets, self.ld, self.text = [], set(), [], [], [], []
        self.title, self.desc, self._t, self._ld, self.h1 = "", "", False, False, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in a:
            if a["id"] in self.ids:
                err("duplicate id %s" % a["id"])
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon"):
            self.assets.append(a["href"])
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "title":
            self._t = True
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "title":
            self._t = False
        if tag == "script":
            self._ld = False
        if not self.stack or self.stack[-1] != tag:
            err("tag mismatch </%s>, open: %s" % (tag, self.stack[-3:]))
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def handle_data(self, d):
        if self._t:
            self.title += d
        elif self._ld:
            self.ld[-1] += d
        elif not self.stack or self.stack[-1] not in ("script", "style"):
            self.text.append(d)


pages = {}
for f in sorted(WEB.rglob("*.html")):
    rel = f.relative_to(WEB).as_posix()
    p = Page()
    p.feed(f.read_text(encoding="utf-8"))
    if p.stack:
        err("%s: unclosed %s" % (rel, p.stack))
    if p.h1 != 1:
        err("%s: %d h1" % (rel, p.h1))
    pages[rel] = p

titles, descs = {}, {}
for rel, p in pages.items():
    titles.setdefault(p.title.strip(), []).append(rel)
    descs.setdefault(p.desc.strip(), []).append(rel)
for k, v in list(titles.items()) + list(descs.items()):
    if len(v) > 1:
        err("not unique (%d pages): %s" % (len(v), k[:60]))

n_links = n_assets = 0
for rel, p in pages.items():
    base = (WEB / rel).parent
    for href in p.links + p.assets:
        if href.startswith(("mailto:", "tel:")):
            continue
        if re.match(r"^[a-z]+://", href) or href.startswith("//"):
            err("%s: external reference %s" % (rel, href))
            continue
        path, frag = urldefrag(href)
        path = unquote(urlparse(path).path)
        target = (base / path).resolve() if path else (WEB / rel)
        if href in p.assets:
            n_assets += 1
        else:
            n_links += 1
        if not target.exists():
            err("%s: broken reference %s" % (rel, href))
        elif frag and target.suffix == ".html":
            tr = target.relative_to(WEB.resolve()).as_posix()
            if frag not in pages[tr].ids:
                err("%s: missing anchor %s" % (rel, href))

n_ld = 0
for rel, p in pages.items():
    vis = re.sub(r"\s+", " ", " ".join(p.text))
    for raw in p.ld:
        try:
            o = json.loads(raw)
        except ValueError:
            err("%s: JSON-LD does not parse" % rel)
            continue
        n_ld += 1
        t = o.get("@type")
        if t == "BreadcrumbList":
            for it in o["itemListElement"]:
                if it["name"] not in vis:
                    err("%s: breadcrumb text not visible: %s" % (rel, it["name"]))
            continue
        if t == "WebSite":
            continue
        checks = []
        if "name" in o:
            checks.append(o["name"])
        if "description" in o and t != "Festival":
            checks.append(o["description"])
        if t == "Festival" and rel == "index.html":
            checks.append(o["description"])
        if t == "FAQPage":
            checks += [q["name"] for q in o["mainEntity"]] + [q["acceptedAnswer"]["text"] for q in o["mainEntity"]]
        if t == "Festival" and rel == "tickets.html":
            for of in o["offers"]:
                checks += [of["name"], "€%s" % of["price"]]
        for place in ([o["location"]] if isinstance(o.get("location"), dict) else o.get("location", [])):
            checks += [place["name"], place["address"]["streetAddress"], place["address"]["postalCode"]]
        for pf in o.get("performer", []):
            checks.append(pf["name"])
        if t == "Event":
            checks += [o["startDate"][11:16], o["endDate"][11:16]]
        if t == "Place":
            checks += [o["address"]["streetAddress"], str(o["maximumAttendeeCapacity"])]
        for c in checks:
            if c and re.sub(r"\s+", " ", str(c)) not in vis:
                err("%s: JSON-LD value not visible on page: %s" % (rel, str(c)[:60]))

sm = (WEB / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>([^<]*)</loc>", sm)
for loc in locs:
    path = loc.split("/web/", 1)[1] or "index.html"
    if not (WEB / path).exists():
        err("sitemap lists missing file %s" % loc)


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


css = (WEB / "css" / "style.css").read_text(encoding="utf-8")


def tokens(block):
    return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", block))


day = tokens(re.search(r":root \{(.*?)\n\}", css, re.S).group(1))
night = dict(day)
night.update(tokens(re.search(r':root\[data-theme="night"\] \{(.*?)\n\}', css, re.S).group(1)))
pairs = [("text", "bg"), ("text", "surface"), ("muted", "bg"), ("muted", "surface"), ("primary", "bg"), ("primary", "surface"), ("on-primary", "primary"),
         ("sea", "bg"), ("sea", "surface"), ("tag-fg", "tag-bg"), ("tag-night-fg", "tag-night-bg"), ("text", "warn-bg"), ("text", "ok-bg"), ("focus", "bg"), ("bg", "sea")]
contrast = []
for name, th in (("Day", day), ("Night", night)):
    for a, b in pairs:
        r = ratio(th[a], th[b])
        contrast.append((name, a, b, r))
        need = 3.0 if a == "focus" else 4.5
        if r < need:
            err("contrast %s %s on %s = %.2f (needs %.1f)" % (name, a, b, r, need))

print("pages: %d | internal links checked: %d | assets: %d | JSON-LD blocks: %d | sitemap URLs: %d" % (len(pages), n_links, n_assets, n_ld, len(locs)))
lo = min(contrast, key=lambda x: x[3])
print("contrast pairs: %d, lowest %.2f:1 (%s %s on %s)" % (len(contrast), lo[3], lo[0], lo[1], lo[2]))
if errors:
    print("FAIL: %d problem(s)" % len(errors))
    for e in errors[:40]:
        print(" -", e)
    sys.exit(1)
print("PASS: 0 problems")
