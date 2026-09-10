# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Stat Labels & Values Translations (KR & JP)
Includes:
 - Exact dictionary for stat labels
 - Rule-based compound label translator
 - Dynamic regex patterns for patch-resilient stat values (preserves numbers across balance updates)
 - Exact dictionary for common stat values
"""

# Static/Common stat keys
STAT_LABELS = {
    "Casting": {"ko": "시전 방식", "ja": "発動タイプ"},
    "Damage": {"ko": "데미지", "ja": "ダメージ"},
    "Damage Falloff": {"ko": "거리별 데미지 감쇠", "ja": "ダメージ減衰"},
    "Fire Rate": {"ko": "연사 속도", "ja": "発射速度"},
    "Ammo": {"ko": "탄약 수", "ja": "装弾数"},
    "Critical Hit": {"ko": "치명타 (헤드샷)", "ja": "クリティカル"},
    "Maximum Projectile Count": {"ko": "최대 투사체 수", "ja": "最大発射弾数"},
    "Projectile Speed": {"ko": "투사체 속도", "ja": "弾速"},
    "Special Effect": {"ko": "특수 효과", "ja": "特殊効果"},
    "Special Effect 1": {"ko": "특수 효과 1", "ja": "特殊効果 1"},
    "Special Effect 2": {"ko": "특수 효과 2", "ja": "特殊効果 2"},
    "Special Effect 3": {"ko": "특수 효과 3", "ja": "特殊効果 3"},
    "Special Mechanic": {"ko": "특수 메커니즘", "ja": "特殊メカニズム"},
    "Health Upon Revival": {"ko": "부활 시 체력", "ja": "蘇生時体力"},
    "Range": {"ko": "사거리 / 범위", "ja": "射程 / 範囲"},
    "Duration": {"ko": "지속 시간", "ja": "持続時間"},
    "Ability Duration": {"ko": "스킬 지속 시간", "ja": "スキル持続時間"},
    "Energy Cost": {"ko": "에너지 소모량", "ja": "エネルギー消費"},
    "ENERGY COST": {"ko": "에너지 소모량", "ja": "エネルギー消費"},
    "Healing Amount": {"ko": "치유량", "ja": "回復量"},
    "Healing": {"ko": "치유량", "ja": "回復量"},
    "Maximum Damage Shared Per Target": {"ko": "대상별 최대 공유 피해", "ja": "対象別最大共有ダメージ"},
    "Cooldown": {"ko": "재사용 대기시간", "ja": "クールダウン"},
    "Healing Amount (Self)": {"ko": "자가 치유량", "ja": "自己回復量"},
    "Number of Bounces": {"ko": "튕김 횟수", "ja": "バウンド回数"},
    "Movement Boost": {"ko": "이동 속도 증가", "ja": "移動速度上昇"},
    "MOVEMENT BOOST": {"ko": "이동 속도 증가", "ja": "移動速度上昇"},
    "Movement Speed": {"ko": "이동 속도", "ja": "移動速度"},
    "Maximum Energy": {"ko": "최대 에너지", "ja": "最大エネルギー"},
    "MAXIMUM ENERGY": {"ko": "최대 에너지", "ja": "最大エネルギー"},
    "Energy Recovery Speed": {"ko": "에너지 회복 속도", "ja": "エネルギー回復速度"},
    "ENERGY RECOVERY SPEED": {"ko": "에너지 회복 속도", "ja": "エネルギー回復速度"},
    "Trail Width": {"ko": "궤적 너비", "ja": "軌跡の幅"},
    "Trail Duration": {"ko": "궤적 지속 시간", "ja": "軌跡持続時間"},
    "Soul Bond Range Increase": {"ko": "영혼 결속 범위 증가", "ja": "ソウルボンド範囲拡大"},
    "Damage per Round": {"ko": "발당 데미지", "ja": "1発あたりのダメージ"},
    "Damage per Tick": {"ko": "틱당 데미지", "ja": "1tickあたりのダメージ"},
    "Bonus Health": {"ko": "추가 체력", "ja": "追加体力"},
    "Bonus Health Duration": {"ko": "추가 체력 지속 시간", "ja": "追加体力持続時間"},
    "Charges": {"ko": "충전 횟수", "ja": "チャージ数"},
    "Charge Time": {"ko": "충전 시간", "ja": "チャージ時間"},
    "Attack Interval": {"ko": "공격 간격", "ja": "攻撃間隔"},
    "Maximum Distance": {"ko": "최대 거리", "ja": "最大射程"},
    "Spell Field Range": {"ko": "영역 반경", "ja": "展開半径"},
    "Spell Field Damage": {"ko": "영역 지속 데미지", "ja": "展開ダメージ"},
    "Spell Field Damage Falloff": {"ko": "영역 데미지 감쇠", "ja": "展開ダメージ減衰"},
    "Spell Field Duration": {"ko": "영역 지속 시간", "ja": "展開持続時間"},
    "Explosion Damage": {"ko": "폭발 데미지", "ja": "爆発ダメージ"},
    "Explosion Radius": {"ko": "폭발 반경", "ja": "爆発半径"},
    "Damage Reduction": {"ko": "피해 감소", "ja": "被ダメージ軽減"},
    "Shield Health": {"ko": "보호막 내구도", "ja": "シールド耐久値"},
    "Maximum Shield Health": {"ko": "최대 보호막 내구도", "ja": "最大シールド耐久値"},
    "Knockback Distance": {"ko": "밀쳐내기 거리", "ja": "ノックバック距離"},
    "Stun Duration": {"ko": "기절 지속 시간", "ja": "スタン持続時間"},
    "Slow Duration": {"ko": "감속 지속 시간", "ja": "鈍足持続時間"},
    "Slow Proportion": {"ko": "감속 비율", "ja": "移動速度低下率"},
    "Vulnerability": {"ko": "받는 피해 증가", "ja": "被ダメージ上昇"},
    "Vulnerability Duration": {"ko": "받는 피해 증가 지속 시간", "ja": "被ダメージ上昇持続時間"},
    "Team-Up Bonus": {"ko": "팀업 보너스", "ja": "チームアップボーナス"},
    "Health": {"ko": "체력", "ja": "体力"},
    "Movement Mode": {"ko": "이동 방식", "ja": "移動モード"},
    "Ammo Consumption": {"ko": "탄약 소모량", "ja": "弾薬消費量"},
    "Maximum Duration": {"ko": "최대 지속 시간", "ja": "最大持続時間"},
    "Speed Boost": {"ko": "이동 속도 증가", "ja": "移動速度上昇"},
    "Base Effect": {"ko": "기본 효과", "ja": "基本効果"},
    "Enhanced Effect": {"ko": "강화 효과", "ja": "強化効果"},
    "Summon Health": {"ko": "소환수 체력", "ja": "召喚物体力"},
    "Healing Reduction Proportion": {"ko": "치유량 감소율", "ja": "回復低下率"},
    "Healing Reduction Duration": {"ko": "치유량 감소 지속 시간", "ja": "回復低下持続時間"},
    "Lifesteal Proportion": {"ko": "생명력 흡수율", "ja": "ライフスティール率"},
    "Healing Per Hit": {"ko": "타격당 치유량", "ja": "命中時回復量"},
    "Damage Boost": {"ko": "공격력 증가", "ja": "与ダメージ上昇"},
    "Initial Projectile Damage": {"ko": "초기 투사체 데미지", "ja": "初期弾ダメージ"},
    "Secondary Damage": {"ko": "2차 데미지", "ja": "2次ダメージ"},
    "Direct Hit Damage": {"ko": "직격 데미지", "ja": "直撃ダメージ"},
    "Splash Damage": {"ko": "범위 데미지", "ja": "範囲ダメージ"},
    "Melee Damage": {"ko": "근접 데미지", "ja": "近接ダメージ"},
    "Shield": {"ko": "보호막", "ja": "シールド"},
    "Barrier Health": {"ko": "장벽 체력", "ja": "バリア耐久値"},
    "Regeneration Rate": {"ko": "재생 속도", "ja": "自動回復速度"},
    "Max Stacks": {"ko": "최대 중첩", "ja": "最大スタック"},
    "Energy Generation": {"ko": "에너지 생성량", "ja": "エネルギー獲得量"},
    "Overheat Rate": {"ko": "과열 속도", "ja": "オーバーヒート速度"},
    "Cooling Rate": {"ko": "냉각 속도", "ja": "冷却速度"},
}

# Static/Common stat text values
STAT_VALUES = {
    "Single-cast direct hit": {"ko": "단일 시전 직격", "ja": "単発直撃"},
    "Single-cast": {"ko": "단일 시전", "ja": "単発発動"},
    "Instant Cast": {"ko": "즉시 시전", "ja": "即時発動"},
    "Targeted": {"ko": "대상 지정", "ja": "ターゲット指定"},
    "Self": {"ko": "자신에게 적용", "ja": "自身対象"},
    "Continuous": {"ko": "지속 시전", "ja": "継続発動"},
    "Passive": {"ko": "패시브", "ja": "パッシブ"},
    "Yes": {"ko": "적용 (헤드샷 가능)", "ja": "適用 (ヘッドショット可能)"},
    "No": {"ko": "미적용", "ja": "適用なし"},
    "Ground": {"ko": "지상", "ja": "地上"},
    "Flight": {"ko": "비행", "ja": "飛行"},
    "Charged release, with multiple delayed projectiles": {"ko": "차징 발사 (복수 시간차 투사체)", "ja": "チャージ発射 (複数時間差弾)"},
    "Persistent spell field that surrounds the caster": {"ko": "시전자를 둘러싸는 지속 장판", "ja": "術者周囲の継続フィールド"},
    "Melee attack": {"ko": "근접 공격", "ja": "近接攻撃"},
    "Rapid Fire": {"ko": "고속 연사", "ja": "高速連射"},
    "Channeling": {"ko": "채널링 집중", "ja": "チャネリング"},
    "Toggle": {"ko": "토글 활성화", "ja": "トグル切替"},
    "Channeled": {"ko": "채널링 (지속 집중)", "ja": "チャネリング"},
    "Lobbed projectile": {"ko": "곡사 투사체", "ja": "曲射弾"},
    "Direct hit": {"ko": "직격", "ja": "直撃"},
    "Area of Effect": {"ko": "범위 효과", "ja": "範囲効果"},
    "Hitscan": {"ko": "히트스캔 (즉발)", "ja": "即着弾 (ヒットスキャン)"},
    "Beam": {"ko": "광선 (빔)", "ja": "ビーム照射"},
}

# Dynamic Patterns for variable numerical stats
# Season balance patches changing numbers will seamlessly retain new values!
STAT_PATTERNS = [
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per round$",
        "ko": "$1 발당 데미지",
        "ja": "$1 発あたりのダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per tick$",
        "ko": "$1 틱당 데미지",
        "ja": "$1 1tickあたりのダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per second$",
        "ko": r"초당 \1 데미지",
        "ja": r"秒間 \1 ダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*rounds per second$",
        "ko": r"초당 \1발",
        "ja": r"秒間 \1発"
    },
    {
        "regex": r"^Falloff begins at (\d+m), decreasing to (\d+%) at (\d+m)$",
        "ko": "$1부터 감쇠 시작, \3에서 \2로 감소",
        "ja": "$1から減衰開始、\3で\2に低下"
    },
    {
        "regex": r"^Falloff begins at (\d+m), decreasing to (\d+) at (\d+m)$",
        "ko": "$1부터 감쇠 시작, \3에서 \2로 감소",
        "ja": "$1から減衰開始、\3で\2に低下"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*spherical radius$",
        "ko": r"반경 \1 구형 범위",
        "ja": r"半径 \1 の球状範囲"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*radius$",
        "ko": r"반경 \1",
        "ja": r"半径 \1"
    },
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s) to recharge$",
        "ko": "$1회 충전 (충전당 \2 소요)",
        "ja": "$1回チャージ (1チャージ \2)"
    },
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s)$",
        "ko": "$1회 충전 (충전당 \2 소요)",
        "ja": "$1回チャージ (1チャージ \2)"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*/\s*s$",
        "ko": r"초당 \1",
        "ja": r"秒間 \1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*s$",
        "ko": "$1초",
        "ja": "$1秒"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*m$",
        "ko": "$1m",
        "ja": "$1m"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*m/s$",
        "ko": "$1 m/s",
        "ja": "$1 m/s"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*%$",
        "ko": "$1%",
        "ja": "$1%"
    }
]
