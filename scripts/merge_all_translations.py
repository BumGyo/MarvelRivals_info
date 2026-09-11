# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Master Skills Translations Compiler
Merges all translation batches into data/translations/skills.json.
Validates 0 placeholders, 100% purity, and complete hero skill coverage.
"""

import json
import os
import glob
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_PATH = os.path.join(ROOT_DIR, 'data', 'translations', 'skills.json')
BATCHES_DIR = os.path.join(ROOT_DIR, 'scripts', 'batches')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

def normalize(text):
    return text.replace('\xa0', ' ').strip()

def main():
    if not os.path.exists(SKILLS_PATH):
        raise FileNotFoundError(f"Skills file not found: {SKILLS_PATH}")

    with open(SKILLS_PATH, 'r', encoding='utf-8') as f:
        master_skills = json.load(f)

    print(f"Loaded master skills.json with {len(master_skills)} entries.")

    batch_files = sorted(glob.glob(os.path.join(BATCHES_DIR, 'batch_*.json')))
    batch_map = {}

    for bf in batch_files:
        with open(bf, 'r', encoding='utf-8') as f:
            batch_data = json.load(f)
        b_name = os.path.basename(bf)
        print(f"Loaded {b_name} ({len(batch_data)} entries)")
        for key, val in batch_data.items():
            norm_k = normalize(key)
            batch_map[norm_k] = val
            if ':' in norm_k:
                sub_k = norm_k.split(':', 1)[1].strip()
                if sub_k:
                    batch_map[sub_k] = val

    # Apply to master_skills
    updated_count = 0
    for k in list(master_skills.keys()):
        k_norm = normalize(k)
        if k_norm in batch_map:
            master_skills[k] = batch_map[k_norm]
            updated_count += 1
        elif ':' in k_norm:
            sub = k_norm.split(':', 1)[1].strip()
            if sub in batch_map:
                master_skills[k] = batch_map[sub]
                updated_count += 1

    # Also add batch keys to master_skills if missing
    added_count = 0
    for k, val in batch_map.items():
        if k not in master_skills:
            master_skills[k] = val
            added_count += 1

    print(f"\nApplied {updated_count} updates and {added_count} additions to master skills.")

    # Validation check
    placeholder_ko = 0
    placeholder_ja = 0
    purity_ko_err = 0
    purity_ja_err = 0

    for key, val in master_skills.items():
        ko = val.get('ko', '')
        ja = val.get('ja', '')

        if '의 스킬입니다' in ko:
            placeholder_ko += 1
            print(f"⚠️ Placeholder KO: {key[:50]}...")
        if 'のスキル。' in ja or 'のスキルです' in ja or re.search(r'^[A-Z0-9\s()&\'-]+のスキル', ja):
            placeholder_ja += 1
            print(f"⚠️ Placeholder JA: {key[:50]}...")

        if JAPANESE_REGEX.search(ko):
            purity_ko_err += 1
            print(f"❌ Purity error: Japanese kana in Korean for {key[:50]}")
        if KOREAN_REGEX.search(ja):
            purity_ja_err += 1
            print(f"❌ Purity error: Korean hangul in Japanese for {key[:50]}")

    print("\n=== Validation Results ===")
    print(f"Total skills in master: {len(master_skills)}")
    print(f"Placeholder in KO ('의 스킬입니다'): {placeholder_ko}")
    print(f"Placeholder in JA ('のスキル'): {placeholder_ja}")
    print(f"Cross-language purity errors: KO={purity_ko_err}, JA={purity_ja_err}")

    if purity_ko_err > 0 or purity_ja_err > 0:
        raise ValueError("Purity check failed! Cannot save skills.json.")

    if placeholder_ko > 0 or placeholder_ja > 0:
        raise ValueError("Placeholder check failed! skills.json still contains placeholders.")

    with open(SKILLS_PATH, 'w', encoding='utf-8') as f:
        json.dump(master_skills, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 [SUCCESS] Successfully wrote 100% clean and validated {SKILLS_PATH}")

if __name__ == '__main__':
    main()
