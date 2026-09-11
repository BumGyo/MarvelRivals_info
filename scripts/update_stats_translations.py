# -*- coding: utf-8 -*-
"""
Update data/translations/stats.json with:
1. Missing stat labels (titles), specifically for Gorr and newly added mechanics
2. Comprehensive dynamic regex patterns for numbers, areas, ranges, charges, and buffs
3. High-quality natural translations for casting mechanisms and hero-specific stat descriptions
4. Strict cross-language purity validation (0 Kana in KO, 0 Hangul in JA)
"""

import json
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_PATH = os.path.join(ROOT_DIR, 'data', 'translations', 'stats.json')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

# 1. Missing Stat Labels (Titles)
NEW_LABELS = {
    "Type": {
        "ko": "공격 유형",
        "ja": "攻撃タイプ"
    },
    "Berserker Summon Range": {
        "ko": "버서커 소환 사거리",
        "ja": "バーサーカー召喚射程"
    },
    "Black Berserker Melee Damage": {
        "ko": "블랙 버서커 근접 데미지",
        "ja": "ブラック・バーサーカー近接ダメージ"
    },
    "Berserker Spawn Range": {
        "ko": "버서커 생성 범위",
        "ja": "バーサーカー生成範囲"
    },
    "Necroverse Range": {
        "ko": "네크로버스 범위",
        "ja": "ネクロバース範囲"
    },
    "Annihilablade Damage": {
        "ko": "아나이얼라블레이드 데미지",
        "ja": "アナイアブレードダメージ"
    },
    "Annihilablade Attack Interval": {
        "ko": "아나이얼라블레이드 공격 주기",
        "ja": "アナイアブレード攻撃間隔"
    },
    "Annihilablade Maximum Distance": {
        "ko": "아나이얼라블레이드 최대 사거리",
        "ja": "アナイアブレード最大射程"
    },
    "Attack Speed Boost to Frenzied Berserkers": {
        "ko": "광란 버서커 공격 속도 증가",
        "ja": "狂乱バーサーカー攻撃速度増加"
    },
    "Necroverse Damage": {
        "ko": "네크로버스 데미지",
        "ja": "ネクロバースダメージ"
    },
    "Summon Maximum Health": {
        "ko": "소환물 최대 체력",
        "ja": "召喚物最大体力"
    },
    "Summon Damage": {
        "ko": "소환물 데미지",
        "ja": "召喚物ダメージ"
    },
    "Summon Attack Interval": {
        "ko": "소환물 공격 주기",
        "ja": "召喚物攻撃間隔"
    },
    "Summon Attack Range": {
        "ko": "소환물 공격 사거리",
        "ja": "召喚物攻撃射程"
    },
    "Shadow Scythe Damage": {
        "ko": "섀도우 사이드 데미지",
        "ja": "シャドウサイスダメージ"
    },
    "Shadow Scythe Attack Interval": {
        "ko": "섀도우 사이드 공격 주기",
        "ja": "シャドウサイス攻撃間隔"
    },
    "Shadow Scythe Maximum Distance": {
        "ko": "섀도우 사이드 최대 사거리",
        "ja": "シャドウサイス最大射程"
    },
    "Summon Damage/Health Conversion": {
        "ko": "소환물 피해 체력 전환율",
        "ja": "召喚物ダメージHP変換率"
    }
}

# 2. Dynamic Regex Patterns (Preserves patch numbers!)
NEW_PATTERNS = [
    # Spell Field & Dimensions
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*(?:radius\s+)?spherical\s*(?:radius\s+)?(?:spell\s+field)?\.?$",
        "ko": "반경 $1 구형 범위",
        "ja": "半径 $1 球状範囲"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*radius\s+spherical\s+spell\s+field\.?$",
        "ko": "반경 $1 구형 장판",
        "ja": "半径 $1 球状フィールド"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*spherical\s*radius\s*spell\s*field\.?$",
        "ko": "반경 $1 구형 장판",
        "ja": "半径 $1 球状フィールド"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*radius\s+cylindrical\s+spell\s+field\.?$",
        "ko": "반경 $1 원기둥형 장판",
        "ja": "半径 $1 円柱状フィールド"
    },
    {
        "regex": r"^A cylindrical spell field with a (\d+(?:\.\d+)?m) radius and a height of (\d+(?:\.\d+)?m)\.?$",
        "ko": "반경 $1, 높이 $2 원기둥형 장판",
        "ja": "半径 $1・高さ $2 の円柱状フィールド"
    },
    {
        "regex": r"^A cylindrical spell field with a (\d+(?:\.\d+)?m) radius and (\d+(?:\.\d+)?m) in length\.?$",
        "ko": "반경 $1, 길이 $2 원기둥형 장판",
        "ja": "半径 $1・長さ $2 の円柱状フィールド"
    },
    {
        "regex": r"^Width:\s*(\d+(?:\.\d+)?m),\s*Height:\s*(\d+(?:\.\d+)?m)$",
        "ko": "너비: $1, 높이: $2",
        "ja": "幅: $1、高さ: $2"
    },
    {
        "regex": r"^Up to (\d+(?:\.\d+)?m)$",
        "ko": "최대 $1",
        "ja": "最大 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*radius\.?$",
        "ko": "반경 $1",
        "ja": "半径 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*spherical\s*radius\.?$",
        "ko": "구형 반경 $1",
        "ja": "球状半径 $1"
    },

    # Charges & Durations
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s) to recharge\.?$",
        "ko": "$1회 충전 (충전당 $2)",
        "ja": "$1回チャージ (1回あたり$2)"
    },
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s)\.?$",
        "ko": "$1회 충전 (충전당 $2)",
        "ja": "$1回チャージ (1回あたり$2)"
    },
    {
        "regex": r"^(\d+s)\s*when not thrown,\s*(\d+s)\s*when thrown$",
        "ko": "미투척 시 $1, 투척 시 $2",
        "ja": "未投擲時 $1、投擲時 $2"
    },
    {
        "regex": r"^The challenge lasts (\d+s)\. The buff lasts (\d+s) after you complete it\.$",
        "ko": "챌린지 지속 시간 $1, 완료 시 버프 $2 지속",
        "ja": "チャレンジ時間 $1、完了後バフ $2 持続"
    },

    # Multipliers & Intervals
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*per hit$",
        "ko": "타격당 $1",
        "ja": "1ヒットあたり$1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*per hit,\s*(\d+)\s*hits?$",
        "ko": "타격당 $1 (총 $2타)",
        "ja": "1ヒットあたり$1（計$2回）"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?s)\s*per hit\.?$",
        "ko": "타격 간격 $1",
        "ja": "ヒット間隔 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?s)\s*per round\.?$",
        "ko": "발당 $1",
        "ja": "1発あたり$1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?s)\s*per use\.?$",
        "ko": "시전당 $1",
        "ja": "1使用あたり$1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*per projectile$",
        "ko": "투사체당 $1",
        "ja": "弾あたり$1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*per second$",
        "ko": "초당 $1",
        "ja": "毎秒 $1"
    },

    # Boosts & Percentages
    {
        "regex": r"^(\d+(?:\.\d+)?%)\s*Damage Boost$",
        "ko": "피해량 $1 증가",
        "ja": "与ダメージ $1 増加"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?%)\s*Healing Boost$",
        "ko": "치유량 $1 증가",
        "ja": "回復量 $1 増加"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?%)\s*Movement Boost$",
        "ko": "이동 속도 $1 증가",
        "ja": "移動速度 $1 増加"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?%)\s*Slow$",
        "ko": "감속 $1",
        "ja": "鈍足 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?%?)\s*for\s*(\d+(?:\.\d+)?s)$",
        "ko": "$2 동안 $1",
        "ja": "$2間 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)%)\s*Max Health$",
        "ko": "$1 + 최대 체력의 $2",
        "ja": "$1 + 最大体力の $2"
    },
    {
        "regex": r"^Hero Hulk and Monster Hulk gain (\d+) Max Health$",
        "ko": "히어로 헐크 및 몬스터 헐크 최대 체력 +$1",
        "ja": "Hero HulkとMonster Hulkの最大体力+$1"
    },
    {
        "regex": r"^First strike:\s*(\d+(?:\.\d+)?(?:s|%|));\s*second strike:\s*(\d+(?:\.\d+)?(?:s|%|));\s*third strike:\s*(\d+(?:\.\d+)?(?:s|%|))$",
        "ko": "1타: $1 | 2타: $2 | 3타: $3",
        "ja": "1撃目: $1 | 2撃目: $2 | 3撃目: $3"
    },
    {
        "regex": r"^First three strikes:\s*(\d+(?:\.\d+)?(?:s|%|));\s*the fo(?:u)?rth strike:\s*(\d+(?:\.\d+)?(?:s|%|))\b\.?$",
        "ko": "1~3타: $1 | 4타: $2",
        "ja": "1~3撃目: $1 | 4撃目: $2"
    },
    {
        "regex": r"^First three strikes:\s*(\d+(?:\.\d+)?s)\s*per hit;\s*the fo(?:u)?rth strike:\s*(\d+(?:\.\d+)?s)\s*per hit\.?$",
        "ko": "1~3타: 타격당 $1 | 4타: 타격당 $2",
        "ja": "1~3撃目: 1撃あたり$1 | 4撃目: 1撃あたり$2"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*hits?\s*per second$",
        "ko": "초당 $1회 타격",
        "ja": "毎秒 $1回ヒット"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*strikes?\s*per second$",
        "ko": "초당 $1회 타격",
        "ja": "毎秒 $1回ヒット"
    },
    {
        "regex": r"^Consume (\d+) Life Orbs?$",
        "ko": "Life Orb $1개 소모",
        "ja": "Life Orb $1個消費"
    },
    {
        "regex": r"^\+(\d+)\s*Max Health$",
        "ko": "최대 체력 +$1",
        "ja": "最大体力 +$1"
    },
    {
        "regex": r"^Gain (\d+) Fury on hit$",
        "ko": "적중 시 Fury $1 획득",
        "ja": "命中時Fury $1 獲得"
    },
    {
        "regex": r"^(\d+)\s*cards? per unleash$",
        "ko": "시전당 카드 $1장",
        "ja": "発動ごとにカード $1枚"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*health per round$",
        "ko": "발당 체력 $1 회복",
        "ja": "1発あたり体力 $1 回復"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*per field$",
        "ko": "장판당 $1",
        "ja": "フィールドあたり $1"
    },
    {
        "regex": r"^To allies and self:\s*(\d+(?:\.\d+)?)/hit$",
        "ko": "아군 및 자신: 타격당 $1",
        "ja": "味方および自身: 1ヒットあたり$1"
    },
    {
        "regex": r"^Unleash:\s*(\d+(?:\.\d+)?);\s*return:\s*(\d+(?:\.\d+)?)$",
        "ko": "방출 시: $1 | 회수 시: $2",
        "ja": "放出時: $1 | 回収時: $2"
    },
    {
        "regex": r"^First unleash:\s*(\d+(?:\.\d+)?s);\s*second unleash:\s*(\d+(?:\.\d+)?s);\s*third unleash:\s*(\d+(?:\.\d+)?s)$",
        "ko": "1차: $1 | 2차: $2 | 3차: $3",
        "ja": "1回目: $1 | 2回目: $2 | 3回目: $3"
    },
    {
        "regex": r"^Cone shape spell field,\s*angle range:\s*(\d+°),\s*length:\s*(\d+(?:\.\d+)?m)$",
        "ko": "부채꼴 장판 (각도: $1, 사거리: $2)",
        "ja": "扇状フィールド（角度: $1、射程: $2）"
    },
    {
        "regex": r"^Upon activation:\s*(\d+(?:\.\d+)?/s);\s*challenge completed:\s*(\d+(?:\.\d+)?/s)$",
        "ko": "발동 시: 초당 $1 | 챌린지 완료 시: 초당 $2",
        "ja": "発動時: 毎秒$1 | チャレンジ完了時: 毎秒$2"
    }
]

# 3. Exact Stat Values (Casting mechanisms, UI keywords, special mechanics)
NEW_VALUES = {
    # Standard Casting Methods & Mechanics
    "Melee": {
        "ko": "근접",
        "ja": "近接"
    },
    "Dash": {
        "ko": "돌진",
        "ja": "ダッシュ"
    },
    "Charged Dash": {
        "ko": "충전 돌진",
        "ja": "チャージダッシュ"
    },
    "Transformation": {
        "ko": "변신",
        "ja": "変身"
    },
    "Movement-based damage ability": {
        "ko": "이동 기반 피해 스킬",
        "ja": "移動系ダメージアビリティ"
    },
    "Single-cast Spell Field": {
        "ko": "단일 설치 장판",
        "ja": "単発設置フィールド"
    },
    "Persistent Spell Field": {
        "ko": "지속 장판",
        "ja": "継続フィールド"
    },
    "Spherical Spell Field": {
        "ko": "구형 장판",
        "ja": "球状フィールド"
    },
    "Cylindrical Spell Field": {
        "ko": "원기둥형 장판",
        "ja": "円柱状フィールド"
    },
    "Spell Field": {
        "ko": "장판 (필드)",
        "ja": "フィールド"
    },
    "The spell field advances along the casting path": {
        "ko": "시전 경로를 따라 장판 전진",
        "ja": "射出軌道に沿ってフィールド前進"
    },
    "Single-cast projectile with delayed impact": {
        "ko": "시간차 폭발 단일 투사체",
        "ja": "時間差着弾の単発弾"
    },
    "Single-cast projectile with delayed impact that also generates a spell field": {
        "ko": "착탄 시 장판을 생성하는 시간차 단일 투사체",
        "ja": "着弾時にフィールドを生成する時間差単発弾"
    },
    "Straight-line projectile that generates a spell field upon impact": {
        "ko": "착탄 시 장판을 생성하는 직선 투사체",
        "ja": "着弾時にフィールドを生成する直線弾"
    },
    "Projectile that fires in a straight trajectory": {
        "ko": "직선 궤도 투사체",
        "ja": "直線軌道弾"
    },
    "Arced projectile that generates a spell field upon impact": {
        "ko": "착탄 시 장판을 생성하는 곡사 투사체",
        "ja": "着弾時にフィールドを生成する曲射弾"
    },
    "Projectile that generates a spell field upon impact": {
        "ko": "착탄 시 장판을 생성하는 투사체",
        "ja": "着弾時にフィールドを生成する弾"
    },
    "Single-cast spell field that surrounds the caster": {
        "ko": "시전자 중심 단일 장판",
        "ja": "術者周囲単発フィールド"
    },
    "Rapid-fire projectile": {
        "ko": "연사 투사체",
        "ja": "連射弾"
    },
    "Shotgun projectiles that hit instantly": {
        "ko": "즉발 산탄 투사체",
        "ja": "即着散弾"
    },
    "Single-cast projectile that can pierce through enemies": {
        "ko": "관통 단일 투사체",
        "ja": "貫通単発弾"
    },
    "Single-cast projectile with a downward delay that creates a spell field upon impact": {
        "ko": "착탄 시 장판을 생성하는 하향 시간차 투사체",
        "ja": "着弾時にフィールドを生成する時間差落下弾"
    },

    # Standard Keywords
    "Infinite": {
        "ko": "무제한",
        "ja": "無制限"
    },
    "None": {
        "ko": "없음",
        "ja": "なし"
    },
    "Yes": {
        "ko": "적용",
        "ja": "あり"
    },
    "No": {
        "ko": "미적용",
        "ja": "なし"
    },
    "Targeted": {
        "ko": "대상 지정",
        "ja": "ターゲット指定"
    },
    "Self": {
        "ko": "자신",
        "ja": "自身"
    },
    "Continuous": {
        "ko": "지속 시전",
        "ja": "継続発動"
    },
    "Passive": {
        "ko": "패시브",
        "ja": "パッシブ"
    },

    # Hero Special Mechanics Descriptions
    "Veil of Lightforce & Terror Cape share charges, capped out at 2 with each taking 10s to recharge. After using either, both abilities enter a 2s cooldown": {
        "ko": "Veil of Lightforce와 Terror Cape는 충전을 공유하며(최대 2회, 충전당 10초), 어느 하나를 사용하면 두 스킬 모두 2초의 쿨다운에 들어갑니다.",
        "ja": "Veil of LightforceとTerror Capeはチャージを共有し（最大2回、1回10秒）、どちらかを使用すると両方のアビリティが2秒のクールダウンに入ります。"
    },
    "Upon activation: 15%; challenge completed: 30%": {
        "ko": "시전 시: 15% | 챌린지 완료 시: 30%",
        "ja": "発動時: 15% | チャレンジ完了時: 30%"
    },
    "Disrupt enemies' vision in range and gain XP. Enemies can damage Deadpool to end the disruption.": {
        "ko": "범위 내 적의 시야를 방해하고 경험치를 획득합니다. 적이 데드풀에게 피해를 주면 방해가 조기 종료됩니다.",
        "ja": "範囲内の敵の視界を妨害して経験値を獲得。敵がデッドプールにダメージを与えると妨害が解除されます。"
    },
    "The healing factor kicks in after Deadpool has been out of combat for 5s. If Deadpool takes more than 200 damage within a two-second window, the healing factor activates and boosts the healing": {
        "ko": "5초간 비전투 시 Healing Factor가 작동합니다. 2초 내에 200 이상의 피해를 입으면 Healing Factor가 즉시 활성화되어 치유량이 대폭 증가합니다.",
        "ja": "5秒間非戦闘時にHealing Factorが起動。2秒以内に200以上のダメージを受けると発動して回復量が急増します。"
    },
    "The ultimate ability can be unleashed after reaching an S rating. The rating is cleared if Deadpool is defeated.": {
        "ko": "S 등급에 도달하면 궁극기를 사용할 수 있습니다. 데드풀이 처치되면 등급이 초기화됩니다.",
        "ja": "Sランク到達でアルティメットが解放。デッドプールが倒されるとランクはリセットされます。"
    },
    "The caster is immobilized during the transformation process and gains Invincibility": {
        "ko": "변신 과정 동안 시전자는 이동이 제한되며 무적 상태가 됩니다.",
        "ja": "変身中、術者は移動不可となり無敵状態を獲得します。"
    },
    "Heavy Blow and Gamma Burst can detect and damage irradiated enemies, and prematurely remove the status": {
        "ko": "Heavy Blow와 Gamma Burst로 피폭된 적을 감지 및 공격할 수 있으며 해당 상태를 조기 해제합니다.",
        "ja": "Heavy BlowとGamma Burstで被曝した敵を感知・攻撃可能で、状態を早期解除します。"
    },
    "100%, up to 50; shares the Bonus Health cap with Shadow Harvest": {
        "ko": "100% (최대 50, Shadow Harvest와 추가 체력 상한 공유)",
        "ja": "100%（最大50、Shadow Harvestと追加HP上限共有）"
    },
    "After every 5 beam bullets fired, the next shot fires 1 additional projectile": {
        "ko": "광선 탄환 5발 발사 후, 다음 사격 시 추가 투사체 1발을 발사합니다.",
        "ja": "ビーム弾を5発発射するたび、次の射撃で追加の弾を1発発射します。"
    },
    "Convert damage taken into Bonus Health": {
        "ko": "받은 피해를 추가 체력으로 전환합니다.",
        "ja": "受けるダメージを追加HPに変換します。"
    },
    "Hit while wielding the gun, inflict Slow effect to the enemy; hit while wielding the sword,  deal Healing Reduction to the enemy": {
        "ko": "총 장착 중 적중 시 감속 효과를 부여하고, 검 장착 중 적중 시 치유 감소를 부여합니다.",
        "ja": "銃の構えでの命中で敵に鈍足を付与、刀の構えでの命中で敵に被回復減少を付与します。"
    },
    "A cylindrical spell field in melee range": {
        "ko": "근접 범위 원기둥형 장판",
        "ja": "近接範囲円柱状フィールド"
    },
    "A cuboid spell field in melee range": {
        "ko": "근접 범위 직육면체형 장판",
        "ja": "近接範囲直方体フィールド"
    },
    "Projectile with an arced trajectory": {
        "ko": "곡사 궤도 투사체",
        "ja": "弧状軌道の投射弾"
    },
    "∞": {
        "ko": "무제한",
        "ja": "無制限"
    },
    "Allies within the area gain Invisibility and Movement Boost": {
        "ko": "범위 내 아군 투명화 및 이동 속도 증가",
        "ja": "範囲内の味方に不可視化と移動速度上昇"
    },
    "Press Space during the Incredible Leap to cling to the wall you encounter": {
        "ko": "Incredible Leap 도중 Space를 누르면 마주친 벽에 달라붙습니다.",
        "ja": "Incredible Leap中にSpaceを押すと接触した壁にしがみつきます。"
    },
    "Magik is invincible while moving": {
        "ko": "이동 중 Magik 무적 상태",
        "ja": "移動中Magik無敵状態"
    },
    "Attacks will target the nearest enemy to the crosshair, dealing damage": {
        "ko": "조준점에 가장 가까운 적을 자동 타격하여 피해를 입힙니다.",
        "ja": "照準に最も近い敵を自動攻撃しダメージを与えます。"
    },
    "Gambit and the targeted ally receive the Purify and Jump Boost effect.": {
        "ko": "Gambit과 대상 아군이 정화 및 점프력 증가 효과를 얻습니다.",
        "ja": "Gambitと対象の味方が浄化およびジャンプ力強化効果を獲得します。"
    },
    "Refresh the cooldown if it hits an enemy for up to 2 times.": {
        "ko": "적에게 적중 시 최대 2회까지 쿨다운이 초기화됩니다.",
        "ja": "敵に命中時、最大2回までクールダウンがリセットされます。"
    },
    "Refresh the cooldown if it hits an enemy for up to 2 times. Deadpool bounces as the ability hits an enemy.": {
        "ko": "적 적중 시 최대 2회 쿨다운이 초기화되며 데드풀이 적중 반동으로 튕겨 나갑니다.",
        "ja": "敵命中時に最大2回クールダウンがリセットされ、デッドプールが跳ね返ります。"
    },
    "Accumulate XP in battle. When maxed, choose an ability to upgrade for powerful boosts": {
        "ko": "전투 중 경험치를 획득하며 가득 차면 스킬을 업그레이드하여 강력한 강화를 얻습니다.",
        "ja": "戦闘で経験値を溜め、満タン時にアビリティを強化して強力なバフを獲得します。"
    }
}

def main():
    if not os.path.exists(STATS_PATH):
        raise FileNotFoundError(f"Stats file not found: {STATS_PATH}")

    with open(STATS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    labels = data.get('labels', {})
    values = data.get('values', {})
    patterns = data.get('patterns', [])

    print(f"Loaded existing stats.json: {len(labels)} labels, {len(values)} values, {len(patterns)} patterns")

    # 1. Update Labels
    added_labels = 0
    for k, v in NEW_LABELS.items():
        if k not in labels or labels[k].get('ko') != v.get('ko'):
            labels[k] = v
            added_labels += 1
    print(f"Added/updated {added_labels} stat labels.")

    # 2. Update Patterns (avoid duplicate regexes)
    existing_regexes = {p.get('regex') for p in patterns}
    added_patterns = 0
    for p in NEW_PATTERNS:
        if p['regex'] not in existing_regexes:
            patterns.append(p)
            existing_regexes.add(p['regex'])
            added_patterns += 1
    print(f"Added {added_patterns} dynamic regex patterns.")

    # 3. Update Values
    added_values = 0
    for k, v in NEW_VALUES.items():
        values[k] = v
        added_values += 1
    print(f"Added/updated {added_values} stat values.")

    # 4. Purity & Placeholder Validation
    purity_errors = 0
    def check_purity(obj, path=""):
        nonlocal purity_errors
        if not obj or not isinstance(obj, dict):
            return
        ko = obj.get('ko', '')
        ja = obj.get('ja', '')
        if isinstance(ko, str):
            if JAPANESE_REGEX.search(ko):
                print(f"❌ Purity Error at {path}.ko: Japanese kana in Korean: '{ko}'")
                purity_errors += 1
            if '의 스킬입니다' in ko:
                print(f"❌ Placeholder Error at {path}.ko: '{ko}'")
                purity_errors += 1
        if isinstance(ja, str):
            if KOREAN_REGEX.search(ja):
                print(f"❌ Purity Error at {path}.ja: Korean hangul in Japanese: '{ja}'")
                purity_errors += 1
            if 'のスキル' in ja and ('のスキル。' in ja or 'のスキルです' in ja):
                print(f"❌ Placeholder Error at {path}.ja: '{ja}'")
                purity_errors += 1

    for k, v in labels.items():
        check_purity(v, f"labels['{k}']")
    for k, v in values.items():
        check_purity(v, f"values['{k}']")
    for idx, p in enumerate(patterns):
        check_purity(p, f"patterns[{idx}]")

    if purity_errors > 0:
        raise ValueError(f"Purity checks failed with {purity_errors} errors!")

    print("✅ All purity checks passed (0 Kana in KO, 0 Hangul in JA, 0 placeholders)!")

    # Save
    data['labels'] = labels
    data['values'] = values
    data['patterns'] = patterns

    with open(STATS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"🎉 Successfully updated {STATS_PATH} ({len(labels)} labels, {len(values)} values, {len(patterns)} patterns)")

if __name__ == '__main__':
    main()
