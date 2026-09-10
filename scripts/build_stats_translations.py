# -*- coding: utf-8 -*-
"""
Builds data/translations/stats.json from translations_stats.py
"""

import json
import os
import sys

sys.path.append('.')
from scripts.translations_stats import STAT_LABELS, STAT_VALUES, STAT_PATTERNS

def build_stats():
    os.makedirs('data/translations', exist_ok=True)
    out = {
        "labels": STAT_LABELS,
        "values": STAT_VALUES,
        "patterns": STAT_PATTERNS
    }
    with open('data/translations/stats.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Generated data/translations/stats.json ({len(STAT_LABELS)} labels, {len(STAT_VALUES)} values, {len(STAT_PATTERNS)} patterns)")

if __name__ == '__main__':
    build_stats()
