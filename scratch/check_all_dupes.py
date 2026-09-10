import re
import json

# Let's check sync_heroes.py type0_rows for all heroes
# We can load the scraped heroes or run a quick scan
with open('data/heroes.json', 'r', encoding='utf-8') as f:
    heroes = json.load(f)

print(f"Total heroes: {len(heroes)}")
for h in heroes:
    # check if any other hero has duplicate skills
    names = [s['name'] for s in h['skills']]
    dupes = [x for x in set(names) if names.count(x) > 1]
    if dupes:
        print(f"{h['name']} ({h.get('names', {}).get('ko', '')}): {len(h['skills'])} skills, duplicates: {dupes}")
