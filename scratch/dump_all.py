import json, re

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

with open('scratch/skills_duelist.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
with open('scratch/skills_strategist.json', 'r', encoding='utf-8') as f:
    s = json.load(f)
with open('scratch/teamups_all.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

with open('scratch/duelist_dump.txt', 'w', encoding='utf-8') as out:
    for hero, sks in d.items():
        out.write(f"\n=== {hero} ({len(sks)}) ===\n")
        for sk in sks:
            out.write(f"  [{sk['key']}] {sk['name']}: {norm(sk['desc'])}\n")
            if sk.get('upgrade'):
                out.write(f"    (UPGRADE) {sk['upgrade']['name']}: {norm(sk['upgrade']['desc'])}\n")

with open('scratch/strategist_dump.txt', 'w', encoding='utf-8') as out:
    for hero, sks in s.items():
        out.write(f"\n=== {hero} ({len(sks)}) ===\n")
        for sk in sks:
            out.write(f"  [{sk['key']}] {sk['name']}: {norm(sk['desc'])}\n")
            if sk.get('upgrade'):
                out.write(f"    (UPGRADE) {sk['upgrade']['name']}: {norm(sk['upgrade']['desc'])}\n")

with open('scratch/teamup_dump.txt', 'w', encoding='utf-8') as out:
    for hero, tus in t.items():
        out.write(f"\n=== {hero} ({len(tus)}) ===\n")
        for tu in tus:
            out.write(f"  Loadout {tu['loadout']} [{tu['tier']}] {tu['name']} (Partner: {tu['partner']}):\n    {norm(tu['desc'])}\n")

print("Dumps created.")
