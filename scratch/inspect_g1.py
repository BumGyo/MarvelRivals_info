import json

with open('scratch/g1_skills.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Items in g1: {len(items)}")
# Let's inspect heroes and sample skills
for it in items[:15]:
    print(f"[{it['hero']}] ({it['key']}) {it['skill']}: {it['desc'][:60]}...")
