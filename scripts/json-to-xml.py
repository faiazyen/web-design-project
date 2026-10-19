#!/usr/bin/env python3
"""Convert data.json into data.xml and check that both files say the same thing.

Usage:  python3 scripts/json-to-xml.py
data.json is the single source of truth. data.xml is generated for the Seminar 2
submission (the assignment accepts XML or JSON). Never edit data.xml by hand.
Plain Python 3, standard library only.

Mapping: object keys become element names; arrays become repeated child elements
named in the SINGULAR map below; true/false are written as text; null is written
as an empty element with nil="true".
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, DST = ROOT / "data.json", ROOT / "data.xml"

SINGULAR = {
    "days": "day", "venues": "venue", "performers": "performer", "programmeItems": "programmeItem",
    "performerIds": "performerId", "tags": "tag", "themes": "theme", "genres": "genre",
    "tickets": "ticket", "includes": "include", "accommodation": "place", "travel": "option",
    "faq": "entry", "principles": "principle", "features": "feature", "commitments": "commitment",
    "timeline": "event", "instruments": "instrument", "members": "member", "styles": "style",
    "types": "type", "levels": "level", "roleFocus": "role", "performerTypes": "performerType",
    "dayParts": "dayPart",
}


def build(parent, key, value):
    if isinstance(value, dict):
        el = ET.SubElement(parent, key)
        for k, v in value.items():
            build(el, k, v)
    elif isinstance(value, list):
        el = ET.SubElement(parent, key)
        child = SINGULAR.get(key, "item")
        for v in value:
            build(el, child, v)
    else:
        el = ET.SubElement(parent, key)
        if value is None:
            el.set("nil", "true")
        elif isinstance(value, bool):
            el.text = "true" if value else "false"
        else:
            el.text = str(value)
    return el


def indent(el, level=0):
    pad = "\n" + "  " * level
    if len(el):
        if not (el.text or "").strip():
            el.text = pad + "  "
        for child in el:
            indent(child, level + 1)
            if not (child.tail or "").strip():
                child.tail = pad + "  "
        child.tail = pad
    if level and not (el.tail or "").strip():
        el.tail = pad


def check(data):
    """Re-read data.xml and compare ids, counts and relations with data.json."""
    tree = ET.parse(DST).getroot()
    problems = []
    for coll, tag in (("venues", "venue"), ("performers", "performer"), ("programmeItems", "programmeItem"),
                      ("days", "day")):
        j_ids = [r["id"] for r in data[coll]]
        x_ids = [e.findtext("id") for e in tree.find(coll).findall(tag)]
        if j_ids != x_ids:
            problems.append("%s: ids differ between JSON and XML" % coll)
    j_items = {i["id"]: i for i in data["programmeItems"]}
    for e in tree.find("programmeItems").findall("programmeItem"):
        j = j_items[e.findtext("id")]
        if e.findtext("venueId") != j["venueId"]:
            problems.append("%s: venueId differs" % j["id"])
        if [p.text for p in e.find("performerIds").findall("performerId")] != j["performerIds"]:
            problems.append("%s: performerIds differ" % j["id"])
        for f in ("title", "type", "level", "roleFocus", "style", "dayId", "start", "end", "dayPart"):
            if e.findtext(f) != str(j[f]):
                problems.append("%s: %s differs" % (j["id"], f))
    # every reference in the XML resolves
    perf = {e.findtext("id") for e in tree.find("performers").findall("performer")}
    ven = {e.findtext("id") for e in tree.find("venues").findall("venue")}
    for e in tree.find("programmeItems").findall("programmeItem"):
        if e.findtext("venueId") not in ven:
            problems.append("XML %s: unknown venue" % e.findtext("id"))
        for p in e.find("performerIds").findall("performerId"):
            if p.text not in perf:
                problems.append("XML %s: unknown performer %s" % (e.findtext("id"), p.text))
    return problems, (len(ven), len(perf), len(tree.find("programmeItems")))


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    root = ET.Element("festivalData")
    for k, v in data.items():
        build(root, k, v)
    indent(root)
    ET.ElementTree(root).write(DST, encoding="utf-8", xml_declaration=True)
    problems, (nv, np_, ni) = check(data)
    print("Wrote %s (%d bytes): %d venues, %d performers, %d programme items" % (
        DST.name, DST.stat().st_size, nv, np_, ni))
    if problems:
        print("MISMATCH between data.json and data.xml:")
        for p in problems:
            print("  - " + p)
        return 1
    print("OK: data.xml matches data.json (ids, counts, venue and performer references, item fields)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
