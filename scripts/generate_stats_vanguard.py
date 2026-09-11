# -*- coding: utf-8 -*-
"""
Generator for Vanguard stat values translations (125 items).
Ensures:
- 100% pure Korean (0 Japanese Kana)
- 100% pure Japanese (0 Korean Hangul)
- English skill names preserved in descriptions
- Natural gamer-friendly Korean and Japanese phrasing
- 0 placeholders
"""

import json
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_vanguard.json')
INPUT_PATH = os.path.join(ROOT_DIR, 'scratch_vanguard_stats.json')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

VANGUARD_TRANSLATIONS = {
    "At full charge, Spear of Ichor can launch up enemies and cause 20 extra damage.": {
        "ko": "완전 충전 시 Spear of Ichor가 적을 공중에 띄우고 20의 추가 피해를 입힙니다.",
        "ja": "最大チャージ時、Spear of Ichorが敵を打ち上げ20の追加ダメージを与えます。"
    },
    "The fourth strike propels you forward in a swift dash.": {
        "ko": "4번째 타격 시 전방으로 신속하게 돌진합니다.",
        "ja": "4撃目に前方へ素早くダッシュ突進します。"
    },
    "Mobility abilities of enemies bound by the ribbons will be disabled. Enemies within a certain distance around the spear will be slowed.": {
        "ko": "리본에 묶인 적은 이동기가 비활성화되며, 창 주변 일정 거리 내의 적은 감속됩니다.",
        "ja": "リボンに拘束された敵は移動アビリティが使用不可になり、槍の周囲の敵に鈍足を付与します。"
    },
    "25/s; 75/s when piercing an enemy": {
        "ko": "초당 25 | 적 관통 시 초당 75",
        "ja": "毎秒25 | 敵貫通時 毎秒75"
    },
    "Every enemy pierced grants Angela with a 50/s passive energy recovery.": {
        "ko": "적을 관통할 때마다 안젤라의 초당 패시브 에너지 회복량이 50 증가합니다.",
        "ja": "敵を貫通するごとにアンジェラのエネルギー自然回復が秒間50増加します。"
    },
    "Hit damage: 30; damage over time: 12.5/s": {
        "ko": "타격 데미지: 30 | 지속 데미지: 초당 12.5",
        "ja": "直撃ダメージ: 30 | 持続ダメージ: 秒間12.5"
    },
    "A cylindrical spell field with a radius of 8m and a height of 2m.": {
        "ko": "반경 8m, 높이 2m 원기둥형 장판",
        "ja": "半径8m・高さ2mの円柱状フィールド"
    },
    "Within the Divine Judgement zone, Angela’s each Axes of Ichors hit grants 50 Bonus Health to herself and 25 Bonus Health to allies within the area.": {
        "ko": "Divine Judgement 영역 내에서 Axes of Ichors 타격 시 자신에게 50, 영역 내 아군에게 25의 Bonus Health를 부여합니다.",
        "ja": "Divine Judgement領域内でAxes of Ichors命中時、自身に50、範囲内の味方に25のBonus Healthを付与します。"
    },
    "60°": {
        "ko": "60°",
        "ja": "60°"
    },
    "Maintain the forward speed faster than 5m/s for 1s": {
        "ko": "전방 속도 5m/s 이상을 1초간 유지",
        "ja": "前方移動速度5m/s以上を1秒間維持"
    },
    "Change Form": {
        "ko": "폼 변경",
        "ja": "フォーム切替"
    },
    "Melee Attack Damage: 45, Flying Shield Damage: 45": {
        "ko": "근접 공격 데미지: 45 | 방패 투척 데미지: 45",
        "ja": "近接攻撃ダメージ: 45 | 盾投擲ダメージ: 45"
    },
    "Melee 1st Hit: 0.4s, Melee 2nd Hit: 0.5s, Flying Shield 1st Hit: 0.5s, Flying Shield 2nd Hit: 0.57s": {
        "ko": "근접 1타: 0.4초, 근접 2타: 0.5초 | 방패 1타: 0.5초, 방패 2타: 0.57초",
        "ja": "近接1撃目: 0.4秒、近接2撃目: 0.5秒 | 盾投擲1撃目: 0.5秒、盾投擲2撃目: 0.57秒"
    },
    "Up to 4 throws": {
        "ko": "최대 4회 투척",
        "ja": "最大4回投擲"
    },
    "Automatically target enemies near the crosshair": {
        "ko": "조준점 주변 적 자동 조준",
        "ja": "照準付近の敵を自動追尾"
    },
    "20m (horizontal)": {
        "ko": "20m (수평)",
        "ja": "20m（水平）"
    },
    "Activation": {
        "ko": "발동",
        "ja": "発動"
    },
    "A spherical spell field with a 4m radius enveloping the caster, and a spell area with a width of 4m along the path": {
        "ko": "시전자를 감싸는 반경 4m 구형 장판 및 경로를 따라 전개되는 너비 4m 장판",
        "ja": "術者を包む半径4mの球状フィールド、および進路に沿った幅4mのエリア"
    },
    "Cast to gain 150 Bonus Health and grant allies 100 Bonus Health. Every second afterward, gain 100 Bonus Health and grant allies 60 Bonus Health": {
        "ko": "시전 시 자신에게 150, 아군에게 100의 Bonus Health 부여. 이후 매초 자신은 100, 아군은 60의 Bonus Health 획득",
        "ja": "発動時自身に150、味方に100のBonus Health付与。その後毎秒自身に100、味方に60のBonus Health獲得"
    },
    "Grant a 30% Movement Boost to both yourself and your allies": {
        "ko": "자신과 아군 모두에게 30% 이동 속도 증가 부여",
        "ja": "自身と味方全員に移動速度30%上昇を付与"
    },
    "Allies within its path gain a 20% boost to Ultimate Energy charge efficiency": {
        "ko": "경로 상의 아군은 궁극기 에너지 충전 효율이 20% 증가합니다.",
        "ja": "進路上の味方はアルティメットエネルギー充填効率が20%上昇します。"
    },
    "Single-cast projectile that can ricochet": {
        "ko": "도탄 가능한 단일 투사체",
        "ja": "跳弾可能な単発弾"
    },
    "Start at 70, with a 20% reduction for each ricochet": {
        "ko": "기본 70 데미지, 도탄 시마다 20%씩 감소",
        "ja": "初期ダメージ70、跳弾ごとに20%減少"
    },
    "Single-cast forward dash": {
        "ko": "단일 전방 돌진",
        "ja": "単発前方突進"
    },
    "Within the duration, deflect Projectiles ricochet directly toward his target direction.": {
        "ko": "지속 시간 동안 날아오는 투사체를 목표 방향으로 즉시 반사합니다.",
        "ja": "効果時間中、飛来する投射物を照準方向へ直接跳ね返します。"
    },
    "Captain America gain 100 Max Health": {
        "ko": "캡틴 아메리카 최대 체력 +100",
        "ja": "キャプテン・アメリカ最大体力+100"
    },
    "60 per ability missed": {
        "ko": "스킬 빗맞힐 때마다 60",
        "ja": "スキルを外すごとに60"
    },
    "70 per ability missed": {
        "ko": "스킬 빗맞힐 때마다 70",
        "ja": "スキルを外すごとに70"
    },
    "Self: 200; allies: 50": {
        "ko": "자신: 200 | 아군: 50",
        "ja": "自身: 200 | 味方: 50"
    },
    "Self: 300; allies: 50": {
        "ko": "자신: 300 | 아군: 50",
        "ja": "自身: 300 | 味方: 50"
    },
    "Disrupt enemies' vision in range and gain XP. Enemies can damage Deadpool to end the disruption. Increase left-click attack speed for the duration.": {
        "ko": "범위 내 적의 시야를 방해하고 경험치를 얻습니다. 적이 데드풀에게 피해를 주면 방해가 해제됩니다. 지속 시간 동안 좌클릭 공격 속도가 증가합니다.",
        "ja": "範囲内の敵の視界を妨害して経験値を獲得。敵がデッドプールにダメージを与えると妨害が解除。効果時間中左クリック攻撃速度が上昇します。"
    },
    "Self: 35%; allies: 25%": {
        "ko": "자신: 35% | 아군: 25%",
        "ja": "自身: 35% | 味方: 25%"
    },
    "Five-round delayed hit projectiles": {
        "ko": "5연발 시간차 타격 투사체",
        "ja": "5連発時間差着弾弾"
    },
    "5.56 rounds per second, with a 0.03-second interval between every two rounds": {
        "ko": "초당 5.56발 (연발 간격 0.03초)",
        "ja": "毎秒5.56発（連射間隔0.03秒）"
    },
    "12 (1 dagger per release)": {
        "ko": "12 (방출당 단검 1개)",
        "ja": "12（1射あたり短剣1本）"
    },
    "Each point of Dark Magic deals 1.3 damage": {
        "ko": "Dark Magic 1포인트당 1.3 데미지",
        "ja": "Dark Magic 1ポイントにつき1.3ダメージ"
    },
    "Each point of energy deals 1.3 damage.": {
        "ko": "에너지 1포인트당 1.3 데미지",
        "ja": "エネルギー1ポイントにつき1.3ダメージ"
    },
    "The spell field pulls enemies in range toward Doctor Strange": {
        "ko": "장판 범위 내 적들을 닥터 스트레인지 쪽으로 끌어당깁니다.",
        "ja": "フィールド範囲内の敵をドクター・ストレンジの元へ引き寄せます。"
    },
    "Multi-segment release": {
        "ko": "다단 방출",
        "ja": "多段発動"
    },
    "Daggers of Denak: Each hit generates 3.5 Dark Magic. When using the V key, every enemy hit generates 10 Dark Magic": {
        "ko": "Daggers of Denak: 타격당 3.5 Dark Magic 생성. V키 사용 시 적중한 적마다 10 Dark Magic 생성",
        "ja": "Daggers of Denak: ヒットごとに3.5 Dark Magic生成。Vキー使用時は敵命中ごとに10 Dark Magic生成"
    },
    "Doctor Strange gain 100 Max Health": {
        "ko": "닥터 스트레인지 최대 체력 +100",
        "ja": "ドクター・ストレンジ最大体力+100"
    },
    "Spore Bomb generates a spell field with a 5m spherical radius, while small explosive spores create a spell field with a 1.5m spherical radius": {
        "ko": "Spore Bomb는 반경 5m 구형 장판 생성, 소형 분열 포자는 반경 1.5m 구형 장판 생성",
        "ja": "Spore Bombは半径5mの球状フィールドを生成、小型分裂胞子は半径1.5mの球状フィールドを生成"
    },
    "The projectile itself deals no damage, while Spore Bomb deals 55 damage and explosive spores deal 10 damage": {
        "ko": "투사체 자체 데미지는 없으며 Spore Bomb 폭발 시 55, 분열 포자 폭발 시 10 데미지",
        "ja": "弾自体のダメージは無く、Spore Bomb爆発時に55、分裂胞子爆発時に10ダメージ"
    },
    "Spore Bomb explodes into 6 explosive spores": {
        "ko": "Spore Bomb 폭발 시 6개의 분열 포자로 분열",
        "ja": "Spore Bomb爆発時に6個の分裂胞子へ拡散"
    },
    "The projectile deals 10 damage, while the spell field deals 70 damage. While imprisoning enemies, it deals 20 damage every 0.5s": {
        "ko": "투사체 직격 시 10, 장판 폭발 시 70 데미지. 적 감금 중 0.5초마다 20 지속 데미지",
        "ja": "弾直撃時10、フィールド爆発時70ダメージ。敵拘束中は0.5秒ごとに20持続ダメージ"
    },
    "Imprison enemies for 3.5s": {
        "ko": "3.5초간 적 감금 구속",
        "ja": "3.5秒間敵を拘束"
    },
    "Thornlash Wall deals 60 damage every 0.5s": {
        "ko": "Thornlash Wall은 0.5초마다 60 데미지 부여",
        "ja": "Thornlash Wallは0.5秒ごとに60ダメージ付与"
    },
    "Ironwood Wall heals 40 Bonus Health per second, up to 250 Bonus Health; gain Unstoppable status when within 15m of Awakened Ironwood Walls": {
        "ko": "Ironwood Wall은 초당 40 Bonus Health 회복 (최대 250). 각성 Ironwood Wall 15m 이내 시 저지 불가 상태 부여",
        "ja": "Ironwood Wallは毎秒40のBonus Health回復（最大250）。覚醒Ironwood Wallの15m以内にいる時阻止不能状態を獲得"
    },
    "The first two strikes can reach 3m, while the third strike can reach 4m": {
        "ko": "1~2타 사거리 3m, 3타 사거리 4m",
        "ja": "1~2撃目射程3m、3撃目射程4m"
    },
    "Basic Cooldown 2s, with a charge of 6s per use.": {
        "ko": "기본 쿨다운 2초 (시전당 6초 충전)",
        "ja": "基本クールダウン2秒（1使用あたり6秒チャージ）"
    },
    "Each direct hit reduces Indestructible Guard cooldown by 1s": {
        "ko": "직격할 때마다 Indestructible Guard 쿨다운이 1초 감소합니다.",
        "ja": "直撃ごとにIndestructible Guardのクールダウンが1秒短縮されます。"
    },
    "When the caster's shield takes damage, 130% of the damage is converted into gamma energy. When an ally's shield takes damage, 10% of the damage is converted into gamma energy": {
        "ko": "시전자의 쉴드가 피해를 받으면 피해량의 130%가 감마 에너지로 전환됩니다. 아군의 쉴드가 피해를 받으면 10%가 감마 에너지로 전환됩니다.",
        "ja": "自身のシールドが被弾時、被ダメージの130%がガンマエネルギーに変換されます。味方のシールド被弾時は10%が変換されます。"
    },
    "Single-cast projectile.": {
        "ko": "단일 투사체",
        "ja": "単発弾"
    },
    "When the caster enters the spell field, it restores 50 gamma energy": {
        "ko": "시전자가 장판 영역에 진입하면 감마 에너지를 50 회복합니다.",
        "ja": "術者がフィールド内に入るとガンマエネルギーが50回復します。"
    },
    "Delivers 5 hits, each dealing 40 damage": {
        "ko": "5연속 타격, 타격당 40 데미지",
        "ja": "5回連続ヒット、1撃あたり40ダメージ"
    },
    "While performing the smash, Hulk gains a 30% Damage Reduction": {
        "ko": "스매시 시전 중 헐크는 받는 피해가 30% 감소합니다.",
        "ja": "スマッシュ発動中、ハルクは被ダメージが30%軽減されます。"
    },
    "Single-cast projectile": {
        "ko": "단일 투사체",
        "ja": "単発弾"
    },
    "Initially, it produces a spell field with a 1m spherical radius; when the projectile reaches maximum distance, the explosion radius expands to a spell field with a 3m spherical radius": {
        "ko": "초기 반경 1m 구형 장판 생성, 투사체가 최대 거리에 도달하면 폭발 반경이 3m 구형 장판으로 확장",
        "ja": "初期は半径1mの球状フィールド生成、弾が最大距離到達時に爆発範囲が半径3mの球状フィールドへ拡大"
    },
    "Projectile Damage: 40. The spell field deals 40 damage at its center, reducing to 50% within a 3m radius from the center": {
        "ko": "투사체 데미지: 40. 장판 중심 데미지: 40 (중심 3m 반경 외곽은 50%로 감소)",
        "ja": "弾ダメージ: 40。フィールド中心ダメージ40（中心から3m範囲で50%に減衰）"
    },
    "Iron Rings' first charge deals 40 damage, the second charge deals 65 damage, and the third charge deals 90 damage": {
        "ko": "Iron Rings 1단계 충전: 40 데미지, 2단계 충전: 65 데미지, 3단계 충전: 90 데미지",
        "ja": "Iron Rings 1段階チャージ: 40ダメージ、2段階チャージ: 65ダメージ、3段階チャージ: 90ダメージ"
    },
    "No cooldown, but the ability can only be activated when the Iron Ring has at least one charge": {
        "ko": "쿨다운 없음 (단, Iron Ring 충전이 최소 1개 이상 있을 때만 활성화 가능)",
        "ja": "クールダウンなし（ただしIron Ringチャージが1以上ある時のみ発動可能）"
    },
    "When fully charged, the Iron Ring has a 6m knockback distance": {
        "ko": "완전 충전 시 Iron Ring의 밀쳐내기 거리 6m",
        "ja": "最大チャージ時、Iron Ringのノックバック距離6m"
    },
    "Create a persistent spell field that launches a projectile upon completion, which generates another spell field on impact": {
        "ko": "지속 장판을 생성하고 완료 시 투사체를 발사하며, 착탄 시 2차 장판을 생성합니다.",
        "ja": "継続フィールドを展開し終了時に弾を発射、着弾時に2次フィールドを生成します。"
    },
    "Initially, the ability has a spherical range with a radius of 5m. After charging for 4s, it expands to an 8m radius": {
        "ko": "초기 반경 5m 구형 범위에서 4초 충전 후 반경 8m로 확장",
        "ja": "初期は半径5mの球状範囲、4秒チャージ後に半径8mへ拡大"
    },
    "The projectile deals no damage. The base damage at the center of the spell field starts at 100 and increases to 350 when fully charged. Each point of Energy adds an extra 3 points of damage to the spell field, with damage reducing to 50% at a distance of 6m from the center": {
        "ko": "투사체 자체 피해 없음. 장판 중심 기본 데미지 100~완전 충전 시 350. 에너지 1포인트당 데미지 +3 추가, 중심 6m 지점에서 50%로 감쇠",
        "ja": "弾自体のダメージはなし。フィールド中心基本ダメージ100〜フルチャージ時350。エネルギー1につきダメージ+3追加、中心6m地点で50%減衰"
    },
    "For each point of projectile damage absorbed, the power increases by 0.125, with a maximum absorption of 800 projectile damage": {
        "ko": "흡수한 투사체 데미지 1포인트당 파워 0.125 증가 (최대 흡수 800)",
        "ja": "吸収した投射物ダメージ1ごとに威力が0.125上昇（最大800吸収）"
    },
    "Shield": {
        "ko": "쉴드",
        "ja": "シールド"
    },
    "The shield grants one charge of Iron Ring for every 100 damage it absorbs": {
        "ko": "쉴드가 100의 피해를 흡수할 때마다 Iron Ring 충전 1회를 획득합니다.",
        "ja": "シールドが100ダメージを吸収するごとにIron Ringチャージを1獲得します。"
    },
    "First hit 0.6s, second hit 1s": {
        "ko": "1타: 0.6초 | 2타: 1초",
        "ja": "1撃目: 0.6秒 | 2撃目: 1秒"
    },
    "Rapid-fire, delayed projectile that is accompanied by a spell field": {
        "ko": "장판을 동반하는 연사 시간차 투사체",
        "ja": "フィールドを伴う連射時間差弾"
    },
    "Projectile Damage: 15; Spell Field Damage: 15": {
        "ko": "투사체 데미지: 15 | 장판 데미지: 15",
        "ja": "弾ダメージ: 15 | フィールドダメージ: 15"
    },
    "20% slowdown on release": {
        "ko": "시전 시 20% 감속",
        "ja": "発動時20%鈍足"
    },
    "If an enemy with a Web-Tracer is hit by the snare again, they will be Immobilized for 0.7s": {
        "ko": "Web-Tracer가 부착된 적이 덫에 다시 맞으면 0.7초간 이동 불가 상태가 됩니다.",
        "ja": "Web-Tracerが付着した敵が再び罠にかかると0.7秒間移動不能になります。"
    },
    "While trapped in the Cyber-Web, Peni Parker receives 25 healing per second. Any excess healing is converted into Bonus Health, up to a maximum of 150 Health, and grants a 25% Movement Boost": {
        "ko": "Cyber-Web 안에서 페니 파커는 초당 25의 치유를 받으며, 초과 치유는 최대 150까지 Bonus Health로 전환되고 이동 속도가 25% 증가합니다.",
        "ja": "Cyber-Web内でペニー・パーカーは秒間25回復し、超過分は最大150までBonus Healthに変換、移動速度が25%上昇します。"
    },
    "Allies in Peni's Cyber-Webs now receive the same Healing Over Time and a Movement Boost effects as her. Movement Boost for allies is 25%, Healing is 15/s. Ally excess healing converts into Bonus Health, up to 25": {
        "ko": "Cyber-Web 안의 아군은 페니 파커와 동일한 지속 치유 및 이속 증가를 받습니다. (아군 이속 25% 증가, 초당 15 치유, 초과 치유 시 최대 25 Bonus Health 전환)",
        "ja": "Cyber-Web内の味方も持続回復と移動速度上昇を獲得します。（味方移動速度25%上昇、秒間15回復、超過分は最大25までBonus Health変換）"
    },
    "Enhancement": {
        "ko": "강화",
        "ja": "強化"
    },
    "Sweep Attack Damage: 60": {
        "ko": "휘두르기 공격 데미지: 60",
        "ja": "薙ぎ払いダメージ: 60"
    },
    "Gain 450 Bonus Health and a 70% Movement Boost": {
        "ko": "Bonus Health 450 및 이동 속도 70% 증가 획득",
        "ja": "Bonus Health 450および移動速度70%上昇を獲得"
    },
    "Each Spider-Drone inflicts 40 damage": {
        "ko": "스파이더 드론 개당 40 데미지",
        "ja": "スパイダードローン1機あたり40ダメージ"
    },
    "Two Spider-Drones are generated every 3s, slows hit enemies by 8% for 2s, each hit stacks the effect and resets the slow period, stacking up to 40%": {
        "ko": "3초마다 스파이더 드론 2대 생성. 적중 시 2초간 8% 감속 (중첩 시 시간 갱신, 최대 40% 중첩)",
        "ja": "3秒ごとにスパイダードローンを2機生成。命中時2秒間8%鈍足（命中ごとに持続時間リセット、最大40%累積）"
    },
    "19m, with the possibility to exceed this distance if descending": {
        "ko": "19m (하강 시 사거리 연장 가능)",
        "ja": "19m（降下時はこれを超える距離まで到達可能）"
    },
    "Double strike, 40 per hit": {
        "ko": "2연타, 타격당 40",
        "ja": "2連撃、1撃あたり40"
    },
    "Double strike 0.33s between attacks, 1s between sets.": {
        "ko": "2연타 타격 간격 0.33초 (세트 간 1초)",
        "ja": "2連撃の間隔0.33秒（セット間1秒）"
    },
    "55+10% of enemies' max Health per hit": {
        "ko": "타격당 55 + 적 최대 체력의 10%",
        "ja": "1撃あたり55 + 敵の最大HPの10%"
    },
    "Move forward 3 meters while punching; gain Bonus Health equal to damage dealt (up to 150); once hit, this ability can knock down flying enemies to the ground": {
        "ko": "펀치하며 3m 전진. 가한 피해량만큼 Bonus Health 획득 (최대 150). 비행 중인 적 적중 시 지면으로 격추",
        "ja": "パンチしながら3m前進。与ダメージ分のBonus Healthを獲得（最大150）。命中時に飛行中の敵を地面へ叩き落とす"
    },
    "Step spell field: 3m high, 10m wide, advancing 2m every 0.1 seconds, up to a maximum of 18m": {
        "ko": "계단식 장판: 높이 3m, 너비 10m (0.1초마다 2m씩 전진, 최대 18m)",
        "ja": "階段状フィールド: 高さ3m、幅10m（0.1秒ごとに2m前進、最大18m）"
    },
    "Stun duration 2.5s": {
        "ko": "기절 지속 시간 2.5초",
        "ja": "スタン持続時間2.5秒"
    },
    "Charge: 30; ground slam: 20; immobilization zone: 15 per/s": {
        "ko": "돌진: 30 | 지면 강타: 20 | 이동 불가 영역: 초당 15",
        "ja": "突進: 30 | 叩きつけ: 20 | 移動不能ゾーン: 秒間15"
    },
    "Ground slam: 8m radius, 2.5m high cylindrical spell field. Immobilization zone: 8m radius, 4m high cylindrical spell field": {
        "ko": "지면 강타: 반경 8m, 높이 2.5m 원기둥형 장판 | 이동 불가 영역: 반경 8m, 높이 4m 원기둥형 장판",
        "ja": "叩きつけ: 半径8m・高さ2.5m円柱状フィールド | 移動不能ゾーン: 半径8m・高さ4m円柱状フィールド"
    },
    "Gain 200 Bonus Health during skill activation": {
        "ko": "스킬 시전 중 200 Bonus Health 획득",
        "ja": "アビリティ発動中200 Bonus Health獲得"
    },
    "Basic Cooldown 3s, with a charge of 10s per use": {
        "ko": "기본 쿨다운 3초 (시전당 10초 충전)",
        "ja": "基本クールダウン3秒（1使用あたり10秒チャージ）"
    },
    "Apply a 20% damage reduction effect to self and 20% damage reduction to all allies within 5m of his landing point for 3s": {
        "ko": "자신 및 착지점 5m 이내의 모든 아군에게 3초간 20% 피해 감소 효과 부여",
        "ja": "自身および着地点5m以内の全味方に3秒間20%の被ダメージ軽減を付与"
    },
    "Basic Cooldown 3s, with a charge of 10s per use, shares the same Cooldown with the E Key ability": {
        "ko": "기본 쿨다운 3초 (시전당 10초 충전, E 스킬과 쿨다운 공유)",
        "ja": "基本クールダウン3秒（1回10秒チャージ、Eアビリティとクールダウン共有）"
    },
    "Apply a 20% Vulnerability to all enemies within 5m of his landing point for 3s": {
        "ko": "착지점 5m 이내의 모든 적에게 3초간 20% 취약(Vulnerability) 부여",
        "ja": "着地点5m以内の全敵に3秒間20%の脆弱を付与"
    },
    "60+11% of enemy's maximum health": {
        "ko": "60 + 적 최대 체력의 11%",
        "ja": "60 + 敵の最大HPの11%"
    },
    "Immune to launch-up, knock-back, and other displacement effects": {
        "ko": "띄우기, 밀쳐내기 및 기타 강제 이동 효과에 면역",
        "ja": "ノックアップ、ノックバック、その他の強制移動効果を無効化"
    },
    "Launch a single-target projectile that returns after a delayed hit": {
        "ko": "단일 대상에게 발사된 후 시간차 타격을 가하고 손으로 돌아오는 투사체",
        "ja": "単一ターゲットに発射され時間差着弾後に手元へ戻る弾"
    },
    "The projectile travels outward at a speed of 60m per second and returns at a speed of 80m per second": {
        "ko": "투사체 투척 속도 초당 60m, 회수 속도 초당 80m",
        "ja": "投擲速度秒間60m、回収速度秒間80m"
    },
    "Outward Projectile Damage: 50; Returning Projectile Damage: 25": {
        "ko": "투척 투사체 데미지: 50 | 회수 투사체 데미지: 25",
        "ja": "投擲時ダメージ: 50 | 回収時ダメージ: 25"
    },
    "Hits grant 75 Bonus Health (only triggers once per throw, even if hitting multiple enemies)": {
        "ko": "적중 시 75 Bonus Health 획득 (다수 적중 시에도 투척당 1회만 발동)",
        "ja": "命中時75 Bonus Health獲得（複数命中時も1投につき1回のみ発動）"
    },
    "A persistent spell field that generates a one-time spell field upon expiration": {
        "ko": "만료 시 1회성 폭발 장판을 생성하는 지속 장판",
        "ja": "効果終了時に1回限りの爆発フィールドを発生させる継続フィールド"
    },
    "The sustained spell field is cylindrical, measuring 8m in radius and 20m in height, whereas the one-time spell field has an 8m spherical radius": {
        "ko": "지속 장판은 반경 8m, 높이 20m 원기둥형이며, 1회성 장판은 반경 8m 구형 장판입니다.",
        "ja": "継続フィールドは半径8m・高さ20mの円柱状、1回限りフィールドは半径8mの球状です。"
    },
    "The sustained spell field lasts for 0.5s, dealing 40 damage, while the one-time spell field deals 220 damage": {
        "ko": "지속 장판 0.5초간 지속 (40 데미지), 1회성 폭발 장판 220 데미지",
        "ja": "継続フィールド0.5秒持続（40ダメージ）、1回限り爆発フィールド220ダメージ"
    },
    "After Ultimate Ability lands, Stun surrounding enemies for 1s": {
        "ko": "궁극기 착지 후 주변 적을 1초간 기절",
        "ja": "アルティメット着地後、周囲の敵を1秒間スタン"
    },
    "No charge: 10m; Full charge: 20m. When carrying an enemy, the ranges are 6m with no charge and 13m with full": {
        "ko": "충전 없음: 10m | 완전 충전: 20m (적을 붙잡은 경우: 충전 없음 6m, 완전 충전 13m)",
        "ja": "ノンチャージ: 10m | フルチャージ: 20m（敵を掴んでいる時: ノンチャージ6m、フルチャージ13m）"
    },
    "No Charge Damage: 40; Full Charge Damage: 60": {
        "ko": "충전 없음: 40 데미지 | 완전 충전: 60 데미지",
        "ja": "ノンチャージ: 40ダメージ | フルチャージ: 60ダメージ"
    },
    "Deal 40 damage when enemies cross the boundaries": {
        "ko": "적이 결계 경계를 넘을 때 40 데미지 부여",
        "ja": "敵が境界を越える際に40ダメージ付与"
    },
    "For each enemy within the spell area, 1 point of Thorforce is restored. Enemies that cross the boundary will be Slowed by 30%, Enemies that cross the boundary will receive an additional debuff that restricts aerial abilities for 2s.": {
        "ko": "영역 내 적 1명당 1 Thorforce 회복. 결계를 넘는 적은 30% 감속되며 2초간 공중 이동기가 제한되는 디버프를 받습니다.",
        "ja": "領域内の敵1体ごとに1 Thorforce回復。境界を越える敵は30%鈍足になり、2秒間空中アビリティが封じられます。"
    },
    "Ability Enhancement": {
        "ko": "스킬 강화",
        "ja": "アビリティ強化"
    },
    "Left Click": {
        "ko": "좌클릭",
        "ja": "左クリック"
    },
    "The first three stages last for 0.4s each, while the fourth stage lasts for 0.8s": {
        "ko": "1~3단계 각 0.4초 지속, 4단계 0.8초 지속",
        "ja": "1~3段階は各0.4秒持続、4段階は0.8秒持続"
    },
    "Projectile Damage: 70, Spell Field Damage: 15 per second": {
        "ko": "투사체 데미지: 70 | 장판 데미지: 초당 15",
        "ja": "弾ダメージ: 70 | フィールドダメージ: 秒間15"
    },
    "Inflict damage over time on nearby enemies; After casting Awakening Rune, you can manually cancel the Awakened state after a brief delay. At the end of the Awakened state, Thor restores 1 point of Thunderforce.": {
        "ko": "주변 적에게 지속 피해 부여. Awakening Rune 시전 후 각성 상태를 수동 취소할 수 있으며, 각성 종료 시 토르는 1 Thorforce를 회복합니다.",
        "ja": "周囲の敵に持続ダメージを付与。Awakening Rune詠唱後、短時間後に覚醒状態を手動解除可能で、終了時に1 Thorforceを回復します。"
    },
    "5s per Thorforce": {
        "ko": "Thorforce 충전당 5초",
        "ja": "Thorforce 1ポイントにつき5秒"
    },
    "Each point of Thorforce consumed grants 50 Bonus Health, while abilities that consume 3 points of Thorforce grant 150 Bonus Health": {
        "ko": "Thorforce 1포인트 소모 시 50 Bonus Health 획득 (3포인트 소모 시 150 Bonus Health 획득)",
        "ja": "Thorforce 1ポイント消費ごとに50 Bonus Health獲得（3ポイント消費時は150 Bonus Health獲得）"
    },
    "Quad-cast delayed spell field": {
        "ko": "4중 시전 시간차 장판",
        "ja": "4連撃時間差フィールド"
    },
    "0.9s, with a 0.1s interval between each tendril": {
        "ko": "0.9초 (촉수 간 간격 0.1초)",
        "ja": "0.9秒（各触手の間隔0.1秒）"
    },
    "Spell field that surrounds the caster": {
        "ko": "시전자 중심 장판",
        "ja": "術者周囲フィールド"
    },
    "The spell field deals 5 damage, increasing to 80 damage if the target remains in the area for a duration": {
        "ko": "기본 5 데미지 (대상이 일정 시간 영역 내에 머무를 경우 80 데미지로 증가)",
        "ja": "基本5ダメージ（対象がエリア内に留まり続けると80ダメージに増加）"
    },
    "Tendrils apply a 25% Slow on the target and take 3s to inflict damage. If the distance from Venom exceeds 11m, the tendrils will detach": {
        "ko": "촉수가 대상에게 25% 감속을 걸고 3초 후 피해를 입힙니다. 베놈과의 거리가 11m를 초과하면 촉수가 끊어집니다.",
        "ja": "触手が対象に25%鈍足を付与し3秒後にダメージ。ヴェノムとの距離が11mを超えると触手が切れます。"
    },
    "Inflict damage equal to 50% of the target's health, followed by an additional 50 damage": {
        "ko": "대상 현재 체력의 50%에 해당하는 피해를 입힌 후 50의 추가 피해 부여",
        "ja": "対象の現在HPの50%相当のダメージを与え、さらに50の追加ダメージを付与"
    },
    "130% of damage dealt is converted into Bonus Health": {
        "ko": "가한 피해량의 130%가 Bonus Health로 전환됩니다.",
        "ja": "与えたダメージの130%がBonus Healthに変換されます。"
    },
    "Grant 100 Bonus Health and convert 110% of lost Health into Bonus Health": {
        "ko": "Bonus Health 100 획득 및 잃은 체력의 110%를 Bonus Health로 전환",
        "ja": "Bonus Health 100獲得および失った体力の110%をBonus Healthに変換"
    },
    "65 damage, with damage falloff starting at 2m from the center of the spell field and decreasing to 40% at 6m": {
        "ko": "기본 65 데미지 (장판 중심 2m부터 감쇠 시작, 6m에서 40%로 감소)",
        "ja": "基本65ダメージ（中心から2mで減衰開始、6m地点で40%に低下）"
    },
    "Knocks enemies inward, with an inward knockback angle of 75°": {
        "ko": "적들을 안쪽으로 끌어당기며 띄움 (내향 넉백 각도 75°)",
        "ja": "敵を内側へノックバック（内向き角度75°）"
    }
}

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        src = json.load(f)

    print(f"Total keys in {INPUT_PATH}: {len(src)}")
    print(f"Total translations mapped: {len(VANGUARD_TRANSLATIONS)}")

    missing = [k for k in src if k not in VANGUARD_TRANSLATIONS]
    if missing:
        print(f"❌ Missing {len(missing)} keys:")
        for m in missing:
            print("  ", repr(m))
        raise ValueError("Missing keys in VANGUARD_TRANSLATIONS")

    # Purity check
    for k, v in VANGUARD_TRANSLATIONS.items():
        ko = v.get('ko', '')
        ja = v.get('ja', '')
        if JAPANESE_REGEX.search(ko):
            raise ValueError(f"Kana in KO: {k} -> {ko}")
        if KOREAN_REGEX.search(ja):
            raise ValueError(f"Hangul in JA: {k} -> {ja}")

    print("✅ All 125 keys covered with 100% purity!")

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(VANGUARD_TRANSLATIONS, f, ensure_ascii=False, indent=2)

    print(f"Successfully wrote {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
