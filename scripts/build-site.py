#!/usr/bin/env python3
"""Write the real HTML pages of the website into web/ from data.json.

Usage:  python3 scripts/build-site.py
Run it on our own computer after changing data.json or this file. The finished site
needs no build and no server: every page is plain HTML that works from file:// and on
any web host. JavaScript only improves the pages (filters, search, My Programme).
Plain Python 3, standard library only.
"""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
BASE_URL = "https://faiazyen.github.io/web-design-project/web/"   # used for canonical addresses
SITE = "Atardecer Bachata Festival"
TODAY = "2026-11-17"

D = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
F = D["festival"]
CAT = D["categories"]
VEN = {v["id"]: v for v in D["venues"]}
PER = {p["id"]: p for p in D["performers"]}
DAY = {d["id"]: d for d in D["days"]}
ITEMS = sorted(D["programmeItems"], key=lambda i: (i["start"], i["venueId"]))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

COUNTRIES = {"AR": "Argentina", "BR": "Brazil", "CL": "Chile", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba", "CZ": "Czechia", "DE": "Germany",
             "DO": "Dominican Republic", "ES": "Spain", "FR": "France", "GB": "United Kingdom", "IT": "Italy", "MA": "Morocco", "MX": "Mexico",
             "NL": "Netherlands", "PE": "Peru", "PL": "Poland", "PT": "Portugal", "SE": "Sweden", "UA": "Ukraine", "VE": "Venezuela"}


def country(code):
    return COUNTRIES.get(code, code)


def norm(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


pages_written = []   # relative paths, for the sitemap


def esc(s):
    return html.escape(str(s), quote=True)


def label(group, id_):
    for x in CAT[group]:
        if x["id"] == id_:
            return x["label"]
    return id_


def date_long(day_id):
    d = DAY[day_id]
    y, m, dd = d["date"].split("-")
    return "%s %d %s" % (d["label"], int(dd), MONTHS[int(m) - 1])


def jsonld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def abs_url(rel):
    return BASE_URL + rel


def clip(s, n=155):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


# ---------------------------------------------------------------- shared pieces
NAV = [("programme", "Programme", "programme.html"), ("performers", "Performers", "performers.html"),
       ("venues", "Venues", "venues.html"), ("roots", "Roots", "roots.html"),
       ("practical", "Practical info", "practical.html"), ("my", "My Programme", "my-programme.html")]


def header(pfx, current):
    items = "".join('<li><a href="%s%s"%s>%s</a></li>' % (pfx, href, ' aria-current="page"' if current == key else "", name) for key, name, href in NAV)
    tickets = '<li><a class="btn" href="%stickets.html"%s>Tickets</a></li>' % (pfx, ' aria-current="page"' if current == "tickets" else "")
    return ('<a class="skip-link" href="#main">Skip to main content</a>'
            '<header class="site-header"><div class="wrap header-row">'
            '<div class="bar"><a class="brand" href="%sindex.html"><img src="%simages/logo.svg" alt="" width="40" height="40"><span class="brand-name">Atardecer</span></a>'
            '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav" hidden>Menu</button></div>'
            '<div class="tools"><form class="search-form" role="search" action="%ssearch.html" method="get">'
            '<label for="site-search">Search the festival</label><input id="site-search" name="q" type="search" placeholder="Artist, session or venue" autocomplete="off">'
            '<button class="btn btn-2" type="submit">Search</button></form>'
            '<div class="auth"><span id="auth"><a href="%slogin.html">Log in / Sign up</a></span>'
            '<button class="btn btn-2 theme-btn" type="button" id="theme-btn" aria-label="Switch to night mode" hidden>Night</button></div></div></div>'
            '<nav id="main-nav" class="main-nav" aria-label="Main"><ul class="wrap">%s%s</ul></nav></header>') % (pfx, pfx, pfx, pfx, items, tickets)


def footer(pfx):
    a = VEN["ven-001"]["address"]
    return ('<footer class="site-footer"><div class="wrap">'
            '<p><strong>%s</strong><br>%s · <time datetime="2027-06-25">25</time>–<time datetime="2027-06-27">27 June 2027</time></p>'
            '<address>Contact: <a href="mailto:%s">%s</a></address>'
            '<nav aria-label="Footer"><ul><li><a href="%spractical.html">Practical info</a></li><li><a href="%stickets.html">Tickets</a></li>'
            '<li><a href="%svenues.html">Venues</a></li><li><a href="%sroots.html">Roots</a></li><li><a href="%spractical.html#code-of-conduct">Code of conduct</a></li>'
            '<li><a href="%spractical.html#accessibility">Accessibility</a></li></ul></nav>'
            '<p class="small">A fictional festival for a course project. All people, venues and organisations are invented. Illustrations are AI-generated vector drawings. '
            'Accounts and saved sessions stay in your browser.</p></div></footer>'
            '<div id="toast" class="toast" role="status" aria-live="polite"></div>') % (esc(SITE), esc(F["city"] + ", " + F["country"]), esc(F["contact"]["email"]), esc(F["contact"]["email"]), pfx, pfx, pfx, pfx, pfx, pfx)


def crumbs_html(crumbs, pfx):
    if not crumbs:
        return ""
    li = []
    for i, (name, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            li.append('<li><span aria-current="page">%s</span></li>' % esc(name))
        else:
            li.append('<li><a href="%s%s">%s</a></li>' % (pfx, href, esc(name)))
    return '<nav class="breadcrumb" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(li)


def breadcrumb_ld(crumbs, rel):
    out = []
    for i, (name, href) in enumerate(crumbs):
        out.append({"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(href if i < len(crumbs) - 1 else rel)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": out}


def page(rel, title, description, body, current="", crumbs=None, ld=None, scripts=(), data_js=False, og_type="website", h1_html=None):
    """Write one page. rel is the path inside web/, for example sessions/x.html."""
    depth = rel.count("/")
    pfx = "../" * depth
    full_title = title if title.endswith(SITE) else "%s | %s" % (title, SITE)
    ld_all = list(ld or [])
    if crumbs and len(crumbs) > 1:
        ld_all.append(breadcrumb_ld(crumbs, rel))
    scripts_html = ('<script src="%sjs/data.js"></script>' % pfx if data_js else "") + '<script src="%sjs/site.js"></script>' % pfx + "".join('<script src="%sjs/%s"></script>' % (pfx, s) for s in scripts)
    doc = ('<!doctype html>\n<html lang="en" class="no-js" data-theme="day" data-root="%s">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n'
           '<meta property="og:site_name" content="%s"><meta property="og:type" content="%s"><meta property="og:title" content="%s">'
           '<meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s">'
           '<meta property="og:image:alt" content="Sunset over the sea with the festival name"><meta property="og:locale" content="en_GB">\n'
           '<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#FFF7EC">\n'
           '<link rel="icon" href="%simages/logo.svg" type="image/svg+xml">\n<link rel="stylesheet" href="%scss/style.css">\n'
           '<script>(function(){var d=document.documentElement;d.className="js";try{var t=localStorage.getItem("atardecer.theme");if(!t&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){t="night"}if(t==="night"||t==="day"){d.setAttribute("data-theme",t)}}catch(e){}})();</script>\n'
           '%s\n</head>\n<body>\n%s\n%s<main id="main" tabindex="-1">\n%s\n</main>\n%s\n%s\n</body>\n</html>\n') % (
        pfx, esc(full_title), esc(clip(description)), esc(abs_url(rel if rel != "index.html" else "")), esc(SITE), og_type, esc(full_title), esc(clip(description)),
        esc(abs_url(rel if rel != "index.html" else "")), esc(abs_url("images/social-card.png")), pfx, pfx,
        "\n".join(jsonld(x) for x in ld_all), header(pfx, current), crumbs_html(crumbs, pfx), body, footer(pfx), scripts_html)
    path = WEB / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    pages_written.append(rel)


def tags_html(it):
    return ('<ul class="tags" aria-label="Session details"><li class="tag">%s</li><li class="tag">%s</li><li class="tag">%s</li><li class="tag tag-%s">%s</li></ul>'
            % (esc(label("types", it["type"])), esc(label("levels", it["level"])), esc(label("roleFocus", it["roleFocus"])), it["dayPart"], "Night" if it["dayPart"] == "night" else "Day"))


def time_html(it):
    d = DAY[it["dayId"]]
    late = it["start"][:10] != d["date"]
    lead = "%s night" % d["label"][:3] if late else d["label"][:3]
    return ('<p class="when"><span class="day">%s</span> <time datetime="%s">%s</time>–<time datetime="%s">%s</time>%s</p>'
            % (lead, esc(it["start"]), it["start"][11:16], esc(it["end"]), it["end"][11:16], ' <span class="late">(after midnight)</span>' if late else ""))


def session_card(it, pfx, level="h3"):
    v = VEN[it["venueId"]]
    pl = ", ".join('<a href="%sperformers/%s.html">%s</a>' % (pfx, PER[p]["slug"], esc(PER[p]["name"])) for p in it["performerIds"])
    return ('<article class="session" data-id="%s" data-day="%s" data-venue="%s" data-type="%s" data-level="%s" data-role="%s" data-daypart="%s">'
            '%s<div class="session-main"><%s class="session-title"><a href="%ssessions/%s.html">%s</a></%s>%s'
            '<p class="meta"><a href="%svenues/%s.html">%s</a> · With %s</p></div>'
            '<div class="session-actions"><button class="btn btn-2 btn-small" type="button" data-save="%s" data-title="%s" aria-pressed="false" hidden>Save</button></div></article>') % (
        it["id"], it["dayId"], it["venueId"], it["type"], it["level"], it["roleFocus"], it["dayPart"], time_html(it), level, pfx, it["slug"], esc(it["title"]), level,
        tags_html(it), pfx, v["slug"], esc(v["name"]), pl, it["id"], esc(it["title"]))


def avatar_img(p, pfx, size=72, lazy=True, alt=None):
    return '<img class="avatar" src="%s%s" alt="%s" width="%d" height="%d"%s>' % (pfx, esc(p["image"]["src"]), esc(alt if alt is not None else ""), size, size, ' loading="lazy"' if lazy else "")


def performer_ld(p, rel_url, full=True):
    members = [{"@type": "Person", "name": m} for m in p["members"]]
    t = "Person" if (p["type"] in ("dj", "singer") or (p["type"] == "instructor" and not members)) else "PerformingGroup"
    o = {"@context": "https://schema.org", "@type": t, "name": p["name"], "url": abs_url(rel_url)}
    if full:
        o["description"] = p["bio"]
    if members:
        o["member"] = members
    return o


def place_ld(v):
    a = v["address"]
    return {"@type": "Place", "name": v["name"], "address": {"@type": "PostalAddress", "streetAddress": a["streetAddress"], "postalCode": a["postalCode"],
            "addressLocality": a["addressLocality"], "addressRegion": a["addressRegion"], "addressCountry": a["addressCountry"]}}


def address_html(v):
    a = v["address"]
    return "<address>%s<br>%s %s<br>%s</address>" % (esc(a["streetAddress"]), esc(a["postalCode"]), esc(a["addressLocality"]), esc(a["addressRegion"]))


def hero_svg():
    return ('<svg class="hero-art" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sky-1)"/><stop offset="0.6" style="stop-color:var(--sky-2)"/>'
            '<stop offset="1" style="stop-color:var(--sky-3)"/></linearGradient><radialGradient id="sun" cx="0.4" cy="0.4" r="0.7"><stop offset="0" style="stop-color:var(--sun-core)"/>'
            '<stop offset="1" style="stop-color:var(--sun)"/></radialGradient></defs>'
            '<rect width="1200" height="520" fill="url(#sky)"/><circle class="sun" cx="900" cy="350" r="105" fill="url(#sun)"/>'
            '<path d="M-20 400 Q300 340 600 395 T1220 385 V520 H-20 Z" style="fill:var(--wave-1)"/><path d="M-20 450 Q320 400 640 452 T1220 440 V520 H-20 Z" style="fill:var(--wave-2)"/>'
            '<g style="fill:var(--bg)" opacity="0.92"><rect x="1010" y="352" width="16" height="64" rx="8"/><rect x="1032" y="338" width="16" height="78" rx="8"/>'
            '<rect x="1054" y="356" width="16" height="60" rx="8"/><rect x="1076" y="344" width="16" height="72" rx="8"/></g></svg>')


# ---------------------------------------------------------------- pages
def build_home():
    feat = [p for p in D["performers"] if p["featured"]]
    opening = [i for i in ITEMS if i["dayId"] == "day-fri" and i["type"] == "social" and i["venueId"] == "ven-003"][0]
    venues = "".join('<article class="card venue-card"><img class="venue-img" src="images/venues/%s.svg" alt="%s" width="800" height="500" loading="lazy">'
                     '<h3><a href="venues/%s.html">%s</a></h3><p class="meta">%s · capacity %s</p>%s</article>' % (
                         v["slug"], esc(v["image"]["alt"]), v["slug"], esc(v["name"]), esc(v["setting"].capitalize()), v["capacity"], address_html(v)) for v in D["venues"])
    artists = "".join('<li class="card artist">%s<h3><a href="performers/%s.html">%s</a></h3><p class="meta">%s · %s</p></li>' % (
        avatar_img(p, "", 72), p["slug"], esc(p["name"]), esc(label("performerTypes", p["type"])), esc(country(p["country"]))) for p in feat)
    body = ('<section class="hero" aria-labelledby="hero-title">%s<div class="hero-card"><p class="eyebrow">%s</p><h1 id="hero-title">%s</h1>'
            '<p class="lede">Three days of bachata in Valencia. Sea by day, club by night.</p>'
            '<p class="dates"><strong><time datetime="2027-06-25">25</time>–<time datetime="2027-06-27">27 June 2027</time></strong> · Valencia, Spain</p>'
            '<p class="btn-row"><a class="btn" href="programme.html">See the programme</a><a class="btn btn-2" href="tickets.html">Tickets</a></p></div></section>'
            '<p class="lede intro">%s</p><ul class="stats" aria-label="The festival in numbers"><li><strong>3</strong> days</li><li><strong>%d</strong> venues</li><li><strong>%d</strong> performers</li><li><strong>%d</strong> sessions</li></ul>'
            '<section aria-labelledby="moods"><h2 id="moods">Pick your mood</h2><div class="grid grid-2">'
            '<article class="card"><h3>Sea by day</h3><p>Workshops by level, sand socials and the daily sunset social. Sessions that start before 20:00.</p><p><a class="btn btn-2" href="programme.html?daypart=day">Show day sessions</a></p></article>'
            '<article class="card"><h3>Club by night</h3><p>Shows, DJs and live music, late into the morning. Sessions that start at 20:00 or later.</p><p><a class="btn btn-2" href="programme.html?daypart=night">Show night sessions</a></p></article></div></section>'
            '<section aria-labelledby="opening"><h2 id="opening">Opening night</h2>%s</section>'
            '<section aria-labelledby="where"><h2 id="where">Where it happens</h2><div class="grid grid-3">%s</div></section>'
            '<section aria-labelledby="artists"><h2 id="artists">Featured artists</h2><ul class="grid grid-3 plain">%s</ul><p><a href="performers.html">See all %d performers</a></p></section>'
            '<section aria-labelledby="plan"><h2 id="plan">Plan your visit</h2><div class="grid grid-3">'
            '<article class="card"><h3>Tickets</h3><p>Four passes, from a single Saturday to the full three days.</p><p><a href="tickets.html">Compare passes</a></p></article>'
            '<article class="card"><h3>Getting here and staying</h3><p>Flights, trains, hotels and access facts for every venue.</p><p><a href="practical.html">Practical info</a></p></article>'
            '<article class="card"><h3>My Programme</h3><p>Save sessions to your own schedule. We warn you if two overlap.</p><p><a href="my-programme.html">Open My Programme</a></p></article></div></section>'
            '<section aria-labelledby="roots"><h2 id="roots">The roots of bachata</h2><p>Bachata began in the Dominican Republic. Read the story, from the first recordings to today, and meet the instruments.</p><p><a href="roots.html">Read the Roots story</a></p></section>') % (
        hero_svg(), esc(F["editionLabel"]), esc(SITE), esc(F["description"]), len(D["venues"]), len(D["performers"]), len(D["programmeItems"]), session_card(opening, ""), venues, artists, len(D["performers"]))
    ld = [{"@context": "https://schema.org", "@type": "Festival", "name": SITE, "description": F["description"], "startDate": F["startDate"], "endDate": F["endDate"],
           "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
           "location": [place_ld(v) for v in D["venues"]], "image": abs_url("images/social-card.png"), "url": abs_url(""),
           "organizer": {"@type": "Organization", "name": SITE, "email": F["contact"]["email"]}},
          {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": abs_url(""),
           "potentialAction": {"@type": "SearchAction", "target": abs_url("search.html?q={search_term_string}"), "query-input": "required name=search_term_string"}}]
    page("index.html", "Bachata festival in Valencia, 25–27 June 2027",
         "Atardecer Bachata Festival: three days of bachata in Valencia, 25–27 June 2027. Workshops by level, sand socials, club nights and shows. Plan your own programme.",
         body, current="", ld=ld)


def build_programme():
    groups = ""
    for d in D["days"]:
        its = [i for i in ITEMS if i["dayId"] == d["id"]]
        groups += '<section class="day-group" data-day="%s" aria-labelledby="g-%s"><h2 id="g-%s">%s <span class="meta">(<span class="day-count">%d</span>)</span></h2><div class="session-list">%s</div></section>' % (
            d["id"], d["id"], d["id"], esc(date_long(d["id"])), len(its), "".join(session_card(i, "") for i in its))

    def sel(id_, name, lab, first, opts):
        return '<div class="field"><label for="%s">%s</label><select id="%s" name="%s"><option value="">%s</option>%s</select></div>' % (
            id_, lab, id_, name, first, "".join('<option value="%s">%s</option>' % (esc(v), esc(t)) for v, t in opts))
    form = ('<details class="filters" id="filters" open><summary>Filters <span id="filter-badge"></span></summary>'
            '<form id="filter-form" action="programme.html" method="get"><fieldset><legend class="vh">Filter the sessions</legend>%s%s%s%s%s%s'
            '<button type="button" class="btn btn-2" id="clear">Clear all filters</button></fieldset></form></details>') % (
        sel("f-day", "day", "Day", "All days", [(d["id"], date_long(d["id"])) for d in D["days"]]),
        sel("f-venue", "venue", "Venue", "All venues", [(v["id"], v["name"]) for v in D["venues"]]),
        sel("f-type", "type", "Type", "All types", [(t["id"], t["label"]) for t in CAT["types"]]),
        sel("f-level", "level", "Level", "All levels", [(t["id"], t["label"]) for t in CAT["levels"]]),
        sel("f-role", "role", "Role focus", "Any role", [(t["id"], t["label"]) for t in CAT["roleFocus"]]),
        sel("f-daypart", "daypart", "Day or night", "Day and night", [(t["id"], t["label"]) for t in CAT["dayParts"]]))
    body = ('<h1>Programme</h1><p class="lede">Friday 25 to Sunday 27 June 2027. All %d sessions are listed below. Filter the list, open a session, or save it to My Programme.</p>'
            '<div class="layout-programme"><aside aria-label="Filters">%s</aside><section aria-labelledby="results-title"><h2 id="results-title" class="vh">Sessions</h2>'
            '<p class="count" id="count" role="status" aria-live="polite">Showing all %d sessions</p>'
            '<div id="none" class="empty" hidden><p><strong>No sessions match these filters.</strong></p><p>Try a different level or role, or clear all filters.</p></div>%s</section></div>') % (
        len(ITEMS), form, len(ITEMS), groups)
    page("programme.html", "Programme: workshops, socials and shows",
         "The full programme of the Atardecer Bachata Festival, 25–27 June 2027 in Valencia: %d workshops, socials and shows. Filter by day, venue, type, level and role." % len(ITEMS),
         body, current="programme", crumbs=[("Home", "index.html"), ("Programme", "programme.html")], scripts=("programme.js",))


def build_sessions():
    for it in ITEMS:
        v = VEN[it["venueId"]]
        lvl = [l for l in CAT["levels"] if l["id"] == it["level"]][0]
        perf = "".join('<li class="card artist-row">%s<div><h3><a href="../performers/%s.html">%s</a></h3><p class="meta">%s · %s</p></div></li>' % (
            avatar_img(PER[p], "../", 56), PER[p]["slug"], esc(PER[p]["name"]), esc(label("performerTypes", PER[p]["type"])), esc(country(PER[p]["country"]))) for p in it["performerIds"])
        others = [o for o in ITEMS if o["venueId"] == it["venueId"] and o["dayId"] == it["dayId"] and o["id"] != it["id"]][:4]
        more = ("<h2>Also at %s that day</h2><ul>%s</ul>" % (esc(v["name"]), "".join('<li><a href="%s.html">%s %s</a></li>' % (o["slug"], o["start"][11:16], esc(o["title"])) for o in others))) if others else ""
        crumbs = [("Home", "index.html"), ("Programme", "programme.html"), (it["title"], "sessions/%s.html" % it["slug"])]
        body = ('<article><h1>%s</h1>%s%s<div class="layout-detail"><div><p>%s</p><p class="btn-row"><button class="btn" type="button" data-save="%s" data-title="%s" aria-pressed="false" hidden>Save</button>'
                '<a class="btn btn-2" href="../my-programme.html">Open My Programme</a></p><h2>Who is on</h2><ul class="plain">%s</ul></div>'
                '<aside aria-labelledby="facts"><h2 id="facts">Facts</h2><dl class="facts"><dt>Day</dt><dd>%s</dd><dt>Where</dt><dd><a href="../venues/%s.html">%s</a>%s</dd><dt>Type</dt><dd>%s</dd>'
                '<dt>Level</dt><dd>%s<br><small>%s</small></dd><dt>Role focus</dt><dd>%s</dd><dt>Style</dt><dd>%s</dd><dt>Places</dt><dd>%s</dd></dl>%s</aside></div></article>') % (
            esc(it["title"]), time_html(it), tags_html(it), esc(it["description"]), it["id"], esc(it["title"]), perf, esc(date_long(it["dayId"])), v["slug"], esc(v["name"]), address_html(v),
            esc(label("types", it["type"])), esc(lvl["label"]), esc(lvl["description"]), esc(label("roleFocus", it["roleFocus"])), esc(label("styles", it["style"])),
            esc(it["capacity"]) if it["capacity"] else "Open, no booking needed", more)
        ld = [{"@context": "https://schema.org", "@type": "Event", "name": it["title"], "description": it["description"], "startDate": it["start"], "endDate": it["end"],
               "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "location": place_ld(v),
               "performer": [performer_ld(PER[p], "performers/%s.html" % PER[p]["slug"], full=False) for p in it["performerIds"]],
               "superEvent": {"@type": "Festival", "name": SITE, "url": abs_url("")}, "url": abs_url("sessions/%s.html" % it["slug"])}]
        for x in ld[0]["performer"]:
            x.pop("@context", None)
        page("sessions/%s.html" % it["slug"], it["title"], "%s, %s %s–%s at %s, Valencia. %s" % (it["title"], DAY[it["dayId"]]["label"], it["start"][11:16], it["end"][11:16], v["name"], it["description"]),
             body, current="programme", crumbs=crumbs, ld=ld, og_type="article")


def build_performers():
    cards = "".join('<li class="card artist" data-name="%s" data-type="%s">%s<h3><a href="performers/%s.html">%s</a></h3><p class="meta">%s · %s · %d %s</p></li>' % (
        esc(norm(p["name"] + " " + " ".join(p["members"]))), p["type"], avatar_img(p, "", 72), p["slug"], esc(p["name"]), esc(label("performerTypes", p["type"])),
        esc(country(p["country"])), len([i for i in ITEMS if p["id"] in i["performerIds"]]), "session" if len([i for i in ITEMS if p["id"] in i["performerIds"]]) == 1 else "sessions") for p in D["performers"])
    types = "".join('<option value="%s">%s</option>' % (t["id"], esc(t["label"])) for t in CAT["performerTypes"])
    body = ('<h1>Performers</h1><p class="lede">%d instructors, DJs, bands, singers and show teams. Open an artist to see every session they play or teach.</p>'
            '<form id="pf" class="filter-row" role="search" aria-label="Filter performers" action="performers.html" method="get"><div class="field"><label for="p-name">Find an artist by name</label>'
            '<input id="p-name" name="name" type="search" autocomplete="off"></div><div class="field"><label for="p-type">Type</label><select id="p-type" name="type"><option value="">All types</option>%s</select></div></form>'
            '<p class="count" id="count" role="status" aria-live="polite">Showing all %d performers</p><div id="none" class="empty" hidden><p><strong>No performer matches.</strong></p><p>Try fewer letters or choose All types.</p></div>'
            '<h2 class="vh">All performers</h2><ul class="grid grid-3 plain" id="list">%s</ul>') % (len(D["performers"]), types, len(D["performers"]), cards)
    page("performers.html", "Performers: instructors, DJs, bands and show teams",
         "Meet the %d performers of the Atardecer Bachata Festival: instructors, DJs, bands, singers and show teams. Find an artist and see all their sessions." % len(D["performers"]),
         body, current="performers", crumbs=[("Home", "index.html"), ("Performers", "performers.html")], scripts=("performers.js",))
    for p in D["performers"]:
        its = [i for i in ITEMS if p["id"] in i["performerIds"]]
        styles = ", ".join(label("styles", s) for s in p["styles"])
        sess = "".join(session_card(i, "../") for i in its)
        body = ('<article><div class="layout-detail"><div><h1>%s</h1><ul class="tags" aria-label="About this performer"><li class="tag">%s</li><li class="tag">%s</li></ul><p>%s</p>%s<p><strong>Styles:</strong> %s</p></div>'
                '<div>%s</div></div><section aria-labelledby="s"><h2 id="s">%s</h2><div class="session-list">%s</div></section></article>') % (
            esc(p["name"]), esc(label("performerTypes", p["type"])), esc(country(p["country"])), esc(p["bio"]),
            ("<p><strong>Dancers:</strong> %s</p>" % " and ".join(esc(m) for m in p["members"])) if p["members"] else "", esc(styles),
            avatar_img(p, "../", 160, lazy=False, alt=p["image"]["alt"]), "Session" if len(its) == 1 else "All %d sessions" % len(its), sess)
        rel = "performers/%s.html" % p["slug"]
        page(rel, p["name"], "%s, %s from %s at the Atardecer Bachata Festival. %s %d %s on the programme." % (
            p["name"], label("performerTypes", p["type"]).lower(), p["country"], p["bio"], len(its), "session" if len(its) == 1 else "sessions"),
             body, current="performers", crumbs=[("Home", "index.html"), ("Performers", "performers.html"), (p["name"], rel)], ld=[performer_ld(p, rel)], og_type="profile")


def build_venues():
    cards = ""
    for v in D["venues"]:
        a = v["accessibility"]
        n = len([i for i in ITEMS if i["venueId"] == v["id"]])
        yn = lambda b: "Yes" if b else "No"
        cards += ('<article class="card venue-card"><img class="venue-img" src="images/venues/%s.svg" alt="%s" width="800" height="500" loading="lazy"><h2><a href="venues/%s.html">%s</a></h2>'
                  '<p class="meta">%s · capacity %s · %d sessions</p><p>%s</p>%s<dl class="facts"><dt>Step-free</dt><dd>%s</dd><dt>Accessible toilets</dt><dd>%s</dd><dt>Quiet space</dt><dd>%s</dd></dl>'
                  '<p><a class="btn btn-2 btn-small" href="venues/%s.html">Venue details</a> <a class="btn btn-2 btn-small" href="programme.html?venue=%s">See sessions here</a></p></article>') % (
            v["slug"], esc(v["image"]["alt"]), v["slug"], esc(v["name"]), esc(v["setting"].capitalize()), v["capacity"], n, esc(v["description"]), address_html(v), yn(a["stepFree"]), yn(a["accessibleToilets"]), yn(a["quietSpace"]), v["slug"], v["id"])
    body = '<h1>Venues</h1><p class="lede">Three venues within a short walk of each other along the beachfront: sand and sea by day, club floor by night.</p><div class="grid grid-3">%s</div>' % cards
    page("venues.html", "Venues: beach stage, pavilion and club in Valencia",
         "The three venues of the Atardecer Bachata Festival in Valencia: Arena Stage on the beach, Pabellón Brisa and Marea Club, with addresses and access facts.",
         body, current="venues", crumbs=[("Home", "index.html"), ("Venues", "venues.html")])
    for v in D["venues"]:
        a = v["accessibility"]
        its = [i for i in ITEMS if i["venueId"] == v["id"]]
        rows = "".join('<li><span class="day">%s</span> <time datetime="%s">%s</time> <a href="../sessions/%s.html">%s</a></li>' % (DAY[i["dayId"]]["label"][:3], esc(i["start"]), i["start"][11:16], i["slug"], esc(i["title"])) for i in its)
        body = ('<article><div class="layout-detail"><div><h1>%s</h1><p class="lede">%s</p><h2>Access</h2><ul><li>Step-free: %s</li><li>Accessible toilets: %s</li><li>Quiet space: %s</li></ul><p>%s</p></div>'
                '<aside aria-labelledby="f"><img class="venue-img" src="../images/venues/%s.svg" alt="%s" width="800" height="500"><h2 id="f">Find it</h2>%s'
                '<dl class="facts"><dt>Setting</dt><dd>%s</dd><dt>Capacity</dt><dd>%s</dd><dt>Coordinates</dt><dd>%s, %s</dd></dl></aside></div>'
                '<section aria-labelledby="s"><h2 id="s">Sessions here (%d)</h2><ul class="plain compact">%s</ul><p><a href="../programme.html?venue=%s">Filter the programme to this venue</a></p></section></article>') % (
            esc(v["name"]), esc(v["description"]), "Yes" if a["stepFree"] else "No", "Yes" if a["accessibleToilets"] else "No", "Yes" if a["quietSpace"] else "No",
            esc(a["notes"]), v["slug"], esc(v["image"]["alt"]), address_html(v), esc(v["setting"].capitalize()), v["capacity"], v["geo"]["latitude"], v["geo"]["longitude"], len(its), rows, v["id"])
        rel = "venues/%s.html" % v["slug"]
        pl = place_ld(v)
        pl.update({"@context": "https://schema.org", "description": v["description"], "maximumAttendeeCapacity": v["capacity"],
                   "geo": {"@type": "GeoCoordinates", "latitude": v["geo"]["latitude"], "longitude": v["geo"]["longitude"]},
                   "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "Step-free access", "value": a["stepFree"]},
                                      {"@type": "LocationFeatureSpecification", "name": "Accessible toilets", "value": a["accessibleToilets"]},
                                      {"@type": "LocationFeatureSpecification", "name": "Quiet space", "value": a["quietSpace"]}]})
        page(rel, v["name"], "%s in Valencia: %s Access facts and %d sessions at the Atardecer Bachata Festival." % (v["name"], v["description"], len(its)), body, current="venues",
             crumbs=[("Home", "index.html"), ("Venues", "venues.html"), (v["name"], rel)], ld=[pl])


def build_practical():
    tr = "".join('<li class="card"><h3>%s</h3><p>%s</p></li>' % (esc(t["title"]), esc(t["text"])) for t in F["travel"])
    acc = "".join("<tr><th scope=\"row\">%s</th><td data-label=\"Type\">%s</td><td data-label=\"Distance to venues\">%s km</td><td data-label=\"Price\">from €%s</td><td data-label=\"Notes\">%s</td></tr>" % (esc(x["name"]), esc(x["type"].capitalize()), esc(x["distanceToVenuesKm"]), esc(x["priceFromPerNight"]), esc(x["notes"])) for x in F["accommodation"])
    faq = "".join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (esc(q["question"]), esc(q["answer"])) for q in F["faq"])
    coc = F["codeOfConduct"]
    feats = "".join("<li>%s</li>" % esc(x) for x in F["accessibility"]["features"])
    sus = "".join("<li>%s</li>" % esc(x) for x in F["sustainability"]["commitments"])
    princ = "".join("<li>%s</li>" % esc(x) for x in coc["principles"])
    body = ('<h1>Practical info</h1><p class="lede">Everything you need before you land in Valencia: how to get here, where to stay, access, answers and the code of conduct.</p>'
            '<nav class="onpage" aria-label="On this page"><ul><li><a href="#travel">Travel</a></li><li><a href="#accommodation">Accommodation</a></li><li><a href="#accessibility">Accessibility</a></li>'
            '<li><a href="#faq">FAQ</a></li><li><a href="#code-of-conduct">Code of conduct</a></li><li><a href="tickets.html">Tickets</a></li></ul></nav>'
            '<section id="travel" aria-labelledby="h-travel"><h2 id="h-travel">Travel</h2><ul class="grid grid-2 plain">%s</ul><h3>Getting here lightly</h3><p>%s</p><ul>%s</ul></section>'
            '<section id="accommodation" aria-labelledby="h-acc"><h2 id="h-acc">Accommodation</h2><p>Places to stay near the venues. Prices are examples, per night.</p>'
            '<div class="table-wrap"><table><caption>Where to stay</caption><thead><tr><th scope="col">Place</th><th scope="col">Type</th><th scope="col">Distance to venues</th><th scope="col">Price</th><th scope="col">Notes</th></tr></thead><tbody>%s</tbody></table></div></section>'
            '<section id="accessibility" aria-labelledby="h-a11y"><h2 id="h-a11y">Accessibility</h2><p>%s</p><ul>%s</ul><p>See the access facts for each venue on the <a href="venues.html">Venues</a> page.</p></section>'
            '<section id="faq" aria-labelledby="h-faq"><h2 id="h-faq">Frequently asked questions</h2>%s</section>'
            '<section id="code-of-conduct" aria-labelledby="h-coc"><h2 id="h-coc">Code of conduct</h2><p>%s</p><ol>%s</ol><p>To report a problem, tell any staff member or write to <a href="mailto:%s">%s</a>.</p></section>') % (
        tr, esc(F["sustainability"]["summary"]), sus, acc, esc(F["accessibility"]["summary"]), feats, faq, esc(coc["summary"]), princ, esc(coc["reportContact"]), esc(coc["reportContact"]))
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["question"], "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}} for q in F["faq"]]}]
    page("practical.html", "Practical info: travel, accommodation, access, FAQ and code of conduct",
         "Plan your trip to the Atardecer Bachata Festival in Valencia: travel options, places to stay, accessibility, answers to common questions and the code of conduct.",
         body, current="practical", crumbs=[("Home", "index.html"), ("Practical info", "practical.html")], ld=ld)


def build_tickets():
    rows = "".join('<tr><th scope="row">%s</th><td data-label="Price">€%s</td><td data-label="Includes"><ul>%s</ul></td><td data-label="Notes">%s</td></tr>' % (esc(t["name"]), esc(t["price"]), "".join("<li>%s</li>" % esc(x) for x in t["includes"]), esc(t["notes"])) for t in F["tickets"])
    body = ('<h1>Tickets</h1><p class="lede">Four passes for the Atardecer Bachata Festival, 25–27 June 2027. The Full Pass costs €%s and includes every workshop, social and show.</p>'
            '<div class="table-wrap"><table><caption>Passes and prices</caption><thead><tr><th scope="col">Pass</th><th scope="col">Price</th><th scope="col">Includes</th><th scope="col">Notes</th></tr></thead><tbody>%s</tbody></table></div>'
            '<section aria-labelledby="buy"><h2 id="buy">How to buy</h2><p>This is a course project, so there is no real ticket sale. In a real festival the buttons here would lead to a checkout. Questions about groups: <a href="mailto:%s">%s</a>.</p>'
            '<p><a href="programme.html">Choose your sessions first</a> and see what each pass covers.</p></section>') % (esc(F["tickets"][0]["price"]), rows, esc(F["contact"]["email"]), esc(F["contact"]["email"]))
    offers = [{"@type": "Offer", "name": t["name"], "price": t["price"], "priceCurrency": t["currency"], "url": abs_url("tickets.html")} for t in F["tickets"]]
    ld = [{"@context": "https://schema.org", "@type": "Festival", "name": SITE, "startDate": F["startDate"], "endDate": F["endDate"], "location": [place_ld(v) for v in D["venues"]], "offers": offers}]
    page("tickets.html", "Tickets and prices", "Compare the four passes for the Atardecer Bachata Festival, Valencia, 25–27 June 2027: Full Pass €%s, Party Pass, Saturday Day Pass and Group Pass." % F["tickets"][0]["price"],
         body, current="tickets", crumbs=[("Home", "index.html"), ("Practical info", "practical.html"), ("Tickets", "tickets.html")], ld=ld)


def build_roots():
    R = F["roots"]
    tl = "".join('<li><strong class="year">%s</strong><span>%s</span></li>' % (esc(t["year"]), esc(t["text"])) for t in R["timeline"])
    ins = "".join("<dt>%s</dt><dd>%s</dd>" % (esc(i["name"]), esc(i["text"])) for i in R["instruments"])
    body = ('<h1>Roots: the story of bachata dominicana</h1><p class="lede">%s</p><section aria-labelledby="t"><h2 id="t">A short timeline</h2><ol class="timeline">%s</ol></section>'
            '<section aria-labelledby="i"><h2 id="i">The sound</h2><dl class="facts wide">%s</dl></section><p><a class="btn" href="programme.html">Find a roots session in the programme</a></p>') % (esc(R["intro"]), tl, ins)
    page("roots.html", "Roots: the story of bachata dominicana", "The story of bachata dominicana from the first recordings in the Dominican Republic to the festivals of today, with a short timeline and the instruments that make the sound.",
         body, current="roots", crumbs=[("Home", "index.html"), ("Roots", "roots.html")])


def build_dynamic():
    page("search.html", "Search", "Search the Atardecer Bachata Festival for sessions, performers and venues.",
         '<h1>Search results</h1><div id="results" aria-live="polite"><p>Type a name, a session or a venue in the search box at the top of the page.</p></div>'
         '<noscript><p>Search needs JavaScript. You can browse instead: <a href="programme.html">programme</a>, <a href="performers.html">performers</a>, <a href="venues.html">venues</a>.</p></noscript>'
         '<section aria-labelledby="pop"><h2 id="pop">Popular searches</h2><ul><li><a href="search.html?q=beginner">beginner</a></li><li><a href="search.html?q=guitar">guitar</a></li>'
         '<li><a href="search.html?q=marisol">marisol</a></li><li><a href="search.html?q=sunset">sunset</a></li></ul></section>',
         current="", crumbs=[("Home", "index.html"), ("Search results", "search.html")], data_js=True, scripts=("search.js",))
    page("my-programme.html", "My Programme", "Your personal programme for the Atardecer Bachata Festival: saved sessions, clash warnings and a calendar download.",
         '<h1>My Programme</h1><div id="content"><p>This page shows the sessions you saved. It needs JavaScript and a browser that allows storage.</p></div>',
         current="my", crumbs=[("Home", "index.html"), ("My Programme", "my-programme.html")], data_js=True, scripts=("my-programme.js",))
    page("login.html", "Log in / Sign up", "Demo sign-up and login for My Programme at the Atardecer Bachata Festival. Nothing leaves your browser.",
         '<h1>Log in / Sign up</h1><p class="banner" id="reason" hidden></p><p class="banner"><strong>Demo only.</strong> Nothing leaves your browser. Do not use a real password. The password is accepted but never stored.</p>'
         '<div class="layout-two"><form id="signup" novalidate aria-labelledby="su-title"><fieldset><legend id="su-title">New here? Sign up</legend><p class="hint">All fields are required.</p>'
         '<div class="field"><label for="su-name">Name</label><input id="su-name" name="name" type="text" required autocomplete="given-name" aria-describedby="su-name-err"><p class="error" role="alert" id="su-name-err" hidden></p></div>'
         '<div class="field"><label for="su-email">Email</label><input id="su-email" name="email" type="email" required autocomplete="email" aria-describedby="su-email-err"><p class="error" role="alert" id="su-email-err" hidden></p></div>'
         '<div class="field"><label for="su-pass">Demo password</label><input id="su-pass" name="password" type="password" required autocomplete="new-password" aria-describedby="su-pass-hint su-pass-err"><p class="hint" id="su-pass-hint">Any text. It is not stored.</p><p class="error" role="alert" id="su-pass-err" hidden></p></div>'
         '<button class="btn" type="submit">Create demo account</button></fieldset></form>'
         '<form id="login" novalidate aria-labelledby="li-title"><fieldset><legend id="li-title">Already have an account? Log in</legend>'
         '<div class="field"><label for="li-email">Email</label><input id="li-email" name="email" type="email" required autocomplete="email" aria-describedby="li-email-err"><p class="error" role="alert" id="li-email-err" hidden></p></div>'
         '<div class="field"><label for="li-pass">Demo password</label><input id="li-pass" name="password" type="password" required autocomplete="current-password" aria-describedby="li-pass-err"><p class="error" role="alert" id="li-pass-err" hidden></p></div>'
         '<button class="btn" type="submit">Log in</button></fieldset></form></div>',
         current="", crumbs=[("Home", "index.html"), ("Log in / Sign up", "login.html")], scripts=("login.js",))


def build_files():
    urls = [("" if r == "index.html" else r) for r in pages_written]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (esc(abs_url(u)), TODAY) for u in urls if u not in ("my-programme.html", "login.html")) + "</urlset>\n"
    (WEB / "sitemap.xml").write_text(sm, encoding="utf-8")
    (WEB / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /web-design-project/web/my-programme.html\nDisallow: /web-design-project/web/login.html\nSitemap: %s\n" % abs_url("sitemap.xml"), encoding="utf-8")
    llms = ["# %s" % SITE, "", "> %s" % F["description"], "", "Fictional festival for a course project. 3 days (25-27 June 2027), %d venues in Valencia, %d performers, %d sessions." % (len(D["venues"]), len(D["performers"]), len(D["programmeItems"])),
            "", "## Key pages", "- [Programme](%s): all sessions, filterable by day, venue, type, level, role" % abs_url("programme.html"), "- [Performers](%s): instructors, DJs, bands, singers, show teams" % abs_url("performers.html"),
            "- [Venues](%s): Arena Stage, Pabellón Brisa, Marea Club, with access facts" % abs_url("venues.html"), "- [Tickets](%s): four passes, Full Pass EUR %s" % (abs_url("tickets.html"), F["tickets"][0]["price"]),
            "- [Practical info](%s): travel, accommodation, accessibility, FAQ, code of conduct" % abs_url("practical.html"), "- [Roots](%s): story of bachata dominicana" % abs_url("roots.html"),
            "", "## Facts", "- Name: %s, %s" % (SITE, F["editionLabel"]), "- Dates: %s to %s" % (F["startDate"], F["endDate"]), "- Location: %s, %s" % (F["city"], F["country"]),
            "- Styles: " + ", ".join(F["genres"]), "- Contact: %s" % F["contact"]["email"], "", "## Notes", "- Every session, performer and venue has its own page with structured data (JSON-LD).", "- Accounts and saved sessions are a browser-only demo, not real accounts.", ""]
    (WEB / "llms.txt").write_text("\n".join(llms), encoding="utf-8")


def main():
    for old in list((WEB / "sessions").glob("*.html")) + list((WEB / "performers").glob("*.html")) + list((WEB / "venues").glob("*.html")):
        old.unlink()
    build_home(); build_programme(); build_sessions(); build_performers(); build_venues(); build_practical(); build_tickets(); build_roots(); build_dynamic(); build_files()
    print("wrote %d pages into web/ (+ sitemap.xml, robots.txt, llms.txt)" % len(pages_written))


if __name__ == "__main__":
    main()
