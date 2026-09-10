import json

with open('scratch/skills_by_hero.json', 'r', encoding='utf-8') as f:
    h_skills = json.load(f)

heroes = [
  'ADAM WARLOCK', 'ANGELA', 'BLACK CAT', 'BLACK PANTHER', 'BLADE',
  'Black Widow', 'CAPTAIN AMERICA', 'Cloak & Dagger', 'Cyclops',
  'DEADPOOL (VANGUARD)', 'DEADPOOL (DUELIST)', 'DEADPOOL (STRATEGIST)',
  'DEVIL DINOSAUR', 'DOCTOR STRANGE'
]

with open('scratch/dump_h1.txt', 'w', encoding='utf-8') as out:
    for h in heroes:
        out.write(f"\n=== {h} ===\n")
        for sname, desc in h_skills.get(h, []):
            out.write(f"  [{sname}]: {desc}\n")

print("Wrote scratch/dump_h1.txt")
