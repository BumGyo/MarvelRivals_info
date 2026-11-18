#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Runtime Stat Translations Compiler
Compiles data/translations/stats.json into lightweight production data/translations.json
for client-side stat label, stat value, and dynamic regex pattern translation.
(Skill and Team-Up descriptions are pre-embedded into data/heroes.json by post_process.js.)
"""

import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_SRC = os.path.join(ROOT_DIR, "data", "translations", "stats.json")
OUT_PATH = os.path.join(ROOT_DIR, "data", "translations.json")


def build_unified():
    with open(STATS_SRC, "r", encoding="utf-8") as f:
        stats = json.load(f)

    # Filter out any accidental self-echo entries where both ko and ja equal the raw key
    clean_labels = {}
    for k, tr in (stats.get("labels") or {}).items():
        if not tr:
            continue
        ko = tr.get("ko", "").strip()
        ja = tr.get("ja", "").strip()
        if ko == k.strip() and ja == k.strip():
            continue
        clean_labels[k] = {"ko": ko, "ja": ja}

    unified = {
        "stat_labels": clean_labels,
        "stat_values": stats.get("values", {}),
        "stat_patterns": stats.get("patterns", []),
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(unified, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUT_PATH) / 1024.0
    print(f"Generated lightweight production {OUT_PATH} ({size_kb:.1f} KB):")
    print(f" - Stat Labels: {len(unified['stat_labels'])} labels")
    print(f" - Stat Values: {len(unified['stat_values'])} values")
    print(f" - Stat Patterns: {len(unified['stat_patterns'])} dynamic regex patterns")


if __name__ == "__main__":
    build_unified()
