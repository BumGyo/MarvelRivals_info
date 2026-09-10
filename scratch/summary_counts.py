import json

with open('data/heroes.json', 'r', encoding='utf-8') as f:
    heroes = json.load(f)

print(f"Total heroes: {len(heroes)}")
all_skills = []
all_teamups = []

for h in heroes:
    for s in h.get('skills', []):
        all_skills.append({
            'hero': h['names']['en'],
            'key': s.get('key'),
            'name': s.get('name'),
            'desc': (s.get('description') or '').strip(),
            'upgrade': s.get('upgrade')
        })
    for t in h.get('teamups', []):
        all_teamups.append({
            'hero': h['names']['en'],
            'loadout': t.get('loadout_name'),
            'loadout_num': t.get('loadout_number'),
            'tier': t.get('tier'),
            'partner': t.get('partner_name', {}).get('en', ''),
            'desc': (t.get('description') or '').strip()
        })

print(f"Total skills: {len(all_skills)}")
print(f"Total teamups: {len(all_teamups)}")
