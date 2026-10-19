#!/usr/bin/env python3
"""Validate data.json (Atardecer Bachata Festival).

Usage:  python3 scripts/validate-data.py [path/to/data.json]
Exit code 0 = all checks pass, 1 = at least one error.
Plain Python 3, standard library only.
"""
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data.json"

MIN_DAYS, MIN_VENUES, MIN_PERFORMERS, MIN_ITEMS = 3, 2, 64, 65
FEST_START, FEST_END = "2027-06-25", "2027-06-27"
OFFSET = "+02:00"
ENUMS = {
    "type": {"workshop", "show", "social"},
    "level": {"beginner", "intermediate", "advanced", "all-levels"},
    "roleFocus": {"lead", "follow", "both"},
    "style": {"dominicana", "sensual", "moderna", "salsa"},
    "dayPart": {"day", "night"},
    "performerType": {"instructor", "dj", "band", "singer", "show-team"},
    "venueKind": {"beach-stage", "pavilion", "club"},
    "venueSetting": {"outdoor", "indoor"},
}
# Well-known real bachata artists. No performer may match any of these.
REAL_ARTISTS = [
    "romeo santos", "aventura", "prince royce", "anthony santos", "antony santos", "zacarias ferreira",
    "luis vargas", "juan luis guerra", "raulin rodriguez", "monchy", "alexandra", "frank reyes", "joe veras",
    "xtreme", "grupo extra", "toby love", "leslie grace", "carlos & paz", "marco & sara", "daniel & desiree",
    "korke", "judith", "ataca", "la alemana", "bachatu", "edwards", "ana & edu", "melvin & gatica",
    "gero & migle", "sergio martin", "cesar guerra", "terrance xin", "pablo g", "daniel jove",
]

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def parse_dt(value, where):
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        err("%s: not a valid ISO 8601 datetime: %r" % (where, value))
        return None
    if not str(value).endswith(OFFSET):
        err("%s: datetime must end with offset %s: %r" % (where, OFFSET, value))
    return dt


def need(obj, fields, where):
    for f in fields:
        if f not in obj or obj[f] in (None, "", []):
            if f in ("capacity", "members", "tags") and f in obj:
                continue
            err("%s: missing or empty field %r" % (where, f))


def check_images(obj, where):
    img = obj.get("image")
    if not isinstance(img, dict):
        err("%s: image object missing" % where)
        return
    for f in ("src", "alt", "credit", "source"):
        if not img.get(f):
            err("%s: image.%s missing" % (where, f))


def check_unique(rows, entity, id_prefix):
    ids, slugs = set(), set()
    for r in rows:
        rid, slug = r.get("id"), r.get("slug")
        if not re.fullmatch(r"%s-\d{3}" % re.escape(id_prefix), str(rid)):
            err("%s %r: id must look like %s-001" % (entity, rid, id_prefix))
        if rid in ids:
            err("%s: duplicate id %r" % (entity, rid))
        ids.add(rid)
        if not slug or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(slug)):
            err("%s %r: invalid slug %r" % (entity, rid, slug))
        if slug in slugs:
            err("%s: duplicate slug %r" % (entity, slug))
        slugs.add(slug)
    return ids


def main():
    try:
        data = json.loads(PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: %s not found" % PATH)
        return 1
    except json.JSONDecodeError as e:
        print("ERROR: %s is not valid JSON: %s" % (PATH, e))
        return 1

    # ---- top level
    for key in ("festival", "days", "categories", "venues", "performers", "programmeItems"):
        if key not in data:
            err("top level: missing key %r" % key)
    if errors:
        return report(data)

    fest, days, cats = data["festival"], data["days"], data["categories"]
    venues, performers, items = data["venues"], data["performers"], data["programmeItems"]

    # ---- minimum counts
    if len(days) != MIN_DAYS:
        err("days: expected exactly %d, found %d" % (MIN_DAYS, len(days)))
    if len(venues) < MIN_VENUES:
        err("venues: expected at least %d, found %d" % (MIN_VENUES, len(venues)))
    if len(performers) < MIN_PERFORMERS:
        err("performers: expected at least %d, found %d" % (MIN_PERFORMERS, len(performers)))
    if len(items) < MIN_ITEMS:
        err("programmeItems: expected at least %d, found %d" % (MIN_ITEMS, len(items)))

    # ---- festival
    need(fest, ["id", "slug", "name", "edition", "editionLabel", "year", "startDate", "endDate", "timezone",
                "city", "country", "countryCode", "tagline", "description", "themes", "genres", "language",
                "currency", "contact", "tickets", "accommodation", "travel", "faq", "codeOfConduct",
                "accessibility", "sustainability", "roots"], "festival")
    if fest.get("startDate") != FEST_START or fest.get("endDate") != FEST_END:
        err("festival: dates must be %s to %s" % (FEST_START, FEST_END))
    if fest.get("timezone") != "Europe/Madrid":
        err("festival: timezone must be Europe/Madrid")
    for coll, req in (("tickets", ["id", "name", "price", "currency", "includes"]),
                      ("accommodation", ["id", "name", "type", "distanceToVenuesKm", "priceFromPerNight"]),
                      ("travel", ["id", "mode", "title", "text"]),
                      ("faq", ["id", "topic", "question", "answer"])):
        seen = set()
        for r in fest.get(coll, []):
            need(r, req, "festival.%s %r" % (coll, r.get("id")))
            if r.get("id") in seen:
                err("festival.%s: duplicate id %r" % (coll, r.get("id")))
            seen.add(r.get("id"))

    # ---- days
    day_ids = set()
    for d in days:
        need(d, ["id", "date", "label", "theme"], "day %r" % d.get("id"))
        day_ids.add(d.get("id"))
        if not (FEST_START <= str(d.get("date")) <= FEST_END):
            err("day %r: date outside festival range" % d.get("id"))
    if len(day_ids) != len(days):
        err("days: duplicate ids")
    day_date = {d["id"]: d["date"] for d in days}

    # ---- categories
    for key in ("types", "levels", "roleFocus", "styles", "performerTypes", "dayParts"):
        if not cats.get(key):
            err("categories.%s missing or empty" % key)
    for lv in cats.get("levels", []):
        if not lv.get("description"):
            err("categories.levels %r: description required (used by the level quiz)" % lv.get("id"))

    # ---- venues
    venue_ids = check_unique(venues, "venue", "ven")
    for v in venues:
        w = "venue %r" % v.get("id")
        need(v, ["name", "kind", "setting", "description", "address", "geo", "capacity", "accessibility",
                 "mapZone"], w)
        if v.get("kind") not in ENUMS["venueKind"]:
            err("%s: invalid kind %r" % (w, v.get("kind")))
        if v.get("setting") not in ENUMS["venueSetting"]:
            err("%s: invalid setting %r" % (w, v.get("setting")))
        for f in ("streetAddress", "postalCode", "addressLocality", "addressRegion", "addressCountry"):
            if not v.get("address", {}).get(f):
                err("%s: address.%s missing" % (w, f))
        for f in ("latitude", "longitude"):
            if not isinstance(v.get("geo", {}).get(f), (int, float)):
                err("%s: geo.%s must be a number" % (w, f))
        for f in ("stepFree", "accessibleToilets", "quietSpace"):
            if not isinstance(v.get("accessibility", {}).get(f), bool):
                err("%s: accessibility.%s must be true or false" % (w, f))
        check_images(v, w)

    # ---- performers
    perf_ids = check_unique(performers, "performer", "perf")
    names = set()
    for p in performers:
        w = "performer %r" % p.get("id")
        need(p, ["name", "type", "country", "styles", "bio"], w)
        if p.get("type") not in ENUMS["performerType"]:
            err("%s: invalid type %r" % (w, p.get("type")))
        for st in p.get("styles", []):
            if st not in ENUMS["style"]:
                err("%s: invalid style %r" % (w, st))
        if not isinstance(p.get("featured"), bool):
            err("%s: featured must be true or false" % w)
        if p.get("type") == "instructor" and len(p.get("members", [])) not in (0, 2):
            err("%s: an instructor has 0 members (solo) or 2 (couple)" % w)
        name_l = str(p.get("name", "")).lower()
        if name_l in names:
            err("performer: duplicate name %r" % p.get("name"))
        names.add(name_l)
        for real in REAL_ARTISTS:
            if real in name_l or any(real in str(m).lower() for m in p.get("members", [])):
                err("%s: name %r matches a well-known real artist (%r)" % (w, p.get("name"), real))
        check_images(p, w)

    # ---- programme items
    item_ids = check_unique(items, "programmeItem", "item")
    # A programme day runs from 06:00 to 06:00, so a 01:30 set belongs to the previous evening.
    start_lo = datetime.fromisoformat(FEST_START + "T06:00:00")
    start_hi = datetime.fromisoformat(FEST_END + "T05:59:59") + timedelta(days=1)
    by_venue, by_perf = {}, {}
    used_perf = set()
    type_counts, level_counts = {}, {}
    for it in items:
        w = "item %r" % it.get("id")
        need(it, ["title", "type", "level", "roleFocus", "style", "dayId", "start", "end", "dayPart", "venueId",
                  "performerIds", "description"], w)
        if "capacity" not in it:
            err("%s: capacity field required (integer or null)" % w)
        for key, enum in (("type", "type"), ("level", "level"), ("roleFocus", "roleFocus"), ("style", "style"),
                          ("dayPart", "dayPart")):
            if it.get(key) not in ENUMS[enum]:
                err("%s: invalid %s %r" % (w, key, it.get(key)))
        type_counts[it.get("type")] = type_counts.get(it.get("type"), 0) + 1
        level_counts[it.get("level")] = level_counts.get(it.get("level"), 0) + 1

        if it.get("venueId") not in venue_ids:
            err("%s: unknown venueId %r" % (w, it.get("venueId")))
        if it.get("dayId") not in day_ids:
            err("%s: unknown dayId %r" % (w, it.get("dayId")))
        if not it.get("performerIds"):
            err("%s: performerIds is empty" % w)
        for pid in it.get("performerIds", []):
            if pid not in perf_ids:
                err("%s: unknown performer id %r" % (w, pid))
            used_perf.add(pid)
        if len(set(it.get("performerIds", []))) != len(it.get("performerIds", [])):
            err("%s: a performer is listed twice" % w)

        a = parse_dt(it.get("start"), w + " start")
        b = parse_dt(it.get("end"), w + " end")
        if a is None or b is None:
            continue
        if b <= a:
            err("%s: end must be after start" % w)
        naive_a, naive_b = a.replace(tzinfo=None), b.replace(tzinfo=None)
        prog_day = (naive_a - timedelta(hours=6)).date()
        if not (start_lo <= naive_a <= start_hi):
            err("%s: start %s is outside the festival range" % (w, it["start"]))
        day_limit = datetime.combine(prog_day, datetime.min.time()) + timedelta(days=1, hours=6)
        if naive_b > day_limit:
            err("%s: end %s is later than 06:00 the morning after its programme day" % (w, it["end"]))
        if it.get("dayId") in day_date and prog_day.strftime("%Y-%m-%d") != day_date[it["dayId"]]:
            err("%s: dayId %s does not match the programme day %s of start %s" % (
                w, it["dayId"], prog_day, it["start"]))
        expect_part = "night" if (a.hour >= 20 or a.hour < 6) else "day"
        if it.get("dayPart") != expect_part:
            err("%s: dayPart is %r but start %s means %r" % (w, it.get("dayPart"), it["start"][11:16], expect_part))

        # sensible times for a bachata event
        if it.get("type") == "workshop":
            if not (9 <= a.hour < 21):
                err("%s: workshop starts at %s, outside 09:00-21:00" % (w, it["start"][11:16]))
            if it.get("level") == "beginner" and not (9 <= a.hour < 19):
                err("%s: beginner workshop at %s should start between 09:00 and 19:00" % (w, it["start"][11:16]))
            if (b - a) > timedelta(minutes=120):
                err("%s: workshop is longer than 2 hours" % w)
        else:
            if it.get("level") != "all-levels":
                err("%s: shows and socials must use level all-levels" % w)

        by_venue.setdefault(it.get("venueId"), []).append((a, b, it.get("id")))
        for pid in it.get("performerIds", []):
            by_perf.setdefault(pid, []).append((a, b, it.get("id")))

    # ---- every performer appears in at least one item
    for pid in sorted(perf_ids - used_perf):
        err("performer %r appears in no programme item" % pid)

    # ---- overlaps
    def overlaps(groups, label):
        for key, rows in groups.items():
            rows.sort()
            for i in range(len(rows) - 1):
                if rows[i + 1][0] < rows[i][1]:
                    err("%s %r: %s (ends %s) overlaps %s (starts %s)" % (
                        label, key, rows[i][2], rows[i][1].strftime("%a %H:%M"),
                        rows[i + 1][2], rows[i + 1][0].strftime("%a %H:%M")))

    overlaps(by_venue, "venue")
    overlaps(by_perf, "performer")

    # ---- soft checks
    for it in items:
        if it.get("type") == "workshop" and it.get("performerIds") and it.get("capacity") is None:
            warn("item %r: workshop without capacity" % it.get("id"))

    return report(data, type_counts, level_counts)


def report(data, type_counts=None, level_counts=None):
    print("Validating %s" % PATH)
    if "performers" in data:
        print("  days=%s venues=%s performers=%s items=%s" % (
            len(data.get("days", [])), len(data.get("venues", [])),
            len(data.get("performers", [])), len(data.get("programmeItems", []))))
    if type_counts:
        print("  item types: %s" % ", ".join("%s=%d" % kv for kv in sorted(type_counts.items(), key=str)))
    if level_counts:
        print("  item levels: %s" % ", ".join("%s=%d" % kv for kv in sorted(level_counts.items(), key=str)))
    for w in warnings:
        print("WARNING: %s" % w)
    if errors:
        print("\n%d error(s):" % len(errors))
        for e in errors:
            print("  - %s" % e)
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: PASS (0 errors, %d warnings)" % len(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
