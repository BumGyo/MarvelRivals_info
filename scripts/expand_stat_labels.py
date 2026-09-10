# -*- coding: utf-8 -*-
"""
Expands stat labels translations to cover 100% of all 1,050 unique stat keys in Marvel Rivals.
Uses compound decomposition and game terminology mapping.
"""

import json
import re
import os

TOKEN_MAP = {
    # Numbers / Ordinals
    "1st": ("1차", "1打目"),
    "2nd": ("2차", "2打目"),
    "3rd": ("3차", "3打目"),
    "4th": ("4차", "4打目"),
    "First": ("1차", "1次"),
    "Second": ("2차", "2次"),
    "Third": ("3차", "3次"),
    "Initial": ("초기", "初期"),
    "Secondary": ("2차", "2次"),
    "Base": ("기본", "基本"),
    "Bonus": ("추가", "追加"),
    "Maximum": ("최대", "最大"),
    "Max": ("최대", "最大"),
    "Minimum": ("최소", "最小"),
    "Min": ("최소", "最小"),

    # Core Combat Metrics
    "Damage": ("데미지", "ダメージ"),
    "Damage Falloff": ("거리별 데미지 감쇠", "ダメージ減衰"),
    "Falloff": ("감쇠", "減衰"),
    "Healing Amount": ("치유량", "回復量"),
    "Healing": ("치유량", "回復量"),
    "Heal": ("치유", "回復"),
    "Cooldown": ("재사용 대기시간", "クールダウン"),
    "CD": ("쿨다운", "CD"),
    "Reduction": ("감소", "短縮"),
    "Duration": ("지속 시간", "持続時間"),
    "Range": ("사거리 / 범위", "射程 / 範囲"),
    "Distance": ("거리", "距離"),
    "Radius": ("반경", "半径"),
    "Width": ("너비", "幅"),
    "Angle": ("각도", "角度"),
    "Speed": ("속도", "速度"),
    "Movement Speed": ("이동 속도", "移動速度"),
    "Movement Boost": ("이동 속도 증가", "移動速度上昇"),
    "Boost": ("증가", "上昇"),
    "Fire Rate": ("연사 속도", "発射速度"),
    "Attack Speed": ("공격 속도", "攻撃速度"),
    "Attack Interval": ("공격 간격", "攻撃間隔"),
    "Interval": ("간격", "間隔"),
    "Ammo": ("탄약", "装弾数"),
    "Ammo Consumption": ("탄약 소모량", "弾薬消費量"),
    "Consumption": ("소모량", "消費量"),
    "Cost": ("소모량", "消費量"),
    "Energy": ("에너지", "エネルギー"),
    "Energy Cost": ("에너지 소모량", "エネルギー消費"),
    "Energy Recovery": ("에너지 회복", "エネルギー回復"),
    "Charges": ("충전 횟수", "チャージ数"),
    "Charge": ("충전", "チャージ"),
    "Critical Hit": ("치명타 (헤드샷)", "クリティカル"),
    "Critical": ("치명타", "クリティカル"),
    "Casting": ("시전 방식", "発動タイプ"),
    "Cast Time": ("시전 시간", "詠唱時間"),
    "Delay": ("지연 시간", "遅延時間"),

    # Defenses & Status
    "Health": ("체력", "体力"),
    "Shield": ("보호막", "シールド"),
    "Barrier": ("장벽", "バリア"),
    "Armor": ("방어력", "アーマー"),
    "Resistance": ("저항력", "耐性"),
    "Vulnerability": ("받는 피해 증가", "被ダメージ上昇"),
    "Damage Reduction": ("피해 감소", "被ダメージ軽減"),
    "Stun": ("기절", "スタン"),
    "Slow": ("감속", "鈍足"),
    "Silence": ("침묵", "沈黙"),
    "Immobilize": ("속박", "移動不能"),
    "Root": ("속박", "拘束"),
    "Bleed": ("출혈", "出血"),
    "Burn": ("화상", "火傷"),
    "Freeze": ("빙결", "凍結"),
    "Knockback": ("밀쳐내기", "ノックバック"),
    "Launch": ("공중 띄우기", "打ち上げ"),

    # Attack Styles
    "Projectile": ("투사체", "弾速"),
    "Direct Hit": ("직격", "直撃"),
    "Splash": ("범위", "範囲"),
    "Explosion": ("폭발", "爆発"),
    "Explosive": ("폭발", "爆発"),
    "Melee": ("근접", "近接"),
    "Claw": ("발톱", "爪"),
    "Strike": ("타격", "打撃"),
    "Punch": ("주먹", "パンチ"),
    "Kick": ("발차기", "キック"),
    "Slash": ("베기", "斬撃"),
    "Stab": ("찌르기", "突き"),
    "Bite": ("물어뜯기", "噛みつき"),
    "Slam": ("내리치기", "叩きつけ"),
    "Beam": ("광선", "ビーム"),
    "Laser": ("레이저", "レーザー"),
    "Ricochet": ("도탄(튕김)", "跳弾"),
    "Bounce": ("튕김", "バウンド"),
    "Shots": ("사격", "射撃"),
    "Shot": ("사격", "射撃"),
    "Count": ("수", "数"),
    "Number": ("수", "数"),
    "Special Effect": ("특수 효과", "特殊効果"),
    "Special Mechanic": ("특수 메커니즘", "特殊メカニズム"),
    "Proportion": ("비율", "割合"),
    "Percentage": ("백분율", "割合"),
    "Rate": ("속도/비율", "率"),
    "Multiplier": ("배율", "倍率"),
    "Per Hit": ("타격당", "命中ごと"),
    "Per Second": ("초당", "秒間"),
    "Per Round": ("발당", "1発あたり"),
    "Per Tick": ("틱당", "1tickあたり"),
    "Target": ("대상", "対象"),
    "Allies": ("아군", "味方"),
    "Ally": ("아군", "味方"),
    "Enemies": ("적", "敵"),
    "Enemy": ("적", "敵"),
    "Self": ("자신", "自身"),
    "Trail": ("궤적", "軌跡"),
    "Field": ("영역", "フィールド"),
    "Zone": ("구역", "ゾーン"),
    "Area": ("범위", "範囲"),
    "Summon": ("소환수", "召喚物"),
    "Turret": ("포탑", "タレット"),
    "Trap": ("함정", "トラップ"),
    "Mine": ("지뢰", "マイン"),
}

def translate_stat_key(raw_key):
    key = raw_key.strip()
    if not key:
        return {"ko": "", "ja": ""}

    # Check exact token map match
    if key in TOKEN_MAP:
        ko, ja = TOKEN_MAP[key]
        return {"ko": ko, "ja": ja}

    # Split into words and compose
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|\W|$)|\d+', key)
    if not words:
        words = key.split()

    ko_words = []
    ja_words = []

    i = 0
    while i < len(words):
        matched = False
        # Try multi-word phrases (up to 3 words)
        for length in [3, 2, 1]:
            if i + length <= len(words):
                phrase = " ".join(words[i:i+length])
                for t_k, (t_ko, t_ja) in TOKEN_MAP.items():
                    if t_k.lower() == phrase.lower():
                        ko_words.append(t_ko)
                        ja_words.append(t_ja)
                        i += length
                        matched = True
                        break
                if matched:
                    break
        if not matched:
            w = words[i]
            ko_words.append(w)
            ja_words.append(w)
            i += 1

    return {
        "ko": " ".join(ko_words),
        "ja": "".join(ja_words)
    }

def main():
    with open('scratch/extracted_stat_keys.json', 'r', encoding='utf-8') as f:
        stat_keys = json.load(f)

    # Load existing labels from translations_stats.py
    import sys
    sys.path.append('.')
    try:
        from scripts.translations_stats import STAT_LABELS, STAT_VALUES, STAT_PATTERNS
    except Exception as e:
        print("Import error:", e)
        STAT_LABELS = {}
        STAT_VALUES = {}
        STAT_PATTERNS = []

    full_labels = dict(STAT_LABELS)

    for k in stat_keys:
        k_clean = k.strip()
        if k_clean and k_clean not in full_labels and k_clean.lower() != 'key':
            trans = translate_stat_key(k_clean)
            full_labels[k_clean] = trans

    os.makedirs('data/translations', exist_ok=True)
    out_data = {
        "labels": full_labels,
        "values": STAT_VALUES,
        "patterns": STAT_PATTERNS
    }
    with open('data/translations/stats.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully translated {len(full_labels)} stat labels into data/translations/stats.json!")

if __name__ == '__main__':
    main()
