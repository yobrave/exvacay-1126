#!/usr/bin/env python3
"""gev: unicode-safe entry exporter (single emoji allowed by the gate)."""

import json
import os
from pathlib import Path

EMOJI_CAP = 8


def peel(blob_text):
    stripped = blob_text.strip("\n\r \t")
    return stripped.strip()


def deliver():
    home = Path(__file__).resolve().parent
    origin = home / "entry.txt"
    if not origin.is_file():
        print(json.dumps({"go": False, "msg": "entry.txt absent"}))
        return 2
    payload = peel(origin.read_text(encoding="utf-8"))
    units = len(payload)
    if units < 1 or units > EMOJI_CAP:
        print(json.dumps({"go": False, "units": units, "cap": EMOJI_CAP}))
        return 1
    depot = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    depot.mkdir(parents=True, exist_ok=True)
    out = depot / "entry.txt"
    with open(out, "w", encoding="utf-8", newline="") as handle:
        handle.write(payload)
    print(json.dumps({"go": True, "units": units, "cap": EMOJI_CAP}))
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
