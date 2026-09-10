import json

with open('scratch/skills_by_hero.json', 'r', encoding='utf-8') as f:
    h_skills = json.load(f)

heroes_all = list(h_skills.keys())
g1 = heroes_all[:14]
g2 = heroes_all[14:28]
g3 = heroes_all[28:42]
g4 = heroes_all[42:]

def dump(g, fn):
    with open(fn, 'w', encoding='utf-8') as out:
        for h in g:
            out.write(f"\n=== {h} ===\n")
            for sname, desc in h_skills.get(h, []):
                out.write(f"  [{sname}]: {desc}\n")
    print(f"Wrote {fn}")

dump(g1, 'scratch/dump_h1.txt')
dump(g2, 'scratch/dump_h2.txt')
dump(g3, 'scratch/dump_h3.txt')
dump(g4, 'scratch/dump_h4.txt')
