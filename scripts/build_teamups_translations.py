# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Team-Up Translations Generator
Generates data/translations/teamups.json for all 112 official hero team-ups
across all 56 heroes, 100% faithful to English source texts.
Combines BATCH_1, BATCH_2, BATCH_3, BATCH_4.
"""

import sys
import os
import json
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from teamup_translations_batch1 import BATCH_1
from teamup_translations_batch2 import BATCH_2
from teamup_translations_batch3 import BATCH_3
from teamup_translations_batch4 import BATCH_4

ALL_BATCHES = {}
ALL_BATCHES.update(BATCH_1)
ALL_BATCHES.update(BATCH_2)
ALL_BATCHES.update(BATCH_3)
ALL_BATCHES.update(BATCH_4)


def build_teamups_json():
    heroes_path = 'data/heroes.json'
    with open(heroes_path, 'r', encoding='utf-8') as f:
        heroes = json.load(f)

    result = {}
    matched_loadouts = 0
    total_loadouts = 0

    for h in heroes:
        hname = h.get('name') or h.get('names', {}).get('en')
        seen_loadouts = []

        for tu in h.get('teamups', []):
            lname = tu.get('loadout_name')
            if lname not in seen_loadouts:
                seen_loadouts.append(lname)

        for idx, lname in enumerate(seen_loadouts, 1):
            total_loadouts += 1
            batch_entry = ALL_BATCHES.get((hname, idx))
            if not batch_entry:
                print(f"Warning: No batch entry for ({hname}, {idx}) '{lname}'")
                continue

            matched_loadouts += 1

            # Update partner_name in heroes.json if needed
            matching_tus = [tu for tu in h.get('teamups', []) if tu.get('loadout_name') == lname]
            for tu in matching_tus:
                if not tu.get('partner_name') or not tu['partner_name'].get('en'):
                    tu['partner_name'] = {
                        'en': batch_entry['partner_en'],
                        'ko': batch_entry['partner_ko'],
                        'ja': batch_entry['partner_ja']
                    }
                else:
                    # ensure ko and ja are filled
                    if not tu['partner_name'].get('ko'):
                        tu['partner_name']['ko'] = batch_entry['partner_ko']
                    if not tu['partner_name'].get('ja'):
                        tu['partner_name']['ja'] = batch_entry['partner_ja']

            entry = {
                "loadout_name": batch_entry["loadout_name"],
                "hero": hname,
                "partner": {
                    "en": batch_entry["partner_en"],
                    "ko": batch_entry["partner_ko"],
                    "ja": batch_entry["partner_ja"]
                },
                "base": {
                    "ko": batch_entry["base_ko"],
                    "ja": batch_entry["base_ja"]
                },
                "enhanced": {
                    "ko": batch_entry["enhanced_ko"],
                    "ja": batch_entry["enhanced_ja"]
                },
                "full": {
                    "ko": f"기본 효과: {batch_entry['base_ko']}\n강화 효과: {batch_entry['enhanced_ko']}",
                    "ja": f"基本効果: {batch_entry['base_ja']}\n強化効果: {batch_entry['enhanced_ja']}"
                }
            }

            # Map for each matching tu
            for tu in matching_tus:
                raw_desc = tu.get('description', '')
                if raw_desc:
                    clean_desc = re.sub(r'\s+', ' ', raw_desc).strip()
                    result[clean_desc] = entry
                    result[raw_desc] = entry

            # Also index by loadout name if not yet indexed
            if batch_entry["loadout_name"] not in result:
                result[batch_entry["loadout_name"]] = entry

    # Save data/heroes.json with updated partner_name metadata
    with open(heroes_path, 'w', encoding='utf-8') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    print(f"Updated partner metadata in {heroes_path}")

    # Save data/translations/teamups.json
    os.makedirs('data/translations', exist_ok=True)
    with open('data/translations/teamups.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Generated data/translations/teamups.json: matched {matched_loadouts}/{total_loadouts} loadouts ({len(result)} keys)")


if __name__ == '__main__':
    build_teamups_json()
