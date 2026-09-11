# -*- coding: utf-8 -*-
"""
Generator for Duelists B stat values translations (93 items).
Deadpool (Duelist), Daredevil, Elsa Bloodstone, Scarlet Witch, Spider-Man, Squirrel Girl, Star-Lord, Storm, Winter Soldier, Wolverine.
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
OUTPUT_PATH = os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_duelists_b.json')
INPUT_PATH = os.path.join(ROOT_DIR, 'scratch_duelists_b_stats.json')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

DUELISTS_B_TRANSLATIONS = {
    # Deadpool (Duelist)
    "Refresh the cooldown if it hits an enemy. Deadpool bounces as the ability hits an enemy.": {
        "ko": "적에게 적중 시 쿨다운 초기화. 적에게 적중하면 Deadpool이 튕겨 오릅니다.",
        "ja": "敵に命中時クールダウンをリセット。敵命中時にDeadpoolが跳ね上がります。"
    },
    "10% for each stack. Up to 4 stacks.": {
        "ko": "스택당 10%. 최대 4스택.",
        "ja": "スタックごとに10%。最大4スタック。"
    },
    "25, up to 50": {
        "ko": "25, 최대 50",
        "ja": "25、最大50"
    },
    "Refresh the cooldown if it hits an enemy.": {
        "ko": "적에게 적중 시 쿨다운 초기화.",
        "ja": "敵に命中時クールダウンをリセット。"
    },

    # Daredevil
    "Block frontal damage and reflect projectiles, becoming immune to all incoming harm during this stance. Gain 60 Fury when successfully blocking an attack.": {
        "ko": "전방 피해를 차단하고 투사체를 반사하며 자세 지속 중 받는 모든 피해에 면역이 됩니다. 공격 차단 성공 시 Fury 60 획득.",
        "ja": "前方からのダメージを遮断し弾を反射、この構え中はあらゆる被ダメージを無効化。ガード成功時にFuryを60獲得。"
    },
    "Devil's Throw slows enemies on hit": {
        "ko": "Devil's Throw 적중 시 적 둔화",
        "ja": "Devil's Throw命中時に敵にスロウを付与"
    },
    "Falloff begins at 5s and decreases by 30/s": {
        "ko": "5초 후 감쇠 시작, 초당 30씩 감소",
        "ja": "5秒後に減衰開始、毎秒30減少"
    },
    "Box shaped spell field. Length: 8m; Width: 4m; Height: 4m": {
        "ko": "상자형 장판. 길이: 8m, 너비: 4m, 높이: 4m",
        "ja": "ボックス型フィールド。長さ: 8m、幅: 4m、高さ: 4m"
    },
    "2m spherical radius spell field at the end": {
        "ko": "끝 지점에 반경 2m 구형 장판 생성",
        "ja": "終端に半径2mの球状フィールドを生成"
    },
    "40. Cause 65 damage when the target caught in the high damage range": {
        "ko": "40. 대상이 고데미지 범위에 걸릴 시 65 데미지",
        "ja": "40。高ダメージ範囲に捉えた対象には65ダメージ"
    },
    "4. Up to 2 ricochets if there are no targets": {
        "ko": "4회. 대상이 없을 경우 최대 2회 도탄",
        "ja": "4回。対象がいない場合は最大2回跳弾"
    },
    "50/s. Cause 85 damage per second when reaching the max damage": {
        "ko": "초당 50. 최대 데미지 도달 시 초당 85 데미지",
        "ja": "毎秒50。最大ダメージ到達時は毎秒85ダメージ"
    },
    "Visual range 35m, decreasing to 10m when the Blind effect reaches its maximum": {
        "ko": "시야 거리 35m, Blind 효과 최대치 도달 시 10m까지 감소",
        "ja": "視界範囲35m、Blind効果が最大に達すると10mまで縮小"
    },
    "Enable Righteous Cross within 5 seconds after using this ability. Gain 30 Fury": {
        "ko": "스킬 사용 후 5초 이내에 Righteous Cross 사용 가능. Fury 30 획득",
        "ja": "アビリティ使用後5秒以内にRighteous Crossが使用可能。Furyを30獲得"
    },
    "2.1m/s. Falloff begins at 10m away from the target, decreasing to 0.9m/s at 40m from the target": {
        "ko": "2.1m/s. 대상으로부터 10m 거리에서 감쇠 시작, 대상과 40m 거리에서 0.9m/s로 감소",
        "ja": "2.1m/s。対象から10m地点で減衰開始、対象から40m地点で0.9m/sまで低下"
    },
    "If Daredevil defeats the target, refresh the cooldown. Gain 60 Fury after the dash": {
        "ko": "Daredevil이 대상을 처치하면 쿨다운 초기화. 돌진 후 Fury 60 획득",
        "ja": "Daredevilが対象を撃破するとクールダウンをリセット。ダッシュ後にFuryを60獲得"
    },

    # Elsa Bloodstone
    "4.5 per round": {
        "ko": "발당 4.5",
        "ja": "1発あたり4.5"
    },
    "The firing interval between shots is 0.12s, with an interval of 0.8s between each round of shooting": {
        "ko": "탄환 간 발사 간격 0.12초, 사격 세트 간 간격 0.8초",
        "ja": "弾間の発射間隔は0.12秒、各バースト射撃間の間隔は0.8秒"
    },
    "13+0.8% of enemy's maximum health": {
        "ko": "13 + 적 최대 체력의 0.8%",
        "ja": "13 + 敵の最大HPの0.8%"
    },
    "After hits an enemy, the projectile splits to several bullets to trace the enemies in range": {
        "ko": "적에게 적중 후 투사체가 여러 개의 탄환으로 분열하여 범위 내 적들을 추적",
        "ja": "敵に命中後、弾が複数の小弾に分裂し範囲内の敵を追跡"
    },
    "Projectile deals 40 extra damage to shields and enemies with bonus health": {
        "ko": "투사체가 쉴드 및 Bonus Health를 보유한 적에게 40의 추가 피해를 입힘",
        "ja": "弾はシールドおよびBonus Healthを持つ敵に40の追加ダメージを与える"
    },
    "Increase movement speed by 40% for 1s": {
        "ko": "1초 동안 이동 속도 40% 증가",
        "ja": "1秒間、移動速度が40%上昇"
    },
    "First hit: 60; second hit: 40": {
        "ko": "1타: 60 | 2타: 40",
        "ja": "1打目: 60 | 2打目: 40"
    },
    "20/s for 2s": {
        "ko": "2초 동안 초당 20",
        "ja": "2秒間、毎秒20"
    },
    "Reduce movement speed by 35% for 2s": {
        "ko": "2초 동안 이동 속도 35% 감소",
        "ja": "2秒間、移動速度が35%低下"
    },
    "Enemies seized by Glartrox cannot use their abilities until it stops moving": {
        "ko": "Glartrox에게 붙잡힌 적은 이동이 멈출 때까지 스킬을 사용할 수 없음",
        "ja": "Glartroxに捕らわれた敵は、停止するまでアビリティを使用不可"
    },
    "Elsa can recall Glartrox at any time": {
        "ko": "Elsa는 언제든지 Glartrox를 회수할 수 있습니다",
        "ja": "ElsaはいつでもGlartroxを呼び戻すことができます"
    },
    "When the Glartrox collides with terrain, returns, or reaches its maximum dash duration, it bites fiercely, dealing massive damage. If Glartrox is defeated, the bite will not be triggered": {
        "ko": "Glartrox가 지형에 충돌하거나, 복귀하거나, 최대 돌진 지속 시간에 도달하면 맹렬하게 물어뜯어 막대한 피해를 입힙니다. Glartrox가 파괴되면 물어뜯기가 발동하지 않습니다.",
        "ja": "Glartroxが地形に衝突、帰還、または最大突進時間に達すると激しく噛みつき、大ダメージを与えます。Glartroxが倒された場合、噛みつきは発動しません。"
    },
    "Maximum durations for dashing and returning are 3.5s each": {
        "ko": "돌진 및 복귀 최대 지속 시간 각 3.5초",
        "ja": "突進および帰還の最大持続時間はそれぞれ3.5秒"
    },
    "Glartrox cannot be critical hit. Drag 8 targets at most": {
        "ko": "Glartrox는 치명타를 입지 않음. 최대 8명의 대상을 끌고 감",
        "ja": "Glartroxはクリティカルを受けない。最大8体の対象を牽引"
    },
    "In 6s after unleashing Helix Advance, the next Double-Barrel Blaster deals 2.5 times damage": {
        "ko": "Helix Advance 사용 후 6초 이내 다음 Double-Barrel Blaster 데미지 2.5배 증가",
        "ja": "Helix Advance発動後6秒以内の次のDouble-Barrel Blasterのダメージが2.5倍に増加"
    },
    "Every unleash of Ruthless Pursuit and Helix Advance grants 30 and 40 Instinct respectively": {
        "ko": "Ruthless Pursuit 및 Helix Advance 시전 시마다 각각 Instinct 30 및 40 획득",
        "ja": "Ruthless PursuitおよびHelix Advanceを発動するごとにInstinctをそれぞれ30、40獲得"
    },
    "Launch up enemies hit, and activate the follow up in 5s": {
        "ko": "적중한 적을 공중으로 띄우고 5초 이내에 연계기 활성화",
        "ja": "命中した敵を打ち上げ、5秒以内に追撃アビリティが使用可能"
    },
    "Using either stage empowers your next Double-Barrel Blaster, dealing 1.8 times damage in 6s": {
        "ko": "어느 단계를 사용하든 다음 Double-Barrel Blaster가 강화되어 6초 이내 1.8배 데미지 적용",
        "ja": "いずれかの段階を使用すると次のDouble-Barrel Blasterが強化され、6秒以内1.8倍のダメージ"
    },
    "The trap becomes Invisible and Invulnerable after one-second deployment. Only one trap can exist at a time": {
        "ko": "함정은 설치 1초 후 투명 및 무적 상태가 됩니다. 동시에 1개의 함정만 존재 가능",
        "ja": "トラップは設置1秒後に不可視かつ無敵状態になります。同時に存在できるトラップは1つのみ"
    },
    "Cause 5 damage every 0.2s, last 1.2s": {
        "ko": "0.2초마다 5 데미지, 1.2초 지속",
        "ja": "0.2秒ごとに5ダメージ、1.2秒持続"
    },
    "Defeat the summon to end the Immobolized state early": {
        "ko": "소환물을 처치하면 이동 불가(Immobilized) 상태가 조기 해제됨",
        "ja": "召喚物を倒すことで移動不能（Immobilized）状態を早期解除可能"
    },
    "Elsa can dash to the enemy who triggers the trap": {
        "ko": "Elsa는 함정을 발동시킨 적에게 돌진할 수 있습니다",
        "ja": "Elsaはトラップを発動させた敵に向かってダッシュ可能"
    },
    "Instinct levels up when it reaches 100, up to 3 levels": {
        "ko": "Instinct가 100에 도달하면 레벨 업, 최대 3레벨",
        "ja": "Instinctが100に達するとレベルアップ、最大3レベル"
    },
    "For each Instinct level gained, reduce the cooldown of Helix Advance and Ruthless Pursuit by 2s": {
        "ko": "Instinct 레벨당 Helix Advance 및 Ruthless Pursuit의 쿨다운 2초 감소",
        "ja": "Instinctレベルが上がるごとにHelix AdvanceとRuthless Pursuitのクールダウンが2秒短縮"
    },

    # Scarlet Witch
    "A cylindrical spell field with a radius of 3m and a height of 5m": {
        "ko": "반경 3m, 높이 5m의 원기둥형 장판",
        "ja": "半径3m、高さ5mの円柱状フィールド"
    },
    "Attack the nearest enemy within range": {
        "ko": "범위 내 가장 가까운 적을 공격",
        "ja": "範囲内で最も近い敵を攻撃"
    },
    "Hitting with Chaos Control charges Chthonian Burst": {
        "ko": "Chaos Control 적중 시 Chthonian Burst 충전",
        "ja": "Chaos Control命中時にChthonian Burstをチャージ"
    },
    "Chaos Control can released during the Sorcery Surge": {
        "ko": "Sorcery Surge 지속 중 Chaos Control 시전 가능",
        "ja": "Sorcery Surge発動中もChaos Controlを使用可能"
    },
    "Begin to slow down by 1.5s, with the effect gradually increases to 50%": {
        "ko": "1.5초 후 감속 시작, 감속 효과는 최대 50%까지 점진적으로 증가",
        "ja": "1.5秒後に減速が開始し、効果は徐々に最大50%まで増加"
    },
    "During this period, Scarlet Witch enters a Free-flight state and gains 200 Bonus Health": {
        "ko": "지속 시간 동안 Scarlet Witch는 자유 비행 상태에 진입하고 200의 Bonus Health를 획득",
        "ja": "効果中、Scarlet Witchは自由飛行状態になり200のBonus Healthを獲得"
    },
    "12s per charge": {
        "ko": "충전당 12초",
        "ja": "チャージごとに12秒"
    },
    "During this period, Scarlet Witch enters the Projection state, can phase through enemies, and is immune to all damage": {
        "ko": "지속 시간 동안 Scarlet Witch는 투영(Projection) 상태에 진입하여 적을 통과할 수 있으며 모든 피해에 면역이 됩니다",
        "ja": "効果中、Scarlet Witchは投影（Projection）状態になり、敵をすり抜け可能で、あらゆるダメージに完全無敵となります"
    },

    # Spider-Man
    "The default attack is a punch, but after landing two consecutive punches, Spider-Man will unleash a kick on the third strike. Landing a punch reduces the cooldown of Web-Cluster by 1s, while landing a kick reduces it by 1.5s": {
        "ko": "기본 공격은 펀치이지만 연속 2타 적중 시 3타에서 킥을 날립니다. 펀치 적중 시 Web-Cluster 쿨다운 1초 감소, 킥 적중 시 1.5초 감소",
        "ja": "通常攻撃はパンチですが、2連撃命中後の3撃目にキックを放ちます。パンチ命中でWeb-Clusterのクールダウンが1秒短縮、キック命中で1.5秒短縮"
    },
    "0.82s per kick": {
        "ko": "킥당 0.82초",
        "ja": "キック1回あたり0.82秒"
    },
    "2s per shot": {
        "ko": "발당 2초",
        "ja": "発射1回あたり2秒"
    },
    "15 damage per hit": {
        "ko": "타격당 15 데미지",
        "ja": "1ヒットあたり15ダメージ"
    },
    "-3% per hit": {
        "ko": "타격당 -3%",
        "ja": "1ヒットあたり-3%"
    },
    "Striking an enemy applies a stacking Slow effect, and after landing consecutive hits, Spider-Man will immobilize the target": {
        "ko": "적 타격 시 중첩되는 둔화 효과를 부여하며, 연속 타격 성공 시 대상을 이동 불가(Immobilize) 상태로 만듭니다",
        "ja": "敵に命中するとスタックするスロウを付与し、連続ヒットで対象を移動不能（Immobilize）にします"
    },
    "6s per charge": {
        "ko": "충전당 6초",
        "ja": "チャージごとに6秒"
    },
    "Attack enemies marked with a Spider-Tracer, pulling Spider-Man towards them": {
        "ko": "Spider-Tracer가 표식된 적을 공격하여 Spider-Man이 대상 쪽으로 끌려갑니다",
        "ja": "Spider-Tracerが付与された敵を攻撃し、Spider-Manをその対象へ引き寄せます"
    },
    "Can only be cast again after landing": {
        "ko": "착지 후에만 재시전 가능",
        "ja": "着地後のみ再発動可能"
    },

    # Squirrel Girl
    "70% falloff at 3m": {
        "ko": "3m에서 70% 감쇠",
        "ja": "3m地点で70%減衰"
    },
    "1.49 acorns per second": {
        "ko": "초당 1.49개 도토리",
        "ja": "毎秒1.49個のどんぐり"
    },
    "20 - 60 m/s (Maximum speed is achieved after 0.7s of charging)": {
        "ko": "20 - 60 m/s (0.7초 충전 시 최대 속도 달성)",
        "ja": "20 - 60 m/s（0.7秒チャージで最大速度到達）"
    },
    "Length: 3m, Width: 5m, Height: 1.75m": {
        "ko": "길이: 3m, 너비: 5m, 높이: 1.75m",
        "ja": "長さ: 3m、幅: 5m、高さ: 1.75m"
    },
    "The squirrels will rush towards the nearest enemy after bouncing": {
        "ko": "다람쥐들은 바운드 후 가장 가까운 적을 향해 돌진합니다",
        "ja": "リスはバウンド後、最も近い敵に向かって突進します"
    },
    "Automatically track enemies within a horizontal angle of 60°": {
        "ko": "수평 각도 60° 이내의 적을 자동 추적",
        "ja": "水平角度60°以内の敵を自動追跡"
    },

    # Star-Lord
    "Rapid-fire shots with spread.": {
        "ko": "탄 퍼짐이 있는 고속 연사 사격.",
        "ja": "拡散を伴う高速連射射撃。"
    },
    "After 2 consecutive shots, the spread increases to 0.15m; after 10 consecutive shots, it increases to 0.35m": {
        "ko": "연속 2발 사격 후 탄 퍼짐이 0.15m로 증가, 연속 10발 사격 후 0.35m로 증가",
        "ja": "連続2発射撃後に拡散が0.15mに拡大、連続10発射撃後に0.35mに拡大"
    },
    "5s per charge": {
        "ko": "충전당 5초",
        "ja": "チャージごとに5秒"
    },
    "During this period, Star-Lord's Reload Speed increases significantly": {
        "ko": "지속 시간 동안 Star-Lord의 재장전 속도가 대폭 증가합니다",
        "ja": "効果中、Star-Lordのリロード速度が大幅に上昇します"
    },
    "7.5 damage per hit": {
        "ko": "타격당 7.5 데미지",
        "ja": "1ヒットあたり7.5ダメージ"
    },
    "Teleport Cooldown 30s; jump device deployment Cooldown 5s.": {
        "ko": "순간이동 쿨다운 30초, 도약 장치 배치 쿨다운 5초.",
        "ja": "テレポートクールダウン30秒、ジャンプ装置設置クールダウン5秒。"
    },

    # Storm
    "Wind Blade pierces through enemies": {
        "ko": "Wind Blade가 적들을 관통합니다",
        "ja": "Wind Bladeが敵を貫通します"
    },
    "Weather effects will be disabled during the Ultimate": {
        "ko": "궁극기 사용 중에는 기상 오라 효과가 비활성화됩니다",
        "ja": "アルティメット発動中は天候オーラ効果が無効化されます"
    },
    "Under this aura, Wind Blade hits reduce Bolt Rush cooldown by 0.5s": {
        "ko": "해당 오라 활성화 중 Wind Blade 적중 시 Bolt Rush 쿨다운 0.5초 감소",
        "ja": "このオーラ適用中、Wind Blade命中時にBolt Rushのクールダウンが0.5秒短縮"
    },
    "2s per strike": {
        "ko": "타격당 2초",
        "ja": "落雷1回あたり2秒"
    },

    # Winter Soldier
    "Cone-shaped spell field with a 5m radius and an apex angle of 75°": {
        "ko": "반경 5m, 중심각 75°의 원뿔형 장판",
        "ja": "半径5m、頂角75°の扇形（コーン型）フィールド"
    },
    "Projectile: Yes; Spell Field: No": {
        "ko": "투사체: 있음 | 장판: 없음",
        "ja": "弾（投射物）: あり | フィールド: なし"
    },
    "Enemies that take damage from the projectile will no longer take damage from the spell field": {
        "ko": "투사체로 피해를 입은 적은 장판으로부터 중복 피해를 받지 않습니다",
        "ja": "弾でダメージを受けた敵は、フィールドからのダメージを受けなくなります"
    },
    "0.5s - 4s": {
        "ko": "0.5초 - 4초",
        "ja": "0.5秒 - 4秒"
    },
    "Cone-shaped spell field with a 4.5m radius and an apex angle of 105°": {
        "ko": "반경 4.5m, 중심각 105°의 원뿔형 장판",
        "ja": "半径4.5m、頂角105°の扇形（コーン型）フィールド"
    },
    "20% Health": {
        "ko": "체력 20%",
        "ja": "HP 20%"
    },
    "Length: 4.5m, Width: 4.5m, Height: 2m": {
        "ko": "길이: 4.5m, 너비: 4.5m, 높이: 2m",
        "ja": "長さ: 4.5m、幅: 4.5m、高さ: 2m"
    },
    "Projectiles pierce through enemies": {
        "ko": "투사체가 적들을 관통합니다",
        "ja": "弾が敵を貫通します"
    },
    "Stellar Impact also triggers the Ceaseless Charge passive effect": {
        "ko": "Stellar Impact 또한 Ceaseless Charge 패시브 효과를 발동시킵니다",
        "ja": "Stellar ImpactもCeaseless Chargeパッシブ効果を発動させます"
    },
    "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact & Stellar Impact)": {
        "ko": "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact & Stellar Impact)",
        "ja": "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact & Stellar Impact)"
    },

    # Wolverine
    "15 damage per strike": {
        "ko": "타격당 15 데미지",
        "ja": "1撃あたり15ダメージ"
    },
    "Deal damage equal to 1.5% of the target's Max Health, with an interval of 0.23s between each strike": {
        "ko": "대상 최대 체력의 1.5%에 해당하는 피해를 입히며, 타격 간 간격은 0.23초",
        "ja": "対象の最大HPの1.5%に相当するダメージを与え、各攻撃の間隔は0.23秒"
    },
    "The first three strikes have an interval of 0.27s between them, and the interval between the third and fourth strike is 0.45s": {
        "ko": "1~3타 간 간격은 0.27초이며, 3타와 4타 사이 간격은 0.45초",
        "ja": "1〜3撃目の間隔は0.27秒、3撃目と4撃目の間隔は0.45秒"
    },
    "Deal damage equal to 10% of the target's Max Health, with an interval of 0.2s between each strike": {
        "ko": "대상 최대 체력의 10%에 해당하는 피해를 입히며, 타격 간 간격은 0.2초",
        "ja": "対象の最大HPの10%に相当するダメージを与え、各攻撃の間隔は0.2秒"
    },
    "6 damage per strike": {
        "ko": "타격당 6 데미지",
        "ja": "1撃あたり6ダメージ"
    },
    "Deal damage equal to 1% of the target's Max Health, with an interval of 0.08s between each strike": {
        "ko": "대상 최대 체력의 1%에 해당하는 피해를 입히며, 타격 간 간격은 0.08초",
        "ja": "対象の最大HPの1%に相当するダメージを与え、各攻撃の間隔は0.08秒"
    },
    "Deal damage equals to target's 1% Maximum Health per second": {
        "ko": "초당 대상 최대 체력의 1%에 해당하는 피해를 입힘",
        "ja": "毎秒、対象の最大HPの1%に相当するダメージを与える"
    },
    "Deal damage equal to 1% of the target's Max Health, with an interval of 0.16s between each strike": {
        "ko": "대상 최대 체력의 1%에 해당하는 피해를 입히며, 타격 간 간격은 0.16초",
        "ja": "対象の最大HPの1%に相当するダメージを与え、各攻撃の間隔は0.16秒"
    },
    "5 + 0.01% Max HP per Rage point": {
        "ko": "Rage 포인트당 5 + 최대 HP의 0.01%",
        "ja": "Rageポイントごとに5 + 最大HPの0.01%"
    },
    "150 - 300 (Damage increases with Rage)": {
        "ko": "150 - 300 (Rage에 비례하여 데미지 증가)",
        "ja": "150 - 300（Rageに応じてダメージ増加）"
    },

    # Additional batch variations
    "In 6s after unleashing Helix Advance, the next Double-Barrel Blaster becomes Monster-Piercer": {
        "ko": "Helix Advance 사용 후 6초 이내 다음 Double-Barrel Blaster가 Monster-Piercer로 전환",
        "ja": "Helix Advance発動後6秒以内の次のDouble-Barrel BlasterがMonster-Piercerに変化"
    },
    "Every unleash of Ruthless Pursuit and Helix Advance grants 30 bonus health. Max bonus health is 75": {
        "ko": "Ruthless Pursuit 및 Helix Advance 시전 시마다 30의 Bonus Health 획득. 최대 Bonus Health 75",
        "ja": "Ruthless PursuitおよびHelix Advanceを発動するごとに30のBonus Healthを獲得。最大Bonus Healthは75"
    },
    "Using either stage empowers your next Double-Barrel Blaster, transforming it into Monster-Piercer": {
        "ko": "어느 단계를 사용하든 다음 Double-Barrel Blaster가 강화되어 Monster-Piercer로 전환",
        "ja": "いずれかの段階を使用すると次のDouble-Barrel Blasterが強化され、Monster-Piercerに変化"
    },
    "The trap becomes Invisible and Invulnerable after one-second deployment": {
        "ko": "함정은 설치 1초 후 투명 및 무적 상태가 됨",
        "ja": "トラップは設置1秒後に不可視かつ無敵状態になる"
    },
    "For each Instinct level gained, reduce the cooldown of Helix Advance by 2s": {
        "ko": "Instinct 레벨당 Helix Advance의 쿨다운 2초 감소",
        "ja": "Instinctレベルが上がるごとにHelix Advanceのクールダウンが2秒短縮"
    },
    "A cylindrical spell field with a radius of 3m and a height of 20m": {
        "ko": "반경 3m, 높이 20m의 원기둥형 장판",
        "ja": "半径3m、高さ20mの円柱状フィールド"
    },
    "Begin to slow down by 1.5s, with the effect gradually increasing to -25% by 3.5s": {
        "ko": "1.5초 후 감속 시작, 3.5초까지 감속 효과가 -25%로 점진적 증가",
        "ja": "1.5秒後に減速が開始し、3.5秒までに効果が-25%まで徐々に増加"
    },
    "During this period, Scarlet Witch enters a Free-flight state, pulls in nearby enemies (within 15m radius) during cast charge. Max pull speed up to 3m/s": {
        "ko": "지속 시간 동안 Scarlet Witch는 자유 비행 상태에 진입하며, 시전 충전 중 주변 적(반경 15m 이내)을 끌어당김. 최대 견인 속도 3m/s",
        "ja": "効果中、Scarlet Witchは自由飛行状態になり、チャージ中に周囲の敵（半径15m以内）を牽引。最大牽引速度3m/s"
    },
    "During this period, Scarlet Witch enters the Projection state, can be healed by teammates": {
        "ko": "지속 시간 동안 Scarlet Witch는 투영(Projection) 상태에 진입하며, 아군의 치유를 받을 수 있음",
        "ja": "効果中、Scarlet Witchは投影（Projection）状態になり、味方からの回復を受けられる"
    },
    "The default attack is a punch, but after landing two consecutive punches, the next attack will be a flying kick": {
        "ko": "기본 공격은 펀치이지만 연속 2타 적중 시 다음 공격은 플라잉 킥이 됨",
        "ja": "通常攻撃はパンチですが、2連撃命中後の次の攻撃はフライングキックになります"
    },
    "Striking an enemy applies a stacking Slow effect, and after reaching a certain number of stacks, the enemy will be Stunned": {
        "ko": "적 타격 시 중첩되는 둔화 효과를 부여하며, 일정 스택 도달 시 대상을 기절(Stun)시킴",
        "ja": "敵に命中するとスタックするスロウを付与し、一定スタック到達で敵をスタン状態にする"
    },
    "Attack enemies marked with a Spider-Tracer, pulling Spider-Man towards them and performing a flying kick": {
        "ko": "Spider-Tracer가 표식된 적을 공격하여 Spider-Man이 대상 쪽으로 끌려가며 플라잉 킥 시전",
        "ja": "Spider-Tracerが付与された敵を攻撃し、Spider-Manをその対象へ引き寄せてフライングキックを放つ"
    },
    "The squirrels will rush towards the nearest enemy after bouncing instead of bouncing randomly": {
        "ko": "다람쥐들이 무작위로 튕기는 대신 바운드 후 가장 가까운 적을 향해 돌진",
        "ja": "リスはランダムに跳ねる代わりに、バウンド後最も近い敵に向かって突進"
    },
    "Automatically track enemies within a horizontal angle of 60°, a vertical angle of 60°, and a maximum distance of 60m": {
        "ko": "수평 각도 60°, 수직 각도 60°, 최대 거리 60m 이내의 적을 자동 추적",
        "ja": "水平角度60°、垂直角度60°、最大距離60m以内の敵を自動追跡"
    },
    "After 2 consecutive shots, the spread increases to 0.15m; after 5 consecutive shots, the spread expands to 0.24m": {
        "ko": "연속 2발 사격 후 탄 퍼짐이 0.15m로 증가, 연속 5발 사격 후 0.24m로 확대",
        "ja": "連続2発射撃後に拡散が0.15mに拡大、連続5発射撃後に0.24mに拡大"
    },
    "Under this aura, Wind Blade hits reduce Bolt Rush cooldown by 0.5s (only once per cast, even if hitting multiple enemies). Increase Bolt Rush spell field range radius from 1m to 1.5m": {
        "ko": "해당 오라 활성화 중 Wind Blade 적중 시 Bolt Rush 쿨다운 0.5초 감소 (여러 명 적중해도 시전당 1회만 적용). Bolt Rush 장판 범위 반경이 1m에서 1.5m로 증가",
        "ja": "このオーラ適用中、Wind Blade命中時にBolt Rushのクールダウンが0.5秒短縮（複数命中時も発動1回につき1回のみ）。Bolt Rushのフィールド範囲半径が1mから1.5mに拡大"
    },
    "Cone-shaped spell field with a 5m radius and an apex angle of 90°": {
        "ko": "반경 5m, 중심각 90°의 원뿔형 장판",
        "ja": "半径5m、頂角90°の扇形（コーン型）フィールド"
    },
    "Enemies that take damage from the projectile will no longer receive damage from the spell field": {
        "ko": "투사체로 피해를 입은 적은 장판으로부터 피해를 받지 않음",
        "ja": "弾でダメージを受けた敵は、フィールドからのダメージを受けなくなります"
    },
    "Cone-shaped spell field with a 4.5m radius and an apex angle of 80°": {
        "ko": "반경 4.5m, 중심각 80°의 원뿔형 장판",
        "ja": "半径4.5m、頂角80°の扇形（コーン型）フィールド"
    },
    "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact)": {
        "ko": "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact)",
        "ja": "40 (Bionic Hook & Tainted Voltage), 50 (Trooper's Fist, Kraken Impact)"
    },
    "Deal damage equal to 1.5% of the target's Max Health, with an extra 0.057% damage for each point of Rage": {
        "ko": "대상 최대 체력의 1.5%에 해당하는 피해를 입히며, Rage 포인트당 0.057% 추가 피해",
        "ja": "対象の最大HPの1.5%に相当するダメージを与え、Rageポイントごとに0.057%の追加ダメージ"
    },
    "The first three strikes have an interval of 0.27s between them, while the fourth strike has a 0.84s interval from the third strike": {
        "ko": "1~3타 간 간격은 0.27초이며, 3타와 4타 사이 간격은 0.84초",
        "ja": "1〜3撃目の間隔は0.27秒、3撃目と4撃目の間隔は0.84秒"
    },
    "Deal damage equal to 10% of the target's Max Health, with an extra 0.3% damage for each point of Rage": {
        "ko": "대상 최대 체력의 10%에 해당하는 피해를 입히며, Rage 포인트당 0.3% 추가 피해",
        "ja": "対象の最大HPの10%に相当するダメージを与え、Rageポイントごとに0.3%の追加ダメージ"
    },
    "Deal damage equal to 1% of the target's Max Health, with an extra 0.035% damage for each point of Rage": {
        "ko": "대상 최대 체력의 1%에 해당하는 피해를 입히며, Rage 포인트당 0.035% 추가 피해",
        "ja": "対象の最大HPの1%に相当するダメージを与え、Rageポイントごとに0.035%の追加ダメージ"
    },
    "Deal damage equal to 1% of the target's Max Health, with an extra 0.035% damage for each point of Rage.": {
        "ko": "대상 최대 체력의 1%에 해당하는 피해를 입히며, Rage 포인트당 0.035% 추가 피해.",
        "ja": "対象の最大HPの1%に相当するダメージを与え、Rageポイントごとに0.035%の追加ダメージ。"
    }
}

def validate_and_generate():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    missing = []
    purity_errors = []
    results = {}

    for en_key in source_data.keys():
        if en_key not in DUELISTS_B_TRANSLATIONS:
            missing.append(en_key)
            continue
        
        tr = DUELISTS_B_TRANSLATIONS[en_key]
        ko = tr.get("ko", "")
        ja = tr.get("ja", "")

        # Purity check: KO must NOT have Kana
        if JAPANESE_REGEX.search(ko):
            purity_errors.append(f"Japanese Kana found in KO: '{ko}' for key '{en_key}'")
        
        # Purity check: JA must NOT have Hangul
        if KOREAN_REGEX.search(ja):
            purity_errors.append(f"Korean Hangul found in JA: '{ja}' for key '{en_key}'")

        results[en_key] = {
            "ko": ko,
            "ja": ja
        }

    print(f"Total keys in batch: {len(source_data)}")
    print(f"Translated keys: {len(results)}")
    print(f"Missing keys: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  Missing: {m}")
    if purity_errors:
        print(f"Purity errors ({len(purity_errors)}):")
        for err in purity_errors:
            print(f"  {err}")
        raise ValueError("Purity check failed!")

    if len(results) == len(source_data):
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[OK] Successfully saved {len(results)} items to {OUTPUT_PATH}")

if __name__ == '__main__':
    validate_and_generate()
