import json

with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

print(f"Total unique descriptions: {len(skills)}")

# Group by hero
hero_map = {}
for desc, meta in skills:
    h = meta['sampleHero']
    if h not in hero_map:
        hero_map[h] = []
    hero_map[h].append((meta['sampleSkill'], desc))

print(f"Heroes count: {len(hero_map)}")
with open('scratch/skills_by_hero.json', 'w', encoding='utf-8') as f:
    json.dump(hero_map, f, ensure_ascii=False, indent=2)

print("Saved scratch/skills_by_hero.json")
