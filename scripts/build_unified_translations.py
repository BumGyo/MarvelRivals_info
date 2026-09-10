# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Master Translations Compiler
Merges:
 - data/translations/skills.json
 - data/translations/teamups.json
 - data/translations/stats.json
into the single production data/translations.json file.
"""

import json
import os

def build_unified():
    with open('data/translations/skills.json', 'r', encoding='utf-8') as f:
        skills = json.load(f)
    with open('data/translations/teamups.json', 'r', encoding='utf-8') as f:
        teamups = json.load(f)
    with open('data/translations/stats.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)

    unified = {
        "skills": skills,
        "teamups": teamups,
        "stat_labels": stats.get("labels", {}),
        "stat_values": stats.get("values", {}),
        "stat_patterns": stats.get("patterns", [])
    }

    with open('data/translations.json', 'w', encoding='utf-8') as f:
        json.dump(unified, f, ensure_ascii=False, indent=2)

    print(f"Generated production data/translations.json:")
    print(f" - Skills: {len(skills)} entries")
    print(f" - Teamups: {len(teamups)} entries")
    print(f" - Stat Labels: {len(unified['stat_labels'])} labels")
    print(f" - Stat Values: {len(unified['stat_values'])} values")
    print(f" - Stat Patterns: {len(unified['stat_patterns'])} dynamic regex patterns")

if __name__ == '__main__':
    build_unified()
