# -*- coding: utf-8 -*-
"""
Master compiler to merge all 4 stat value batches into data/translations/stats.json,
generate dynamic numeric pattern templates for patch resilience, and compile production data/translations.json.
"""

import json
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'translations', 'stats.json')

BATCHES = [
    os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_vanguard.json'),
    os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_duelists_a.json'),
    os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_duelists_b.json'),
    os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_strategists.json')
]

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

def merge_and_build():
    with open(STATS_JSON_PATH, 'r', encoding='utf-8') as f:
        stats = json.load(f)

    values = stats.setdefault('values', {})
    patterns = stats.setdefault('patterns', [])

    initial_count = len(values)
    print(f"Initial stat values in stats.json: {initial_count}")

    merged_count = 0
    purity_errors = []

    for b_path in BATCHES:
        with open(b_path, 'r', encoding='utf-8') as f:
            b_data = json.load(f)
        
        for k, tr in b_data.items():
            ko = tr.get('ko', '').strip()
            ja = tr.get('ja', '').strip()

            if not ko or not ja:
                purity_errors.append(f"Empty translation for key '{k}' in {os.path.basename(b_path)}")

            if JAPANESE_REGEX.search(ko):
                purity_errors.append(f"Kana in KO for '{k}': {ko}")
            if KOREAN_REGEX.search(ja):
                purity_errors.append(f"Hangul in JA for '{k}': {ja}")

            values[k] = {
                "ko": ko,
                "ja": ja
            }
            merged_count += 1

    if purity_errors:
        print(f"Found {len(purity_errors)} purity errors:")
        for err in purity_errors[:10]:
            print(f"  {err}")
        raise ValueError("Purity validation failed!")

    print(f"Merged {merged_count} batch items. Total values now: {len(values)}")

    # Add dynamic balance patch resilience patterns:
    # If a value contains numbers and has a recurring formula, create a regex pattern
    # so that future balance patches with updated numbers automatically work!
    existing_regexes = set(p['regex'] for p in patterns)

    new_dynamic_patterns = [
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*per round$",
            "ko": r"발당 $1",
            "ja": r"1発あたり$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*damage per round$",
            "ko": r"발당 $1 데미지",
            "ja": r"1発あたり$1ダメージ"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*damage per hit$",
            "ko": r"타격당 $1 데미지",
            "ja": r"1ヒットあたり$1ダメージ"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*damage per strike$",
            "ko": r"타격당 $1 데미지",
            "ja": r"1撃あたり$1ダメージ"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*damage per shot$",
            "ko": r"발당 $1 데미지",
            "ja": r"1発あたり$1ダメージ"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*damage per cast$",
            "ko": r"시전당 $1 데미지",
            "ja": r"発動ごとに$1ダメージ"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)/s$",
            "ko": r"초당 $1",
            "ja": r"毎秒$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)/sec$",
            "ko": r"초당 $1",
            "ja": r"毎秒$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)/s for (\d+(?:\.\d+)?)s$",
            "ko": r"$2초 동안 초당 $1",
            "ja": r"$2秒間、毎秒$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)/sec for (\d+(?:\.\d+)?)s$",
            "ko": r"$2초 동안 초당 $1",
            "ja": r"$2秒間、毎秒$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)/s for (\d+(?:\.\d+)?)\s*s$",
            "ko": r"$2초 동안 초당 $1",
            "ja": r"$2秒間、毎秒$1"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)s per charge$",
            "ko": r"충전당 $1초",
            "ja": r"チャージごとに$1秒"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)s per shot$",
            "ko": r"발당 $1초",
            "ja": r"発射1回あたり$1秒"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)s per strike$",
            "ko": r"타격당 $1초",
            "ja": r"1撃あたり$1秒"
        },
        {
            "regex": r"^(\d+(?:\.\d+)?)\s*health per round.*$",
            "ko": r"발당 $1 치유",
            "ja": r"1発あたり$1回復"
        },
        {
            "regex": r"^(\d+),\s*up to (\d+)$",
            "ko": r"$1, 최대 $2",
            "ja": r"$1、最大$2"
        },
        {
            "regex": r"^(\d+)% for each stack\.\s*Up to (\d+) stacks\.$",
            "ko": r"스택당 $1%. 최대 $2스택.",
            "ja": r"スタックごとに$1%。最大$2スタック。"
        },
        {
            "regex": r"^(\d+)%\s*Maximum Health$",
            "ko": r"최대 체력의 $1%",
            "ja": r"最大HPの$1%"
        },
        {
            "regex": r"^(\d+)%\s*Health$",
            "ko": r"체력 $1%",
            "ja": r"HP $1%"
        },
        {
            "regex": r"^Reduce movement speed by (\d+)% for (\d+(?:\.\d+)?)s$",
            "ko": r"$2초 동안 이동 속도 $1% 감소",
            "ja": r"$2秒間、移動速度が$1%低下"
        },
        {
            "regex": r"^Increase movement speed by (\d+)% for (\d+(?:\.\d+)?)s$",
            "ko": r"$2초 동안 이동 속도 $1% 증가",
            "ja": r"$2秒間、移動速度が$1%上昇"
        },
        {
            "regex": r"^Falloff begins at (\d+(?:\.\d+)?s) and decreases by (\d+(?:\.\d+)?)/s$",
            "ko": r"$1 후 감쇠 시작, 초당 $2씩 감소",
            "ja": r"$1後に減衰開始、毎秒$2減少"
        }
    ]

    added_patterns = 0
    for np in new_dynamic_patterns:
        if np['regex'] not in existing_regexes:
            patterns.append(np)
            existing_regexes.add(np['regex'])
            added_patterns += 1

    print(f"Added {added_patterns} dynamic balance patch resilience patterns. Total patterns: {len(patterns)}")

    # Write back to data/translations/stats.json
    with open(STATS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved data/translations/stats.json")

    # Compile production data/translations.json
    from build_unified_translations import build_unified
    build_unified()

if __name__ == '__main__':
    merge_and_build()
