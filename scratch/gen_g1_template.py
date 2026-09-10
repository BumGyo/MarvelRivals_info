import json, re

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

with open('scratch/g1_skills.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Loaded {len(items)} skills for G1")
with open('scratch/g1_items.py', 'w', encoding='utf-8') as f:
    f.write("# -*- coding: utf-8 -*-\nG1_ITEMS = [\n")
    for it in items:
        f.write(f"    {{\n        'hero': {repr(it['hero'])},\n        'skill': {repr(it['skill'])},\n        'desc': {repr(norm(it['desc']))}\n    }},\n")
    f.write("]\n")

print("Generated scratch/g1_items.py")
