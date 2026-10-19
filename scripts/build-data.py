#!/usr/bin/env python3
"""Convert data.json into web/js/data.js (window.FESTIVAL_DATA).

Usage:  python3 scripts/build-data.py
Plain Python 3, standard library only. Run it after every change to data.json,
then run scripts/validate-data.py. Never edit web/js/data.js by hand.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data.json"
DST = ROOT / "web" / "js" / "data.js"

HEADER = """/*
 * GENERATED FILE - DO NOT EDIT BY HAND.
 * Source: data.json (repo root). Build: python3 scripts/build-data.py
 * Loaded with <script src="js/data.js"> so the site works from file:// without fetch().
 */
"""


def main():
    try:
        data = json.loads(SRC.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print("ERROR: cannot read %s: %s" % (SRC, e))
        return 1
    DST.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    # "</" could end an inline script early if the file is ever inlined; keep it safe.
    body = body.replace("</", "<\\/")
    DST.write_text(HEADER + "window.FESTIVAL_DATA = " + body + ";\n", encoding="utf-8")
    print("Wrote %s (%d bytes)" % (DST.relative_to(ROOT), DST.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
