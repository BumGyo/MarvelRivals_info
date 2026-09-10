import json

with open('scratch/all_heroes_forms_scan.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

multi_form_heroes = []
single_form_heroes = []

for h in data:
    if h.get("error"):
        print(f"Error in {h.get('title')}: {h.get('error')}")
        continue
    t0_count = h.get("type0_count", 0)
    skill_forms = h.get("skill_form_indices", [])
    
    if t0_count > 1 or len(skill_forms) > 1:
        multi_form_heroes.append(h)
    else:
        single_form_heroes.append(h)

print(f"\n=======================================================")
print(f"  FOUND {len(multi_form_heroes)} MULTI-FORM HEROES ON OFFICIAL SITE")
print(f"=======================================================")

for mh in sorted(multi_form_heroes, key=lambda x: x["title"]):
    print(f"\n★ Hero: {mh['title']}")
    print(f"   - Type 0 Forms Count: {mh['type0_count']}")
    print(f"   - Form Names / Avatars in Type 0:")
    for f in mh["type0_forms"]:
        print(f"       [{f['index']}] Name='{f['name']}', Avatar='{f['avatar']}'")
    print(f"   - Skill Form Indices (td_last): {mh['skill_form_indices']}")
    print(f"   - Total Normal Skills: {mh['skills_count']}")

print(f"\nSingle Form Heroes Count: {len(single_form_heroes)}")
