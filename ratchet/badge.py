# Copyright 2026 Krishan Subudhi
# SPDX-License-Identifier: Apache-2.0
"""`ratchet badge`: a shields.io endpoint JSON of the current code size."""

from __future__ import annotations

import argparse
import json
import pathlib
import re

from . import config, measure, rules
from .rules import n

OUT = ".ratchet/badge.json"
URL = ("[![code size](https://img.shields.io/endpoint?url=https://raw."
       "githubusercontent.com/%s/main/%s)](https://github.com/krishansubudhi/ratchet)")


def payload(root: str, cfg: dict) -> dict:
    group = "source" if "source" in cfg["groups"] else next(iter(cfg["groups"]))
    lines = rules.totals(measure.measure(root, cfg["groups"]))[group]
    return {"schemaVersion": 1, "label": "code size", "color": "blue",
            "message": "%s lines" % n(lines)}


def cmd_badge(root: str, args: argparse.Namespace) -> int:
    if args.print_markdown:
        origin = measure.git(root, "remote", "get-url", "origin", check=False)
        slug = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?\s*$", origin)
        print(URL % (slug.group(1) if slug else "OWNER/REPO", OUT))
        return 0
    data = payload(root, config.load(root))
    path = pathlib.Path(root, args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")
    print("wrote %s: %s" % (args.out, data["message"]))
    return 0
