import json, re

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

for g in [2, 3, 4]:
    with open(f'scratch/g{g}_skills.json', 'r', encoding='utf-8') as f:
        items = json.load(f)
    with open(f'scratch/g{g}_items.py', 'w', encoding='utf-8') as f:
        f.write(f"# -*- coding: utf-8 -*-\nG{g}_ITEMS = [\n")
        for it in items:
            f.write(f"    {{\n        'hero': {repr(it['hero'])},\n        'skill': {repr(it['skill'])},\n        'desc': {repr(norm(it['desc']))}\n    }},\n")
        f.write("]\n")
    print(f"Generated scratch/g{g}_items.py ({len(items)} items)")
