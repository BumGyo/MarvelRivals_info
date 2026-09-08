#!/usr/bin/env python3
import json
import sys

def validate():
    with open('data/heroes.json', 'r', encoding='utf-8') as f:
        heroes = json.load(f)

    print(f"Total heroes loaded: {len(heroes)}")
    assert len(heroes) >= 50, f"Expected at least 50 heroes, found {len(heroes)}"

    errors = []
    for h in heroes:
        name = h.get('name')
        base_stats = h.get('base_stats', {})
        
        # Check Health
        hp = base_stats.get('Health')
        if not hp:
            errors.append(f"[{name}] Missing Health in base_stats: {base_stats}")
        elif hp == 'N/A':
            errors.append(f"[{name}] Health is N/A")
            
        # Check Movement Speed
        spd = base_stats.get('Movement Speed')
        if not spd:
            errors.append(f"[{name}] Missing Movement Speed in base_stats: {base_stats}")
        elif spd == 'N/A':
            errors.append(f"[{name}] Movement Speed is N/A")
        elif not spd.endswith('m/s'):
            errors.append(f"[{name}] Movement Speed '{spd}' does not end with 'm/s'")

        # Check Movement Mode
        mode = base_stats.get('Movement Mode')
        if not mode:
            errors.append(f"[{name}] Missing Movement Mode in base_stats")

        # Check Skills
        skills = h.get('skills', [])
        if not skills:
            errors.append(f"[{name}] Has no skills!")

        # Check Team-ups
        teamups = h.get('teamups', [])
        if not teamups:
            errors.append(f"[{name}] Has no teamups!")

    if errors:
        print("\n❌ VALIDATION ERRORS FOUND:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    else:
        print("\n✅ ALL 53 HEROES PASSED VALIDATION WITH 0 ERRORS!")
        print(f"Sample heroes base_stats:")
        for sample in [heroes[0], heroes[15], heroes[30], heroes[52]]:
            print(f" - {sample['name']:15} | HP: {sample['base_stats']['Health']:30} | SPD: {sample['base_stats']['Movement Speed']:10} | Mode: {sample['base_stats']['Movement Mode']}")

if __name__ == '__main__':
    validate()
