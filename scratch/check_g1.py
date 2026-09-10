import json

with open('scratch/skills_by_hero.json', 'r', encoding='utf-8') as f:
    hero_skills = json.load(f)

heroes_g1 = [
  'ADAM WARLOCK', 'ANGELA', 'BLACK CAT', 'BLACK PANTHER', 'BLADE',
  'Black Widow', 'CAPTAIN AMERICA', 'Cloak & Dagger', 'Cyclops',
  'DEADPOOL (VANGUARD)', 'DEADPOOL (DUELIST)', 'DEADPOOL (STRATEGIST)',
  'DEVIL DINOSAUR', 'DOCTOR STRANGE'
]

total = 0
for h in heroes_g1:
    sks = hero_skills.get(h, [])
    total += len(sks)
    print(f"{h}: {len(sks)} skills")
print(f"Total skills in Group 1: {total}")
