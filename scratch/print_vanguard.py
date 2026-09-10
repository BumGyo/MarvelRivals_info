import json, re

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

with open('scratch/skills_vanguard.json', 'r', encoding='utf-8') as f:
    v = json.load(f)

with open('scratch/vanguard_dump.txt', 'w', encoding='utf-8') as out:
    for hero, sks in v.items():
        out.write(f"\n=== {hero} ({len(sks)}) ===\n")
        for s in sks:
            out.write(f"  [{s['key']}] {s['name']}: {norm(s['desc'])}\n")
            if s.get('upgrade'):
                out.write(f"    (UPGRADE) {s['upgrade']['name']}: {norm(s['upgrade']['desc'])}\n")

print("Wrote scratch/vanguard_dump.txt")
