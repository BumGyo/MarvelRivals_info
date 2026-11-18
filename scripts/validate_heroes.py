#!/usr/bin/env python3
"""
Marvel Rivals Hero Schema & Base Stats Validator
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALID_ROLES = {"VANGUARD", "DUELIST", "STRATEGIST"}


def validate():
    heroes_path = ROOT / "data" / "heroes.json"
    with heroes_path.open("r", encoding="utf-8") as f:
        heroes = json.load(f)

    print(f"Total heroes loaded: {len(heroes)}")
    if len(heroes) < 55:
        print(f"❌ Expected at least 55 heroes, found {len(heroes)}")
        sys.exit(1)

    errors = []
    for h in heroes:
        name = h.get("name", "<unknown>")
        role = h.get("role")
        if role not in VALID_ROLES:
            errors.append(f"[{name}] Invalid role: {role}")

        if name == "ADAM WARLOCK" and role != "STRATEGIST":
            errors.append(f"[ADAM WARLOCK] Expected STRATEGIST, got {role}")

        names = h.get("names", {})
        if not (names.get("en") and names.get("ko") and names.get("ja")):
            errors.append(f"[{name}] Missing localized name in names: {names}")

        base_stats = h.get("base_stats", {})
        hp = base_stats.get("Health")
        if not hp or hp == "N/A":
            errors.append(f"[{name}] Missing or invalid Health: {hp}")

        spd = base_stats.get("Movement Speed", "")
        if not spd or not spd.endswith("m/s"):
            errors.append(f"[{name}] Invalid Movement Speed '{spd}' (must end with 'm/s')")

        if not base_stats.get("Movement Mode"):
            errors.append(f"[{name}] Missing Movement Mode")

        has_skills = bool(h.get("skills")) or any(bool(fm.get("skills")) for fm in h.get("forms", []))
        if not has_skills:
            errors.append(f"[{name}] Has no skills in skills or forms!")

        if not h.get("teamups"):
            errors.append(f"[{name}] Has no teamups!")

    if errors:
        print("\n❌ VALIDATION ERRORS FOUND:")
        for err in errors:
            print(" -", err)
        sys.exit(1)

    print(f"\n✅ ALL {len(heroes)} HEROES PASSED SCHEMA VALIDATION WITH 0 ERRORS!")


if __name__ == "__main__":
    validate()
