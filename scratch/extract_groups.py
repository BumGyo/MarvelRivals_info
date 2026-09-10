import json

with open('data/heroes.json', 'r', encoding='utf-8') as f:
    heroes = json.load(f)

g1_names = set([
  'ADAM WARLOCK', 'ANGELA', 'BLACK CAT', 'BLACK PANTHER', 'BLADE',
  'Black Widow', 'CAPTAIN AMERICA', 'Cloak & Dagger', 'Cyclops',
  'DEADPOOL (VANGUARD)', 'DEADPOOL (DUELIST)', 'DEADPOOL (STRATEGIST)',
  'DEVIL DINOSAUR', 'DOCTOR STRANGE'
])
g2_names = set([
  'Daredevil', 'Elsa Bloodstone', 'Emma Frost', 'GROOT', 'Gambit',
  'HAWKEYE', 'HELA', 'HULK', 'HUMAN TORCH', 'IRON FIST',
  'IRON MAN', 'Invisible Woman', 'JEFF THE LAND SHARK', 'Jubilation Lee'
])
g3_names = set([
  'LOKI', 'LUNA SNOW', 'MAGIK', 'MAGNETO', 'MANTIS',
  'MOON KNIGHT', 'Mister Fantastic', 'NAMOR', 'PENI PARKER',
  'PHOENIX', 'PSYLOCKE', 'ROCKET RACCOON', 'Rogue', 'SCARLET WITCH'
])

def extract_for_group(group_names, filename):
    out = []
    seen = set()
    for h in heroes:
        if h['names']['en'] in group_names:
            for s in h.get('skills', []):
                d = (s.get('description') or '').strip()
                if d and d not in seen:
                    seen.add(d)
                    out.append({
                        'hero': h['names']['en'],
                        'skill': s.get('name'),
                        'key': s.get('key'),
                        'desc': d
                    })
                if s.get('upgrade'):
                    ud = (s['upgrade'].get('description') or '').strip()
                    if ud and ud not in seen:
                        seen.add(ud)
                        out.append({
                            'hero': h['names']['en'],
                            'skill': s['upgrade'].get('name', s.get('name')),
                            'key': s.get('key'),
                            'desc': ud
                        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} unique skills to {filename}")

extract_for_group(g1_names, 'scratch/g1_skills.json')
extract_for_group(g2_names, 'scratch/g2_skills.json')
extract_for_group(g3_names, 'scratch/g3_skills.json')

# Group 4 is all remaining
all_known = g1_names | g2_names | g3_names
g4_names = set(h['names']['en'] for h in heroes if h['names']['en'] not in all_known)
extract_for_group(g4_names, 'scratch/g4_skills.json')
