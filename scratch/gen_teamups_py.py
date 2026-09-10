import json

with open('scratch/extracted_teamups.json', 'r', encoding='utf-8') as f:
    tus = json.load(f)

print(f"Loaded {len(tus)} unique teamups.")
with open('scratch/teamups_to_translate.py', 'w', encoding='utf-8') as f:
    f.write("# -*- coding: utf-8 -*-\nTEAMUP_DATA = [\n")
    for desc, meta in tus:
        f.write(f"    {{\n        'hero': {repr(meta['sampleHero'])},\n        'loadout': {repr(meta['sampleLoadout'])},\n        'desc': {repr(desc)}\n    }},\n")
    f.write("]\n")

print("Generated scratch/teamups_to_translate.py")
