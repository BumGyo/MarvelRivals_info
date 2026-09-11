# -*- coding: utf-8 -*-
"""
Generator for Duelists A stat values translations (116 items).
Black Panther, Blade, Black Widow, Hawkeye, Hela, Human Torch, Iron Fist, Iron Man, Magik, Moon Knight, Namor, Psylocke, The Punisher.
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
OUTPUT_PATH = os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_duelists_a.json')
INPUT_PATH = os.path.join(ROOT_DIR, 'scratch_duelists_a_stats.json')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

DUELISTS_A_TRANSLATIONS = {
    "Cuboid Spell Field": {
        "ko": "직육면체형 장판",
        "ja": "直方体フィールド"
    },
    "Length: 22m, Width: 20m, Height: 7m": {
        "ko": "길이: 22m, 너비: 20m, 높이: 7m",
        "ja": "長さ: 22m、幅: 20m、高さ: 7m"
    },
    "150°": {
        "ko": "150°",
        "ja": "150°"
    },
    "Gain 50% Damage Reduction during Bast's Descent startup animation": {
        "ko": "Bast's Descent 시전 선딜레이 중 50% 피해 감소 획득",
        "ja": "Bast's Descent発動前の予備動作中、被ダメージ50%軽減を獲得"
    },
    "Health drops below 100": {
        "ko": "체력 100 미만으로 저하 시",
        "ja": "HPが100未満に低下時"
    },
    "Cause 26 damage per single slash; double strike cause 13 damage per hit": {
        "ko": "단타 베기 시 26 데미지 | 2연타 베기 시 타격당 13 데미지",
        "ja": "単発斬撃時26ダメージ | 2連撃時1ヒットあたり13ダメージ"
    },
    "Projectile that fires in a straight trajectory, which breaks into shrapnel after reaching a certain distance": {
        "ko": "직선 궤도로 발사된 후 일정 거리에 도달하면 파편으로 분열하는 투사체",
        "ja": "直線軌道で発射後、一定距離で破片に拡散する弾"
    },
    "1s after activation": {
        "ko": "발동 후 1초",
        "ja": "発動後1秒"
    },
    "Every 200 damage resisted grants 1 charge for Daywalker Dash": {
        "ko": "200의 피해를 방어할 때마다 Daywalker Dash 1회 충전 획득",
        "ja": "200ダメージを防ぐごとにDaywalker Dashチャージを1獲得"
    },
    "10m, maximum distance 24m after fully charged.": {
        "ko": "기본 10m (완전 충전 시 최대 거리 24m)",
        "ja": "基本10m（最大チャージ時最大距離24m）"
    },
    "Length: Maximum dash distance; Width: 6m; Height: 4.5m": {
        "ko": "길이: 최대 돌진 거리, 너비: 6m, 높이: 4.5m",
        "ja": "長さ: 最大突進距離、幅: 6m、高さ: 4.5m"
    },
    "Dash. Cause damage and special effects to the enemies hit": {
        "ko": "돌진하며 적중한 적에게 피해 및 특수 효과를 부여합니다.",
        "ja": "突進し、命中した敵にダメージと特殊効果を付与します。"
    },
    "apply 8% Healing Reduction per strike (32% total if all hit)": {
        "ko": "타격당 8% 치유 감소 부여 (전타 적중 시 총 32%)",
        "ja": "1撃ごとに8%の被回復減少を付与（全弾命中で計32%）"
    },
    "10 per hit, 4 hits in total": {
        "ko": "타격당 10 (총 4타)",
        "ja": "1ヒットあたり10（計4撃）"
    },
    "Landing all four hits of Whirlwind Slash grants 1 slash speed stack; Excess lifesteal grants Bonus Health( max 75; conversion rate 50%)": {
        "ko": "Whirlwind Slash 4타 모두 적중 시 공격 속도 1스택 획득. 초과 흡혈량은 Bonus Health로 전환 (최대 75, 전환율 50%)",
        "ja": "Whirlwind Slash全4撃命中時、攻撃速度スタックを1獲得。超過ライフスティールはBonus Healthへ変換（最大75、変換率50%）"
    },
    "70%, Affected by Healing Reduction": {
        "ko": "70% (치유 감소 효과 적용)",
        "ja": "70%（被回復減少効果の影響を受ける）"
    },
    "20% per bounce": {
        "ko": "바운스당 20%",
        "ja": "跳弾ごとに20%"
    },
    "Charged release, with delayed projectiles.": {
        "ko": "충전 발사 (시간차 투사체)",
        "ja": "チャージ発射（時間差弾）"
    },
    "3.5m to 5m radius spherical spell field": {
        "ko": "반경 3.5m~5m 구형 장판",
        "ja": "半径3.5m〜5mの球状フィールド"
    },
    "50~70": {
        "ko": "50~70",
        "ja": "50~70"
    },
    "0.8s/Round": {
        "ko": "발당 0.8초",
        "ja": "1発あたり0.8秒"
    },
    "Launch an electric projectile that travels in a straight line, which generates a spell area upon hitting the environment or an enemy": {
        "ko": "직선 궤도의 전격 투사체를 발사하여 지형이나 적에게 적중 시 장판을 생성합니다.",
        "ja": "直線軌道の電撃弾を発射し、地形または敵命中時にフィールドを生成します。"
    },
    "0.25s per strike": {
        "ko": "타격당 0.25초",
        "ja": "1撃あたり0.25秒"
    },
    "Generate a spell area after hitting the ground": {
        "ko": "지면 강타 시 장판 생성",
        "ja": "地面着弾時にフィールドを生成"
    },
    "Radius: 6m; Height: 3m cylindrical spell area": {
        "ko": "반경 6m, 높이 3m 원기둥형 장판",
        "ja": "半径6m・高さ3mの円柱状フィールド"
    },
    "Charged projectile with an arced trajectory": {
        "ko": "곡사 궤도로 날아가는 충전형 투사체",
        "ja": "弧状軌道を描くチャージ弾"
    },
    "130 - 195 m/s (Maximum speed is achieved after 0.9s of charging)": {
        "ko": "130 - 195 m/s (0.9초 충전 시 최대 속도 도달)",
        "ja": "130 - 195 m/s（0.9秒チャージ時に最大速度到達）"
    },
    "28 - 70 (Maximum damage is achieved after 0.9s of charging)": {
        "ko": "28 - 70 (0.9초 충전 시 최대 데미지 도달)",
        "ja": "28 - 70（0.9秒チャージ時に最大ダメージ到達）"
    },
    "11.3°": {
        "ko": "11.3°",
        "ja": "11.3°"
    },
    "While Hunter's Sight is active, bow draw speed is increased": {
        "ko": "Hunter's Sight 활성화 중 활 당김 속도가 증가합니다.",
        "ja": "Hunter's Sight発動中、弓の引き絞り速度が上昇します。"
    },
    "Length: 2m, Width: 6m, Height: 2m": {
        "ko": "길이: 2m, 너비: 6m, 높이: 2m",
        "ja": "長さ: 2m、幅: 6m、高さ: 2m"
    },
    "Charge up to 2.5s": {
        "ko": "최대 2.5초 충전",
        "ja": "最大2.5秒チャージ"
    },
    "15m-40m": {
        "ko": "15m-40m",
        "ja": "15m-40m"
    },
    "Straight-line projectile that is accompanied by a spell field": {
        "ko": "장판을 동반하는 직선 투사체",
        "ja": "フィールドを伴う直線弾"
    },
    "Length: 3m, Width: 3m, Height: 2.7m": {
        "ko": "길이: 3m, 너비: 3m, 높이: 2.7m",
        "ja": "長さ: 3m、幅: 3m、高さ: 2.7m"
    },
    "Length: 3m, Width: 5m, Height: 1.6m": {
        "ko": "길이: 3m, 너비: 5m, 높이: 1.6m",
        "ja": "長さ: 3m、幅: 5m、高さ: 1.6m"
    },
    "This ability cannot block explosions or effects created by projectiles on hit": {
        "ko": "이 스킬은 폭발 피해나 투사체 적중 시 발생하는 효과는 방어할 수 없습니다.",
        "ja": "このアビリティは爆発ダメージや投射物の着弾効果は防御できません。"
    },
    "0 - 90 (Maximum damage is achieved after 0.9s of aiming)": {
        "ko": "0 - 90 (0.9초 조준 시 최대 데미지 도달)",
        "ja": "0 - 90（0.9秒照準時に最大ダメージ到達）"
    },
    "Apply bonus damage to the base damage of Piercing Arrow": {
        "ko": "Piercing Arrow의 기본 데미지에 보너스 피해를 추가합니다.",
        "ja": "Piercing Arrowの基本ダメージに追加ボーナスダメージを適用します。"
    },
    "Projectiles stick to enemies on hit": {
        "ko": "적중 시 투사체가 적에게 부착됩니다.",
        "ja": "命中時に弾が敵へ突き刺さります。"
    },
    "32% falloff at 4m.": {
        "ko": "4m에서 32% 감쇠",
        "ja": "4mで32%減衰"
    },
    "Shapeshift into a Nastrond Crow and gain invincibility": {
        "ko": "나스트론드 까마귀로 변신하여 무적 상태를 획득합니다.",
        "ja": "ナストロンドのカラスに変身し無敵状態を獲得します。"
    },
    "Slow the enemies by 20% at the center, increasing to 40% at 2.5m from the center.": {
        "ko": "중심부 적 20% 감속, 중심 2.5m 지점에서 40%로 증가",
        "ja": "中心部で敵に20%鈍足、中心から2.5m地点で40%に増加"
    },
    "Burst Projectile": {
        "ko": "점사 투사체",
        "ja": "バースト弾"
    },
    "Instantly recover all Fire Cluster energy after not using Fire Cluster for 1s": {
        "ko": "Fire Cluster를 1초간 미사용 시 모든 에너지를 즉시 회복합니다.",
        "ja": "Fire Clusterを1秒間未使用時、全エネルギーを即座に回復します。"
    },
    "5.5 per round": {
        "ko": "발당 5.5",
        "ja": "1発あたり5.5"
    },
    "Falloff begins at 15m, decreasing to 60% at 20m.": {
        "ko": "15m부터 감쇠 시작, 20m에서 60%로 감소",
        "ja": "15mから減衰開始、20mで60%に低下"
    },
    "Straight-line projectile that generates a spherical spell field upon impact.": {
        "ko": "착탄 시 구형 장판을 생성하는 직선 투사체",
        "ja": "着弾時に球状フィールドを生成する直線弾"
    },
    "2.5s per strike": {
        "ko": "타격 간격 2.5초",
        "ja": "1撃あたり2.5秒"
    },
    "3m spherical radius; 8m high capsule-shaped spell field.": {
        "ko": "반경 3m 구형, 높이 8m 캡슐형 장판",
        "ja": "半径3m球状、高さ8mカプセル状フィールド"
    },
    "Generate 5 Bonus Health per 0.1s": {
        "ko": "0.1초마다 5 Bonus Health 생성",
        "ja": "0.1秒ごとに5 Bonus Health生成"
    },
    "Invisible Woman": {
        "ko": "Invisible Woman",
        "ja": "Invisible Woman"
    },
    "Successfully interacted: 30s; fail to interact: 3s": {
        "ko": "상호작용 성공 시: 30초 | 실패 시: 3초",
        "ja": "インタラクト成功時: 30秒 | 失敗時: 3秒"
    },
    "Launch-up spell field causes 30 damage; mobility abilities disabling spell field causes 15 damage per second": {
        "ko": "띄우기 장판: 30 데미지 | 이동기 차단 장판: 초당 15 데미지",
        "ja": "打ち上げフィールド: 30ダメージ | 移動制限フィールド: 秒間15ダメージ"
    },
    "A cylindrical spell field with a radius of 8m and a height of 1m": {
        "ko": "반경 8m, 높이 1m 원기둥형 장판",
        "ja": "半径8m・高さ1mの円柱状フィールド"
    },
    "A cylindrical spell field with a radius of 8m and a height of 8m": {
        "ko": "반경 8m, 높이 8m 원기둥형 장판",
        "ja": "半径8m・高さ8mの円柱状フィールド"
    },
    "The first four strikes each deal 35 damage, while the fifth strike deals 55 damage": {
        "ko": "1~4타 각 35 데미지, 5타 55 데미지",
        "ja": "1~4撃目各35ダメージ、5撃目55ダメージ"
    },
    "The first four strikes have an interval of 0.45s between them, while the fifth strike has a 0.67s interval from the fourth strike": {
        "ko": "1~4타 타격 간격 0.45초, 5타 간격 0.67초",
        "ja": "1~4撃目の間隔0.45秒、5撃目の間隔0.67秒"
    },
    "8 base damage + 3.1% of the enemy's Max Health per strike": {
        "ko": "타격당 기본 8 데미지 + 적 최대 체력의 3.1%",
        "ja": "1撃あたり基本8ダメージ + 敵最大HPの3.1%"
    },
    "35 - 70 (Maximum damage is achieved when the target is at 50% Health)": {
        "ko": "35 - 70 (대상 체력 50% 이하 시 최대 데미지)",
        "ja": "35 - 70（対象のHPが50%時最大ダメージ到達）"
    },
    "Excess healing converts to Bonus Health.": {
        "ko": "초과 치유량은 Bonus Health로 전환됩니다.",
        "ja": "超過回復分はBonus Healthに変換されます。"
    },
    "After firing the one-handed repulsor twice in a row, the next attack will fire two repulsors at once": {
        "ko": "한손 리펄서를 2회 연속 발사한 후, 다음 공격은 양손 리펄서를 동시 발사합니다.",
        "ja": "片手リパルサーを2回連続発射後、次の攻撃で両手リパルサーを一斉発射します。"
    },
    "Repulsor Blast and Unibeam share the same ammo count": {
        "ko": "Repulsor Blast와 Unibeam은 동일한 탄약 수를 공유합니다.",
        "ja": "Repulsor BlastとUnibeamは共通の残弾数を共有します。"
    },
    "40% falloff at 5m": {
        "ko": "5m에서 40% 감쇠",
        "ja": "5mで40%減衰"
    },
    "Length: 15m, Width: 5m, Height: 5m": {
        "ko": "길이: 15m, 너비: 5m, 높이: 5m",
        "ja": "長さ: 15m、幅: 5m、高さ: 5m"
    },
    "5% falloff at 10m": {
        "ko": "10m에서 5% 감쇠",
        "ja": "10mで5%減衰"
    },
    "As the projectile travels, it creates a dispersive spell field that deals Damage Over Time to nearby enemies": {
        "ko": "투사체가 날아가는 동안 확산 장판을 형성하여 주변 적들에게 지속 피해를 줍니다.",
        "ja": "弾の飛翔中、周囲の敵に持続ダメージを与える拡散フィールドを展開します。"
    },
    "Each KO while Armor Overdrive is active extends its duration by 2s": {
        "ko": "Armor Overdrive 활성화 중 처치(KO)를 달성할 때마다 지속 시간이 2초 연장됩니다.",
        "ja": "Armor Overdrive発動中のキル（KO）ごとに効果時間が2秒延長されます。"
    },
    "Scatter-type projectile that generates a spell area upon impact": {
        "ko": "착탄 시 장판을 생성하는 산탄형 투사체",
        "ja": "着弾時にフィールドを生成する拡散弾"
    },
    "Launch missiles directly beneath Iron Man": {
        "ko": "아이언맨 바로 아래 지면으로 미사일 발사",
        "ja": "アイアンマンの直下へミサイルを発射"
    },
    "Launch in the direction of Iron Man's crosshair": {
        "ko": "아이언맨의 조준점 방향으로 발사",
        "ja": "アイアンマンの照準方向へ発射"
    },
    "Falloff begins at 4.5m, decreasing to 50% at 6.5m": {
        "ko": "4.5m부터 감쇠 시작, 6.5m에서 50%로 감소",
        "ja": "4.5mから減衰開始、6.5mで50%に低下"
    },
    "A cylindrical spell field with a radius of 6m and a height of 5m": {
        "ko": "반경 6m, 높이 5m 원기둥형 장판",
        "ja": "半径6m・高さ5mの円柱状フィールド"
    },
    "Charged projectile that travels in a straight trajectory": {
        "ko": "직선 궤도로 날아가는 충전형 투사체",
        "ja": "直線軌道で飛翔するチャージ弾"
    },
    "45 - 81 (Maximum damage is achieved after 1.2s of charging)": {
        "ko": "45 - 81 (1.2초 충전 시 최대 데미지 도달)",
        "ja": "45 - 81（1.2秒チャージ時に最大ダメージ到達）"
    },
    "Projectile pierces enemies and reduces Stepping Discs cooldown by 1s per enemy pierced": {
        "ko": "투사체가 적을 관통하며 관통한 적 1명당 Stepping Discs 쿨다운이 1초 감소합니다.",
        "ja": "弾が敵を貫通し、貫通した敵1体につきStepping Discsのクールダウンが1秒短縮されます。"
    },
    "20 damage per hit": {
        "ko": "타격당 20 데미지",
        "ja": "1ヒットあたり20ダメージ"
    },
    "Length: 6.5m, Width: 3m, Height: 3m": {
        "ko": "길이: 6.5m, 너비: 3m, 높이: 3m",
        "ja": "長さ: 6.5m、幅: 3m、高さ: 3m"
    },
    "When in the Darkchild state, all of Magik's abilities are enhanced": {
        "ko": "Darkchild 상태에서는 매직의 모든 스킬이 강화됩니다.",
        "ja": "Darkchild状態中、マジックの全アビリティが強化されます。"
    },
    "Magik can perform a combo ability within a certain time frame, choosing between Eldritch Whirl or Demon's Rage": {
        "ko": "매직은 일정 시간 내에 연계기를 발동할 수 있으며, Eldritch Whirl 또는 Demon's Rage 중 선택할 수 있습니다.",
        "ja": "マジックは一定時間内に連携コンボを発動でき、Eldritch WhirlまたはDemon's Rageから選択可能です。"
    },
    "Begins at 0%, growing to 40% at 5m": {
        "ko": "0%에서 시작, 5m에서 40%로 증가",
        "ja": "0%から開始、5mで40%に増加"
    },
    "Deals 3 hits at intervals of 0.15s, with each hit dealing 35 damage": {
        "ko": "0.15초 간격으로 3연타 (타격당 35 데미지)",
        "ja": "0.15秒間隔で3連撃（1撃あたり35ダメージ）"
    },
    "Deals 3 hits at intervals of 0.25s, each dealing 45 damage": {
        "ko": "0.25초 간격으로 3연타 (타격당 45 데미지)",
        "ja": "0.25秒間隔で3連撃（1撃あたり45ダメージ）"
    },
    "A cylindrical spell field with a radius of 12m and a height of 5m": {
        "ko": "반경 12m, 높이 5m 원기둥형 장판",
        "ja": "半径12m・高さ5mの円柱状フィールド"
    },
    "90 - 180 (Maximum damage is achieved after 1.8s of charging)": {
        "ko": "90 - 180 (1.8초 충전 시 최대 데미지 도달)",
        "ja": "90 - 180（1.8秒チャージ時に最大ダメージ到達）"
    },
    "25 damage per hit": {
        "ko": "타격당 25 데미지",
        "ja": "1ヒットあたり25ダメージ"
    },
    "Length: 6m, Width: 4m, Height: 4m": {
        "ko": "길이: 6m, 너비: 4m, 높이: 4m",
        "ja": "長さ: 6m、幅: 4m、高さ: 4m"
    },
    "Triple shot that fires in a straight trajectory": {
        "ko": "직선 궤도 3연사 투사체",
        "ja": "直線軌道3点バースト弾"
    },
    "The firing interval between shots is 0.05s, with an interval of 0.57s between each round of shooting": {
        "ko": "연발 간격 0.05초, 라운드 간 간격 0.57초",
        "ja": "連射間隔0.05秒、発射ラウンド間隔0.57秒"
    },
    "25, up to a max of 76 Bonus Health": {
        "ko": "25 (최대 76 Bonus Health)",
        "ja": "25（最大76 Bonus Health）"
    },
    "Delayed Spherical Spell Field": {
        "ko": "시간차 폭발 구형 장판",
        "ja": "時間差爆発球状フィールド"
    },
    "150 damage per hit": {
        "ko": "타격당 150 데미지",
        "ja": "1ヒットあたり150ダメージ"
    },
    "Start at 1.5m, 70% falloff at 5m": {
        "ko": "1.5m부터 감쇠 시작, 5m에서 70%로 감소",
        "ja": "1.5mから減衰開始、5mで70%に低下"
    },
    "50% falloff at 3m": {
        "ko": "3m에서 50% 감쇠",
        "ja": "3mで50%減衰"
    },
    "A cylindrical spell field with an inner circle radius of 3.5m, an outer circle radius of 9m, and a height of 3m": {
        "ko": "내경 반경 3.5m, 외경 반경 9m, 높이 3m 도넛형 원기둥 장판",
        "ja": "内径半径3.5m・外径半径9m・高さ3mの円柱状フィールド"
    },
    "Inner Circle Damage: 500; Outer Circle Damage: 180": {
        "ko": "내경 데미지: 500 | 외경 데미지: 180",
        "ja": "内径ダメージ: 500 | 外径ダメージ: 180"
    },
    "Arced Trajectory (Summon Monstro Spawn), Direct Hit (Monstro Spawn)": {
        "ko": "곡사 궤도 (Monstro Spawn 소환) | 직격 (Monstro Spawn)",
        "ja": "曲射軌道（Monstro Spawn召喚） | 直撃（Monstro Spawn）"
    },
    "A cylindrical spell field with a radius of 3m and a height of 13m": {
        "ko": "반경 3m, 높이 13m 원기둥형 장판",
        "ja": "半径3m・高さ13mの円柱状フィールド"
    },
    "A cylindrical spell field with a radius of 6m and a height of 11m": {
        "ko": "반경 6m, 높이 11m 원기둥형 장판",
        "ja": "半径6m・高さ11mの円柱状フィールド"
    },
    "Undead Monstro is untargetable": {
        "ko": "Undead Monstro는 타겟팅 불가 상태입니다.",
        "ja": "Undead Monstroはターゲット不可状態です。"
    },
    "Double projectile with spread": {
        "ko": "확산형 2연발 투사체",
        "ja": "拡散型2連射弾"
    },
    "The firing interval between shots is 0.2s, with an interval of 0.6s between each round of shooting": {
        "ko": "탄환 간격 0.2초, 발사 주기 간격 0.6초",
        "ja": "連射間隔0.2秒、発射ラウンド間隔0.6秒"
    },
    "10 bonus health per round": {
        "ko": "발당 10 Bonus Health",
        "ja": "1発あたり10 Bonus Health"
    },
    "When the projectile is recalled, it will move 20s toward the crosshair before returning to Psylocke": {
        "ko": "수리검 회수 시 조준점 방향으로 20s 이동 후 사일록에게 돌아옵니다.",
        "ja": "手裏剣回収時、照準方向へ20s移動した後にサイロックの手元へ戻ります。"
    },
    "0.86°": {
        "ko": "0.86°",
        "ja": "0.86°"
    },
    "Deal 50 damage. Affect a single target at most once.": {
        "ko": "50 데미지 부여 (단일 대상에게 최대 1회만 적용)",
        "ja": "50ダメージ付与（単一ターゲットに最大1回のみ適用）"
    },
    "Heal 60 health upon unleashing and 30 health when retrieved.": {
        "ko": "방출 시 60 치유, 회수 시 30 치유",
        "ja": "射出時60回復、回収時30回復"
    },
    "Grant 2s of self healing for each target hit": {
        "ko": "적중 대상마다 2초간 지속 자가 치유 부여",
        "ja": "命中した対象ごとに2秒間の自己持続回復を付与"
    },
    "160 damage per hit": {
        "ko": "타격당 160 데미지",
        "ja": "1ヒットあたり160ダメージ"
    },
    "Psylocke will slash a random enemy, giving priority to the one who has been hit the least": {
        "ko": "사일록이 무작위 적을 베며 피격 횟수가 가장 적은 적을 우선 타격합니다.",
        "ja": "サイロックはランダムな敵を斬撃し、被弾回数が最も少ない敵を優先して攻撃します。"
    },
    "Casting this ability will automatically recall the Wing Shurikens. The shurikens will first travel to Psylocke's starting position before returning to her": {
        "ko": "스킬 시전 시 Wing Shurikens가 자동 회수됩니다. 수리검은 사일록의 최초 시전 위치를 경유한 뒤 손으로 복귀합니다.",
        "ja": "発動時にWing Shurikensを自動回収。手裏剣はサイロックの初期位置を経由した後に手元へ戻ります。"
    },
    "When attacked while in stealth, Psylocke will remain in stealth but will briefly become visible for a short duration": {
        "ko": "은신 중 피격 시 은신은 유지되지만 짧은 시간 동안 실루엣이 드러납니다.",
        "ja": "ステルス中に被弾時、ステルスは維持されますが短時間姿が可視化されます。"
    },
    "Up to a 0.075m radius.": {
        "ko": "최대 반경 0.075m",
        "ja": "最大半径0.075m"
    },
    "Create a temporary smokescreen that obstructs vision": {
        "ko": "시야를 차단하는 임시 연막을 생성합니다.",
        "ja": "視界を遮断する一時的な煙幕を展開します。"
    },
    "Rapid-fire projectiles that hit instantly and have a tracking trajectory": {
        "ko": "즉발 적중 및 유도 궤적을 가진 연사 투사체",
        "ja": "即時着弾かつ誘導軌道を持つ高速連射弾"
    },
    "Start with a spread radius of 0.6m, which reduces to 0.3m after 50 shots, and further decreases to 0.15m after 100 shots": {
        "ko": "초기 탄퍼짐 반경 0.6m, 50발 사격 후 0.3m로 축소, 100발 사격 후 0.15m로 축소",
        "ja": "初期拡散半径0.6m、50発射撃後0.3mへ縮小、100発射撃後0.15mへさらに縮小"
    },
    "20° - 160°": {
        "ko": "20° - 160°",
        "ja": "20° - 160°"
    },
    "5m - 35m": {
        "ko": "5m - 35m",
        "ja": "5m - 35m"
    },
    "Rapid-fire projectiles that create a spell field upon impact": {
        "ko": "착탄 시 장판을 생성하는 연사 투사체",
        "ja": "着弾時にフィールドを生成する連射弾"
    },
    "Start with a spread radius of 0.2m, which reduces to 0.1m after 10 shots, and further decreases to 0.05m after 20 shots": {
        "ko": "초기 탄퍼짐 반경 0.2m, 10발 사격 후 0.1m로 축소, 20발 사격 후 0.05m로 축소",
        "ja": "初期拡散半径0.2m、10発射撃後0.1mへ縮小、20発射撃後0.05mへさらに縮小"
    },
    "Warrior's Gaze": {
        "ko": "Warrior's Gaze",
        "ja": "Warrior's Gaze"
    },
    "Retain vision of enemies that disappear from view for a short duration": {
        "ko": "시야에서 사라진 적의 실루엣을 잠시 동안 계속 포착합니다.",
        "ja": "視界から外れた敵の姿を短時間透視・追跡し続けます。"
    },
    "+25 Max Health, +5% Damage Boost": {
        "ko": "최대 체력 +25, 피해량 +5% 증가",
        "ja": "最大体力+25、与ダメージ+5%増加"
    }
}

def main():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        src = json.load(f)

    print(f"Total keys in {INPUT_PATH}: {len(src)}")
    print(f"Total translations mapped: {len(DUELISTS_A_TRANSLATIONS)}")

    missing = [k for k in src if k not in DUELISTS_A_TRANSLATIONS]
    if missing:
        print(f"❌ Missing {len(missing)} keys:")
        for m in missing:
            print("  ", repr(m))
        raise ValueError("Missing keys in DUELISTS_A_TRANSLATIONS")

    # Purity check
    for k, v in DUELISTS_A_TRANSLATIONS.items():
        ko = v.get('ko', '')
        ja = v.get('ja', '')
        if JAPANESE_REGEX.search(ko):
            raise ValueError(f"Kana in KO: {k} -> {ko}")
        if KOREAN_REGEX.search(ja):
            raise ValueError(f"Hangul in JA: {k} -> {ja}")

    print("✅ All 116 keys covered with 100% purity!")

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(DUELISTS_A_TRANSLATIONS, f, ensure_ascii=False, indent=2)

    print(f"Successfully wrote {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
