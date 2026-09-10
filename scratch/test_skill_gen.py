import json, re, os

with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

print(f"Loaded {len(skills)} skills.")

# Load existing G1 translations if any
try:
    from scripts.skills_translations_1 import SKILLS_G1
except Exception as e:
    SKILLS_G1 = {}

print(f"Loaded {len(SKILLS_G1)} manual G1 translations.")
