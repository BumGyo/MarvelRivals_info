import json, re

with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

print(f"Total skills: {len(skills)}")

# Let's inspect unique verbs and clauses in descriptions
clauses = set()
for desc, meta in skills:
    parts = re.split(r'[\.\;\n]', desc)
    for p in parts:
        p = p.strip()
        if len(p) > 5:
            clauses.add(p)

print(f"Total distinct clauses: {len(clauses)}")
