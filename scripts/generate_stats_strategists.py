# -*- coding: utf-8 -*-
"""
Generator for Strategists stat values translations (209 items).
Adam Warlock, Black Cat, Cloak & Dagger, Cyclops, Deadpool (Strategist), Devil Dinosaur,
Emma Frost, Gambit, Gorr the God Butcher, Invisible Woman, Jeff the Land Shark,
Jubilation Lee, Loki, Luna Snow, Mantis, Mister Fantastic, Phoenix, Rocket Raccoon,
Rogue, The Hood, Ultron, White Fox.
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
OUTPUT_PATH = os.path.join(ROOT_DIR, 'scripts', 'batches', 'stats_strategists.json')
INPUT_PATH = os.path.join(ROOT_DIR, 'scratch_strategists_stats.json')

KOREAN_REGEX = re.compile(r'[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]')
JAPANESE_REGEX = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')

STRATEGISTS_TRANSLATIONS = {
    # ADAM WARLOCK
    "The firing interval for a single charged shot is 0.3s, while the interval for multiple shots is 0.07s": {
        "ko": "단발 충전 사격의 발사 간격은 0.3초, 다중 사격 간격은 0.07초",
        "ja": "単発チャージ射撃の間隔は0.3秒、連射時の間隔は0.07秒"
    },
    "Cosmic Cluster shares ammo with Quantum Magic, each hit reduces the cooldown of Avatar Life Stream by 0.6s.": {
        "ko": "Cosmic Cluster는 Quantum Magic과 탄약을 공유하며, 적중 시마다 Avatar Life Stream의 쿨다운이 0.6초 감소합니다.",
        "ja": "Cosmic ClusterはQuantum Magicと弾薬を共有し、命中ごとにAvatar Life Streamのクールダウンが0.6秒短縮されます。"
    },
    "Revive allies within range, centered on Adam. Continuously monitor for fallen allies within this range; if they enter the area, they can be revived at the casting location": {
        "ko": "Adam을 중심으로 범위 내 아군 부활. 해당 범위 내 쓰러진 아군을 지속 감지하여 영역에 들어오면 시전 위치에서 부활시킵니다",
        "ja": "Adamを中心に範囲内の味方を蘇生。範囲内の倒れた味方を継続監視し、エリア内に入れば発動地点で蘇生させます"
    },
    "Allies revived will be blessed with Bonus Health equal to 70% of their Maximum Health with a 5s duration. Bonus Health falloff begins at 5s, decreasing to 0 in 2s.": {
        "ko": "부활한 아군은 5초 동안 최대 체력의 70%에 해당하는 Bonus Health를 부여받습니다. Bonus Health는 5초 후 감쇠가 시작되어 2초에 걸쳐 0으로 감소합니다.",
        "ja": "蘇生された味方は5秒間、最大HPの70%に相当するBonus Healthを獲得。Bonus Healthは5秒後に減衰開始し、2秒かけて0になります。"
    },
    "Adam Warlock will share a portion of the damage sustained by linked allies. If Adam Warlock sustains damage that would KO him due to the link, then the link will be broken, and he will retain 1 Health. The link will also break once enough damage is sustained, if Adam Warlock or the linked ally leave the link's range, or after a certain length of time has passed": {
        "ko": "Adam Warlock은 연결된 아군이 받는 피해의 일부를 공유합니다. 연결로 인해 처치당할 수준의 피해를 받으면 링크가 끊어지고 체력 1로 생존합니다. 일정량 이상의 피해를 받거나 연결 범위를 벗어나거나 일정 시간이 지나도 링크가 해제됩니다",
        "ja": "Adam Warlockはリンクされた味方の被ダメージの一部を共有します。リンクにより戦闘不能になるダメージを受けた場合はリンクが切れ、HP 1で耐えます。一定以上のダメージを受けるか範囲外に出るか一定時間経過でもリンクが解除されます"
    },
    "Adam can hover and attack during the ability's duration": {
        "ko": "스킬 지속 시간 동안 Adam은 체공 및 공격이 가능합니다",
        "ja": "アビリティ発動中、Adamは滞空および攻撃が可能です"
    },
    "Bouncing target does not include Adam Warlock": {
        "ko": "바운드 대상에 Adam Warlock 본인은 포함되지 않음",
        "ja": "バウンド対象にAdam Warlock自身は含まれません"
    },
    "2 charges, with each charge taking 6s to recharge; when a critical hit lands on an enemy, reduce the cooldown time of Avatar Life Stream by 1s.": {
        "ko": "2회 충전, 충전당 6초 소요. 적에게 치명타 적중 시 Avatar Life Stream의 쿨다운 1초 감소.",
        "ja": "2チャージ、チャージごとに6秒。敵へのクリティカルヒット時、Avatar Life Streamのクールダウンが1秒短縮。"
    },

    # BLACK CAT
    "150° cone spell field with a radius of 7.5m and a height of 2.5m": {
        "ko": "반경 7.5m, 높이 2.5m, 각도 150°의 부채꼴 장판",
        "ja": "半径7.5m、高さ2.5m、角度150°の扇形フィールド"
    },
    "Falloff begins at 30°, drop to 30% of maximum damage at 75°": {
        "ko": "30°에서 감쇠 시작, 75°에서 최대 피해의 30%까지 감소",
        "ja": "30°で減衰開始、75°で最大ダメージの30%まで低下"
    },
    "Gain 0/50/200/500 Fortune randomly": {
        "ko": "Fortune 0/50/200/500을 무작위로 획득",
        "ja": "Fortuneをランダムに0/50/200/500獲得"
    },
    "60%, drop to 0 in 2s": {
        "ko": "60%, 2초에 걸쳐 0으로 감소",
        "ja": "60%、2秒かけて0まで低下"
    },
    "Remove any active control effects": {
        "ko": "모든 활성 제어(군중 제어) 효과 제거",
        "ja": "発動中のあらゆる行動制限（妨害効果）を解除"
    },
    "A cylindrical spell field with a radius of 5m and a height of 40m.": {
        "ko": "반경 5m, 높이 40m의 원기둥형 장판.",
        "ja": "半径5m、高さ40mの円柱状フィールド。"
    },
    "50, up to 50": {
        "ko": "50, 최대 50",
        "ja": "50、最大50"
    },
    "50, up to 100": {
        "ko": "50, 최대 100",
        "ja": "50、最大100"
    },
    "150, up to 150": {
        "ko": "150, 최대 150",
        "ja": "150、最大150"
    },
    "Lose 50% of Fortune when defeated, with a minimum deduction of 200": {
        "ko": "처치 시 Fortune의 50%를 잃으며, 최소 200 차감",
        "ja": "倒された時にFortuneの50%を失う（最低200減少）"
    },

    # Cloak & Dagger
    "Single-cast projectile that generates a spell area upon impact": {
        "ko": "충돌 시 장판을 생성하는 단발 투사체",
        "ja": "着弾時にフィールドを生成する単発弾"
    },
    "The projectile features an attraction effect, pulling in the closest target to the crosshair and creating a spell field upon impact. This spell field provides healing effects": {
        "ko": "투사체에 끌어당김 효과가 있어 조준선에 가장 가까운 대상을 끌어당기고 충돌 시 치유 효과를 제공하는 장판을 생성합니다",
        "ja": "弾には牽引効果があり、照準に最も近い対象を引き寄せ着弾時に回復効果を与えるフィールドを生成します"
    },
    "When a Spell Field is created, allies in range get a One-Time Healing of 60": {
        "ko": "장판 생성 시 범위 내 아군에게 60의 즉시 치유 제공",
        "ja": "フィールド生成時、範囲内の味方に60の即時回復を付与"
    },

    # Cyclops
    "50%, minimum 10%": {
        "ko": "50%, 최소 10%",
        "ja": "50%、最低10%"
    },
    "75+20%Maximum Health": {
        "ko": "75 + 최대 체력의 20%",
        "ja": "75 + 最大HPの20%"
    },
    "75+40%Maximum Health": {
        "ko": "75 + 최대 체력의 40%",
        "ja": "75 + 最大HPの40%"
    },
    "First field 2m, second field 8m": {
        "ko": "1차 장판 2m, 2차 장판 8m",
        "ja": "1次フィールド 2m、2次フィールド 8m"
    },
    "Minimum 0.35s, maximum 1s": {
        "ko": "최소 0.35초, 최대 1초",
        "ja": "最小0.35秒、最大1秒"
    },
    "Minimum 11m, maximum 22m": {
        "ko": "최소 11m, 최대 22m",
        "ja": "最小11m、最大22m"
    },
    "After the first refraction, each additional refraction increases damage by 10%, up to 20%": {
        "ko": "첫 굴절 후 추가 굴절마다 데미지 10% 증가, 최대 20%",
        "ja": "初回転折後、追加の屈折ごとにダメージが10%増加（最大20%）"
    },
    "2 charges, with each charge taking 15s to recharge. Base Cooldown 2s": {
        "ko": "2회 충전, 충전당 15초 소요. 기본 쿨다운 2초",
        "ja": "2チャージ、チャージごとに15秒。基本クールダウン2秒"
    },

    # DEADPOOL (STRATEGIST)
    "45 per round": {
        "ko": "발당 45",
        "ja": "1発あたり45"
    },
    "80 per ability missed": {
        "ko": "빗나간 스킬당 80",
        "ja": "外れたアビリティごとに80"
    },
    "90 per ability missed": {
        "ko": "빗나간 스킬당 90",
        "ja": "外れたアビリティごとに90"
    },
    "80/s upon activation; 120/s after completing the challenge": {
        "ko": "발동 시 초당 80 | 챌린지 완료 후 초당 120",
        "ja": "発動時 毎秒80 | チャレンジ達成後 毎秒120"
    },
    "Refresh the cooldown if it hits an enemy or an ally. Transform the next katana base attack to a Stab.": {
        "ko": "적 또는 아군에게 적중 시 쿨다운 초기화. 다음 카타나 기본 공격을 찌르기(Stab)로 전환.",
        "ja": "敵または味方に命中時クールダウンをリセット。次のカタナ通常攻撃を突き（Stab）に変化。"
    },
    "+5% Healing Bonus": {
        "ko": "+5% 치유 보너스",
        "ja": "+5% 回復ボーナス"
    },

    # DEVIL DINOSAUR
    "1st and 3rd attacks: 1s; 2nd attack: 0.9s": {
        "ko": "1타 및 3타: 1초 | 2타: 0.9초",
        "ja": "1打目および3打目: 1秒 | 2打目: 0.9秒"
    },
    "0.75% Maximum Health": {
        "ko": "최대 체력의 0.75%",
        "ja": "最大HPの0.75%"
    },
    "2 times per second": {
        "ko": "초당 2회",
        "ja": "毎秒2回"
    },
    "First 4 hits: 15 each; 5th hit: 30": {
        "ko": "1~4타: 각 15 | 5타: 30",
        "ja": "1〜4撃目: 各15 | 5撃目: 30"
    },
    "First 4 hits: 8% Maximum Health each; 5th hit: 12% Maximum Health": {
        "ko": "1~4타: 각 최대 체력의 8% | 5타: 최대 체력의 12%",
        "ja": "1〜4撃目: 各最大HPの8% | 5撃目: 最大HPの12%"
    },
    "150% of Bleed Damage Dealt": {
        "ko": "입힌 출혈 피해의 150%",
        "ja": "与えた出血ダメージの150%"
    },
    "Maximum Health +100": {
        "ko": "최대 체력 +100",
        "ja": "最大HP +100"
    },

    # Emma Frost
    "Damage increases with energy: 0 - 70/s, 99 - 110/s, full energy - 140/s": {
        "ko": "에너지에 따라 데미지 증가: 0 - 초당 70, 99 - 초당 110, 풀 에너지 - 초당 140",
        "ja": "エネルギーに応じてダメージ増加: 0で毎秒70、99で毎秒110、最大エネルギーで毎秒140"
    },
    "Energy gain: Hero hit: 12/s; Sentience hit: 18/s; Common summons hit: 5/s; Shield hit: 6/s. Falloff begins 4s after not hitting an enemy, at a rate of 30/s": {
        "ko": "에너지 획득: 영웅 적중 초당 12, Sentience 적중 초당 18, 일반 소환수 적중 초당 5, 쉴드 적중 초당 6. 적 미적중 4초 후 초당 30씩 감쇠",
        "ja": "エネルギー獲得: ヒーロー命中 毎秒12、Sentience命中 毎秒18、通常召喚物命中 毎秒5、シールド命中 毎秒6。敵非命中4秒後、毎秒30ずつ減衰"
    },
    "First & second hit: 50; third hit: 70; fourth hit: 80": {
        "ko": "1~2타: 50 | 3타: 70 | 4타: 80",
        "ja": "1〜2撃目: 50 | 3撃目: 70 | 4撃目: 80"
    },
    "Deployable Shield": {
        "ko": "설치형 쉴드",
        "ja": "設置型シールド"
    },
    "Hit damage: 40; damage increases to 90 when the target is knocked into walls": {
        "ko": "타격 데미지: 40 | 대상을 벽에 충돌시킬 경우 90으로 데미지 증가",
        "ja": "命中ダメージ: 40 | 対象を壁に激突させた場合ダメージが90に増加"
    },
    "Maximum knockback distance: 10m": {
        "ko": "최대 넉백 거리: 10m",
        "ja": "最大ノックバック距離: 10m"
    },
    "Large-ranged Persistent Spell Field": {
        "ko": "광범위 지속형 장판",
        "ja": "広範囲持続型フィールド"
    },
    "Basic damage 80/s; distance falloff: falloff begins at 10m, decreasing to 70% at 30m; angle falloff: falloff begins at 7° from the center of view, decreasing to 80% at 20°": {
        "ko": "기본 데미지 초당 80. 거리 감쇠: 10m에서 감쇠 시작, 30m에서 70%로 감소. 각도 감쇠: 시야 중심 7°에서 감쇠 시작, 20°에서 80%로 감소",
        "ja": "基本ダメージ毎秒80。距離減衰: 10mで減衰開始、30mで70%に低下。角度減衰: 視界中央7°で減衰開始、20°で80%に低下"
    },
    "When exposed to the ability, enemies accumulate 10 stacks per second, and the stacks decrease by 10 stacks per second when they leave the exposure. At 15 stacks, a control effect is triggered. Each enemy can only be controlled once per ultimate activation. Gain 25% Damage Reduction during the ability.": {
        "ko": "스킬 범위 노출 시 적은 초당 10스택이 누적되며 벗어나면 초당 10스택씩 감소합니다. 15스택 시 제어 효과가 발동합니다. 궁극기 발동당 적마다 1회만 제어 가능. 스킬 지속 중 피해 감소 25% 획득.",
        "ja": "効果範囲にいる敵は毎秒10スタック蓄積し、離脱すると毎秒10スタック減少します。15スタックで行動妨害が発動。アルティメット発動ごとに各敵1回のみ妨害可能。発動中は被ダメージ25%軽減を獲得。"
    },
    "Switch Form": {
        "ko": "형태 전환",
        "ja": "形態切り替え"
    },
    "25% Damage Reduction in Diamond form": {
        "ko": "Diamond 형태에서 피해 감소 25%",
        "ja": "Diamond形態時、被ダメージ25%軽減"
    },
    "Single-cast delayed projectile": {
        "ko": "단발 지연 투사체",
        "ja": "単発遅延弾"
    },
    "Target's 25% Current Health": {
        "ko": "대상 현재 체력의 25%",
        "ja": "対象の現在HPの25%"
    },
    "Deal 5 damage per direct hit. When the sentience shatters, it deals damage to the target, which is equal to 25% of the target's maximum health": {
        "ko": "직격당 5 데미지. Sentience가 파괴될 때 대상 최대 체력의 25%에 해당하는 피해를 입힘",
        "ja": "直撃時5ダメージ。Sentience粉砕時、対象の最大HPの25%に相当するダメージを与える"
    },
    "When the distance between the target and its sentience is more than 15m, their linkage can be broken": {
        "ko": "대상과 Sentience 간의 거리가 15m를 초과하면 연결이 끊어질 수 있음",
        "ja": "対象とSentienceの距離が15mを超えるとリンクが解除される"
    },
    "Dash Based Control": {
        "ko": "돌진형 제어",
        "ja": "突進型行動妨害"
    },
    "Control effect duration: 1.6s": {
        "ko": "제어 효과 지속 시간: 1.6초",
        "ja": "行動妨害持続時間: 1.6秒"
    },
    "A fan-shaped spell field with a radius of 12m, a height of 3m, and an angle of 60°": {
        "ko": "반경 12m, 높이 3m, 각도 60°의 부채꼴 장판",
        "ja": "半径12m、高さ3m、角度60°の扇形フィールド"
    },

    # Gambit
    "2°": {
        "ko": "2°",
        "ja": "2°"
    },
    "Heal 30 health per second within duration": {
        "ko": "지속 시간 동안 초당 30 체력 치유",
        "ja": "持続時間中、毎秒30HPを回復"
    },
    "Within the duration, consume one stack of Sleight of Hand to use Bridge Boost and Purifying Pick-Up.": {
        "ko": "지속 시간 동안 Sleight of Hand 1스택을 소모하여 Bridge Boost 및 Purifying Pick-Up 사용 가능.",
        "ja": "持続時間中、Sleight of Handを1スタック消費してBridge BoostおよびPurifying Pick-Upを使用可能。"
    },
    "Within the duration, consume one stack of Sleight of Hand to use Explosive Trick and Bidding Barrage": {
        "ko": "지속 시간 동안 Sleight of Hand 1스택을 소모하여 Explosive Trick 및 Bidding Barrage 사용 가능",
        "ja": "持続時間中、Sleight of Handを1スタック消費してExplosive TrickおよびBidding Barrageを使用可能"
    },
    "The projectile automatically tracks allies and will bounce between allies on impact. Bridge Boost bounces on a single target are set to a maximum of 2": {
        "ko": "투사체가 아군을 자동 추적하며 충돌 시 아군 사이를 바운드합니다. 단일 대상에 대한 Bridge Boost 바운드는 최대 2회",
        "ja": "弾は味方を自動追跡し、着弾時に味方同士をバウンドします。単一対象に対するBridge Boostのバウンドは最大2回"
    },
    "55 per round": {
        "ko": "발당 55",
        "ja": "1発あたり55"
    },
    "Launch enemies up on hit, which can take effect only once.": {
        "ko": "적중 시 적을 띄움 (1회만 적용 가능).",
        "ja": "命中時に敵を打ち上げる（発動は1回のみ有効）。"
    },
    "The spell field applies Purify to allies upon impact. This can take effect on allies a maximum of 2 times and on himself once.": {
        "ko": "장판이 충돌 시 아군에게 정화(Purify) 효과를 부여합니다. 아군에게는 최대 2회, 본인에게는 1회 적용 가능.",
        "ja": "フィールド着弾時に味方へ浄化（Purify）を付与。味方には最大2回、自身には1回まで発動可能。"
    },

    # Gorr the God Butcher
    "40 for the 1st/3rd hits, 60 for the 2nd/4th hits": {
        "ko": "1/3타: 40 | 2/4타: 60",
        "ja": "1/3撃目: 40 | 2/4撃目: 60"
    },
    "0.4s for the 1st/3rd hits, 0.6s for the 2nd/4th hits": {
        "ko": "1/3타: 0.4초 | 2/4타: 0.6초",
        "ja": "1/3撃目: 0.4秒 | 2/4撃目: 0.6秒"
    },
    "65 + 10% Max Health": {
        "ko": "65 + 최대 체력의 10%",
        "ja": "65 + 最大HPの10%"
    },
    "100%, up to 50": {
        "ko": "100%, 최대 50",
        "ja": "100%、最大50"
    },
    "2 charges, 10s recharge each.": {
        "ko": "2회 충전, 충전당 10초 소요.",
        "ja": "2チャージ、チャージごとに10秒。"
    },
    "50% of the Black Berserker's remaining Health, up to 50; shares the Bonus Health cap with Berserker Swarm": {
        "ko": "Black Berserker 남은 체력의 50%, 최대 50. Berserker Swarm과 Bonus Health 상한 공유",
        "ja": "Black Berserkerの残HPの50%（最大50）。Berserker SwarmとBonus Health上限を共有"
    },
    "5 + 5% Max Health": {
        "ko": "5 + 최대 체력의 5%",
        "ja": "5 + 最大HPの5%"
    },
    "55 + 2% Max Health": {
        "ko": "55 + 최대 체력의 2%",
        "ja": "55 + 最大HPの2%"
    },

    # Invisible Woman
    "Orbs can pierce heroes and return to Invisible Woman after reaching their maximum distance. They damage enemies and heal teammates": {
        "ko": "구체는 영웅을 관통하며 최대 사거리에 도달한 후 Invisible Woman에게 복귀합니다. 적에게 피해를 주고 아군을 치유합니다",
        "ja": "オーブはヒーローを貫通し、最大距離到達後にInvisible Womanへ戻ります。敵にダメージを与え、味方を回復します"
    },
    "Deal 30 damage per hit upon being shot out and 15 damage per hit on its return journey.": {
        "ko": "발사 시 타격당 30 데미지, 복귀 시 타격당 15 데미지.",
        "ja": "射出時1ヒットあたり30ダメージ、帰還時1ヒットあたり15ダメージ。"
    },
    "No falloff": {
        "ko": "감쇠 없음",
        "ja": "減衰なし"
    },
    "Heal 50 health per hit upon being shot out and 45 health per hit on its return journey.": {
        "ko": "발사 시 타격당 50 치유, 복귀 시 타격당 45 치유.",
        "ja": "射出時1ヒットあたり50回復、帰還時1ヒットあたり45回復。"
    },
    "50/sec, self 20/sec": {
        "ko": "초당 50 | 본인 초당 20",
        "ja": "毎秒50 | 自身 毎秒20"
    },
    "Before the shield is destroyed, Invisible Woman can choose to reproject the shield onto a selected teammate at any time": {
        "ko": "쉴드가 파괴되기 전에는 언제든지 선택한 팀원에게 쉴드를 재배치할 수 있습니다",
        "ja": "シールドが破壊される前であれば、いつでも選択した味方にシールドを再展開可能"
    },
    "After the shield has been damaged, Invisible Woman can press the F key to reclaim the shield and restore its value": {
        "ko": "쉴드가 피해를 입은 후 F키를 눌러 쉴드를 회수하고 내구도를 복구할 수 있습니다",
        "ja": "シールド損傷後、Fキーを押してシールドを回収し耐久値を回復可能"
    },
    "If no Guardian Shield is present, pressing the recall key now deploys a shield in front of Invisible Woman": {
        "ko": "배치된 Guardian Shield가 없을 때 회수 키를 누르면 Invisible Woman 전방에 쉴드를 전개합니다",
        "ja": "展開中のGuardian Shieldがない場合、回収キーを押すとInvisible Womanの前方にシールドを展開します"
    },
    "Targeted, generates a cylindrical spell field": {
        "ko": "타겟 지정형, 원기둥형 장판 생성",
        "ja": "ターゲット指定型、円柱状フィールドを生成"
    },
    "200/sec": {
        "ko": "초당 200",
        "ja": "毎秒200"
    },
    "10m radius, 40m height": {
        "ko": "반경 10m, 높이 40m",
        "ja": "半径10m、高さ40m"
    },
    "Slows enemies within range by 20%": {
        "ko": "범위 내 적을 20% 둔화",
        "ja": "範囲内の敵に20%のスロウを付与"
    },
    "35/sec": {
        "ko": "초당 35",
        "ja": "毎秒35"
    },
    "Applies a slow effect to enemies within the spell field; the closer they are to the center of the field, the greater the slow effect": {
        "ko": "장판 내 적에게 둔화 효과 적용. 장판 중심에 가까울수록 더 강한 둔화 적용",
        "ja": "フィールド内の敵にスロウを付与。中心に近いほどスロウ効果が増加"
    },
    "Center 50%, Edge 0": {
        "ko": "중심 50%, 외곽 0",
        "ja": "中心50%、外縁0"
    },
    "1.5m radius, 35m length": {
        "ko": "반경 1.5m, 길이 35m",
        "ja": "半径1.5m、長さ35m"
    },
    "30/sec": {
        "ko": "초당 30",
        "ja": "毎秒30"
    },

    # JEFF THE LAND SHARK
    "Rapid-fire, delayed projectile": {
        "ko": "고속 연사, 지연 투사체",
        "ja": "高速連射、遅延弾"
    },
    "Damage falloff starts at 15m to a maximum of 60% at 30m": {
        "ko": "15m에서 데미지 감쇠 시작, 30m에서 최대 60%까지 감소",
        "ja": "15mで減衰開始、30mで最大60%まで低下"
    },
    "Projectile Damage: 25 damage per round, Spell Field Damage: 45 damage per cast": {
        "ko": "투사체 데미지: 발당 25 | 장판 데미지: 시전당 45",
        "ja": "弾ダメージ: 1発あたり25 | フィールドダメージ: 発動ごとに45"
    },
    "Falloff begins at 1m, decreasing to 50% at 3m (projectile damage has no falloff)": {
        "ko": "1m에서 감쇠 시작, 3m에서 50%로 감소 (투사체 데미지는 감쇠 없음)",
        "ja": "1mで減衰開始、3mで50%に低下（弾ダメージは減衰なし）"
    },
    "Direct hits can launch enemies up": {
        "ko": "직격 시 적을 공중으로 띄움",
        "ja": "直撃時に敵を打ち上げる"
    },
    "After swallowing allies and enemies, Jeff will deal damage to enemies and heal allies for the duration of the effect, during which they will also benefit from Hide and Seek": {
        "ko": "아군과 적을 삼킨 후 효과 지속 시간 동안 적에게 피해를 주고 아군을 치유하며 아군은 Hide and Seek 효과도 적용받습니다",
        "ja": "味方と敵を飲み込んだ後、効果持続中に敵へダメージを与え味方を回復、味方はHide and Seekの恩恵も受けます"
    },
    "It's Jeff! (Ultimate Ability) leaves an 8m radius Healing Pool at the point of activation that heals allies within range by 100/s. Healing Pool lasts for 8s": {
        "ko": "It's Jeff! (궁극기) 시전 지점에 반경 8m의 Healing Pool을 남겨 범위 내 아군을 초당 100 치유합니다. Healing Pool은 8초간 지속됩니다",
        "ja": "It's Jeff!（アルティメット）発動地点に半径8mのHealing Poolを残し、範囲内の味方を毎秒100回復。Healing Poolは8秒間持続"
    },
    "10m radius,5m high cylindrical spell field": {
        "ko": "반경 10m, 높이 5m의 원기둥형 장판",
        "ja": "半径10m、高さ5mの円柱状フィールド"
    },
    "Overflow healing on swallowed allies grants 45 Health per second as Bonus Health, up to 150": {
        "ko": "삼켜진 아군의 초과 치유량은 초당 45만큼 Bonus Health로 전환 (최대 150)",
        "ja": "飲み込まれた味方の超過回復量は毎秒45のBonus Healthとして付与（最大150）"
    },
    "During the dive, gain Unstoppable, healing over time, and a Movement Boost, while Jeff's hitbox is reduced": {
        "ko": "잠수 중 저지 불가(Unstoppable), 지속 치유, 이동 속도 증가를 획득하며 Jeff의 피격 판정이 축소됩니다",
        "ja": "潜航中、妨害無効（Unstoppable）、継続回復、移動速度上昇を獲得し、Jeffの当たり判定が縮小"
    },
    "Summons": {
        "ko": "소환물",
        "ja": "召喚物"
    },
    "Touching the bubble will immediately activate its effect": {
        "ko": "방울에 접촉 시 즉시 효과 발동",
        "ja": "泡に触れると即座に効果が発動"
    },
    "Falloff begins at 3s and decreases by 30/s": {
        "ko": "3초 후 감쇠 시작, 초당 30씩 감소",
        "ja": "3秒後に減衰開始、毎秒30減少"
    },
    "60m radius, 90° fan-shaped area in front of Jeff": {
        "ko": "Jeff 전방 반경 60m, 90° 부채꼴 영역",
        "ja": "Jeffの前方、半径60m・90°の扇形エリア"
    },
    "10m spherical radius spell field centered around Storm": {
        "ko": "Storm 중심 반경 10m 구형 장판",
        "ja": "Stormを中心とする半径10mの球状フィールド"
    },

    # Jubilation Lee
    "6 seconds; when reaching its max charge for the first time, duration is increased by 6 seconds": {
        "ko": "6초. 처음 최대 충전에 도달할 때 지속 시간 6초 증가",
        "ja": "6秒。初回最大チャージ到達時に持続時間が6秒延長"
    },
    "250 Healing/Damage": {
        "ko": "250 치유/피해",
        "ja": "250 回復/ダメージ"
    },
    "4m radius, increasing linearly with energy; up to 8m at max energy": {
        "ko": "반경 4m, 에너지에 따라 선형 증가 (최대 에너지 시 최대 8m)",
        "ja": "半径4m、エネルギーに応じて線形増加（最大エネルギー時 最大8m）"
    },
    "35/sec, increasing linearly with energy; up to 50/sec at max energy": {
        "ko": "초당 35, 에너지에 따라 선형 증가 (최대 에너지 시 최대 초당 50)",
        "ja": "毎秒35、エネルギーに応じて線形増加（最大エネルギー時 最大毎秒50）"
    },
    "0; increases linearly with energy, reaching max when the orb's remaining duration is greater than 6 seconds, restoring 1 charge": {
        "ko": "0. 에너지에 따라 선형 증가하며, 구체의 남은 지속 시간이 6초보다 길 때 최대치에 도달하여 충전 1회 복구",
        "ja": "0。エネルギーに応じて線形増加し、オーブの残り時間が6秒以上の時に最大となりチャージを1回復"
    },
    "Inner circle radius 6m; Outer circle radius 10m": {
        "ko": "내측 원 반경 6m, 외측 원 반경 10m",
        "ja": "内円半径6m、外円半径10m"
    },
    "Matches current range of selected orb": {
        "ko": "선택된 구체의 현재 범위와 동일",
        "ja": "選択したオーブの現在の範囲と一致"
    },
    "25/sec for 3s": {
        "ko": "3초 동안 초당 25",
        "ja": "3秒間、毎秒25"
    },

    # LOKI
    "The projectile deals no damage, while the spell field inflicts 25 damage per cast": {
        "ko": "투사체 피해는 없으며, 장판이 시전당 25의 피해를 입힙니다",
        "ja": "弾自体にダメージはなく、フィールドが発動ごとに25ダメージを与えます"
    },
    "Falloff begins at 0.5m, decreasing to 80% at 2.5m": {
        "ko": "0.5m에서 감쇠 시작, 2.5m에서 80%로 감소",
        "ja": "0.5mで減衰開始、2.5mで80%に低下"
    },
    "Loki leaves an illusion in his place and becomes invisible while continuously healing himself. This invisibility has no time limit, but any actions other than casting Devious Exchange, reloading, or casting Doppelganger will render him visible": {
        "ko": "Loki는 원래 자리에 분신을 남기고 은신 상태가 되어 자신을 지속 치유합니다. 이 은신은 시간 제한이 없으나 Devious Exchange 시전, 재장전, Doppelganger 시전 외의 행동을 하면 은신이 해제됩니다",
        "ja": "Lokiはその場に分身を残して透明化し、自身を継続回復します。この透明化には時間制限がありませんが、Devious Exchange発動、リロード、Doppelganger発動以外のアクションを行うと姿を現します"
    },
    "Health regenerates at a rate of 20 Health per second while invisible": {
        "ko": "은신 상태 동안 초당 20의 체력이 회복됩니다",
        "ja": "透明化中、毎秒20のHPが自動回復します"
    },
    "After transforming, Loki's Ultimate ability will be fully charged. Casting a transformation-type Ultimate ability will extend the duration of God of Mischief until the transformation ability ends": {
        "ko": "변신 후 Loki의 궁극기가 완전히 충전됩니다. 변신형 궁극기를 시전하면 God of Mischief 지속 시간이 해당 변신 궁극기가 끝날 때까지 연장됩니다",
        "ja": "変身後、Lokiのアルティメットがフルチャージされます。変身系アルティメットを発動すると、そのアビリティ終了までGod of Mischiefの持続時間が延長されます"
    },
    "Release a spell field at the location of Loki and the Illusion": {
        "ko": "Loki 및 분신의 위치에 장판 방출",
        "ja": "Lokiおよび分身の位置にフィールドを展開"
    },
    "The spell field is sustained by Rune Stones. It will disappear if the Rune Stone is destroyed or if its maximum duration is reached. Allies within the field will receive healing over time, and any damage taken will be converted into healing based on the amount of damage taken": {
        "ko": "장판은 Rune Stone에 의해 유지됩니다. Rune Stone이 파괴되거나 최대 지속 시간에 도달하면 소멸합니다. 장판 내 아군은 지속 치유를 받으며, 받는 피해는 피해량에 비례하여 치유로 전환됩니다",
        "ja": "フィールドはRune Stoneによって維持されます。Rune Stoneが破壊されるか最大持続時間に達すると消失します。フィールド内の味方は継続回復を受け、被ダメージは受けた量に応じて回復に変換されます"
    },
    "A cylindrical spell field with a radius of 5m and a height of 2m": {
        "ko": "반경 5m, 높이 2m의 원기둥형 장판",
        "ja": "半径5m、高さ2mの円柱状フィールド"
    },
    "A cylindrical spell field with a radius of 6.5m and a height of 2m.": {
        "ko": "반경 6.5m, 높이 2m의 원기둥형 장판.",
        "ja": "半径6.5m、高さ2mの円柱状フィールド。"
    },
    "Project an Illusion at a selected location": {
        "ko": "지정한 위치에 분신 투영",
        "ja": "指定した地点に分身を投影"
    },
    "Damage: 30; Backstab Damage: +15 (total of 45)": {
        "ko": "데미지: 30 | 백스탭 데미지: +15 (총 45)",
        "ja": "ダメージ: 30 | バックスタブダメージ: +15（合計45）"
    },

    # LUNA SNOW
    "A triple shot that hits instantly": {
        "ko": "즉시 적중하는 3연발 사격",
        "ja": "即座に着弾する3連発射撃"
    },
    "24 damage per round, for a total of 72 damage": {
        "ko": "발당 24 데미지 (총 72 데미지)",
        "ja": "1発あたり24ダメージ（合計72ダメージ）"
    },
    "24 health per round, for a total of 72 health": {
        "ko": "발당 24 치유 (총 72 치유)",
        "ja": "1発あたり24回復（合計72回復）"
    },
    "0.5s for three shots. The interval between the first two shots is 0.05s": {
        "ko": "3발 발사 시 0.5초. 첫 2발 간의 간격은 0.05초",
        "ja": "3発で0.5秒。最初の2発の間隔は0.05秒"
    },
    "Freeze enemies for 2.7s. However, if they are attacked during the last 2.2s of the freeze, the effect will be canceled. Grants 50 Bonus Health per enemy hit": {
        "ko": "적을 2.7초 동안 결빙시킵니다. 단 결빙 마지막 2.2초 동안 공격을 받으면 결빙이 해제됩니다. 적중한 적마다 50의 Bonus Health 부여",
        "ja": "敵を2.7秒間凍結。ただし凍結の後半2.2秒間に攻撃を受けると解除されます。命中した敵ごとに50のBonus Healthを獲得"
    },
    "Single-cast spell field that pierces through enemies": {
        "ko": "적을 관통하는 단발 장판",
        "ja": "敵を貫通する単発フィールド"
    },
    "Replace the previous Light & Dark Ice cast": {
        "ko": "이전 Light & Dark Ice 시전을 대체",
        "ja": "直前のLight & Dark Iceの発動を上書き"
    },
    "A cylindrical spell field with a radius of 1m and a height of 40m": {
        "ko": "반경 1m, 높이 40m의 원기둥형 장판",
        "ja": "半径1m、高さ40mの円柱状フィールド"
    },
    "Provide healing to allies marked with Idol Aura; Reduce Ice Arts cooldown by 2s whenever a hero with Idol Aura takes part in a KO": {
        "ko": "Idol Aura가 부여된 아군에게 치유 제공. Idol Aura를 가진 영웅이 처치에 관여할 때마다 Ice Arts 쿨다운 2초 감소",
        "ja": "Idol Auraが付与された味方を回復。Idol Auraを持つヒーローが撃破に関与するたびにIce Artsのクールダウンが2秒短縮"
    },
    "30/s for 3 seconds": {
        "ko": "3초 동안 초당 30",
        "ja": "3秒間、毎秒30"
    },

    # MANTIS
    "Critical hit generates 1 Life Orb": {
        "ko": "치명타 적중 시 Life Orb 1개 생성",
        "ja": "クリティカルヒット時にLife Orbを1個生成"
    },
    "Healing Flower provides two types of healing effects: One-time Healing and Healing Over Time": {
        "ko": "Healing Flower는 즉시 치유와 지속 치유의 두 가지 치유 효과를 제공합니다",
        "ja": "Healing Flowerは即時回復と継続回復の2種類の回復効果を提供します"
    },
    "10 + 2.5% of the target's maximum Health per second": {
        "ko": "초당 10 + 대상 최대 체력의 2.5%",
        "ja": "毎秒10 + 対象の最大HPの2.5%"
    },
    "8s (16s maximum duration)": {
        "ko": "8초 (최대 지속 시간 16초)",
        "ja": "8秒（最大持続時間16秒）"
    },
    "A Mantis illusions will manifest beside the sedated heroes. Allies can attack this illusion to awaken the affected hero": {
        "ko": "수면 상태에 걸린 영웅 옆에 Mantis 분신이 나타납니다. 아군이 이 분신을 공격하여 수면 상태의 영웅을 깨울 수 있습니다",
        "ja": "催眠状態のヒーローの隣にMantisの幻影が現れます。味方はこの幻影を攻撃することで対象ヒーローを目覚めさせることができます"
    },
    "8s (the duration cannot stack; repeatedly casting will only refresh the duration)": {
        "ko": "8초 (지속 시간은 중첩되지 않으며 재시전 시 지속 시간만 갱신)",
        "ja": "8秒（効果時間はスタックせず、再発動時は持続時間のみ更新）"
    },
    "Consume Life Orbs to receive Healing Over Time": {
        "ko": "Life Orb를 소모하여 지속 치유 획득",
        "ja": "Life Orbを消費して継続回復を獲得"
    },

    # Mister Fantastic
    "Straight Spell Field": {
        "ko": "직선형 장판",
        "ja": "直線型フィールド"
    },
    "Swinging your arms can attack multiple targets": {
        "ko": "팔을 휘둘러 여러 대상을 동시에 공격 가능",
        "ja": "腕を振り回すことで複数の対象を攻撃可能"
    },
    "After successfully pulling an enemy with Distended Grip, the target is afflicted with a 1-second immobilize effect": {
        "ko": "Distended Grip으로 적을 당겨오는 데 성공하면 대상에게 1초간 이동 불가(Immobilize) 부여",
        "ja": "Distended Gripで敵を引き寄せることに成功すると、対象に1秒間の移動不能（Immobilize）を付与"
    },
    "Initial 70, Each Additional Leap +14, Max 140": {
        "ko": "기본 70, 추가 도약마다 +14, 최대 140",
        "ja": "初期70、追加ジャンプごとに+14、最大140"
    },
    "Start at 3m, 71.4% falloff at 10m": {
        "ko": "3m에서 감쇠 시작, 10m에서 71.4% 감쇠",
        "ja": "3mで減衰開始、10mで71.4%減衰"
    },
    "Per Leap -10%, Can Stack, Max -60%": {
        "ko": "도약마다 -10%, 중첩 가능, 최대 -60%",
        "ja": "ジャンプごとに-10%、スタック可能、最大-60%"
    },
    "When Mister Fantastic uses Brainiac Bounce (Ultimate Ability), immediately gain Bonus Health equal to that gained when entering inflated state": {
        "ko": "Mister Fantastic이 Brainiac Bounce (궁극기) 사용 시 팽창 상태 진입 시와 동일한 Bonus Health 즉시 획득",
        "ja": "Mister FantasticがBrainiac Bounce（アルティメット）使用時、膨張状態突入時と同等のBonus Healthを即座に獲得"
    },
    "gain 350 Maximum Health and a one-time heal of 350, which is removed upon exiting the Inflated state": {
        "ko": "최대 체력 350 증가 및 350 즉시 치유 획득 (팽창 상태 종료 시 제거)",
        "ja": "最大HPが350増加し350の即時回復を獲得（膨張状態終了時に消失）"
    },

    # PHOENIX
    "Apply 1 Spark to enemies hit. Critical hits apply 2 Sparks. At 3 Sparks, Phoenix triggers a fiery explosion that applies 1 Spark to enemies around. Sparks from explosions will not stack within a brief period.": {
        "ko": "적중한 적에게 Spark 1개 부여. 치명타 적중 시 Spark 2개 부여. 3스택 시 폭발을 일으키며 주변 적에게 Spark 1개를 부여합니다. 폭발로 인한 Spark는 짧은 시간 동안 중첩되지 않습니다.",
        "ja": "命中した敵にSparkを1個付与。クリティカル時は2個付与。3個で火炎爆発を引き起こし周囲の敵にSparkを1個付与。爆発によるSparkは短時間の間スタックしません。"
    },
    "5/s for 4 s": {
        "ko": "4초 동안 초당 5",
        "ja": "4秒間、毎秒5"
    },
    "The first blast Stuns enemies, while the subsequent two explosions inflict Slow.": {
        "ko": "첫 번째 폭발은 적을 기절(Stun)시키며, 이어지는 두 번의 폭발은 둔화를 부여합니다.",
        "ja": "最初の爆発は敵をスタンさせ、続く2回の爆発はスロウを付与します。"
    },
    "Inflict 30% Slow for 2 seconds.": {
        "ko": "2초 동안 30% 둔화 부여.",
        "ja": "2秒間、30%のスロウを付与。"
    },
    "The shockwave destroys enemy summons, shields, and any Bonus Health. Enemies hit by the spell field and the shockwave are applied with 1 Spark.": {
        "ko": "충격파가 적 소환물, 쉴드, Bonus Health를 모두 파괴합니다. 장판 및 충격파에 적중당한 적에게 Spark 1개를 부여합니다.",
        "ja": "衝撃波は敵の召喚物、シールド、Bonus Healthを破壊します。フィールドと衝撃波に命中した敵にSparkを1個付与します。"
    },
    "The detonation applies 1 Spark to enemies hit.": {
        "ko": "폭발 시 적중한 적에게 Spark 1개 부여.",
        "ja": "起爆時、命中した敵にSparkを1個付与。"
    },
    "Enter a state of free flight within the duration. Gain a 50% Movement Boost": {
        "ko": "지속 시간 동안 자유 비행 상태 진입. 이동 속도 50% 증가 획득",
        "ja": "効果時間中、自由飛行状態に突入。移動速度50%上昇を獲得"
    },

    # ROCKET RACCOON
    "One-time healing for allies when projectile hits them，Bouncing Spheres will bounce off surfaces upon contact, with a maximum of 10 bounces. When they approach injured allies, their speed will reduce": {
        "ko": "투사체 적중 시 아군 즉시 치유. Bouncing Spheres는 표면 접촉 시 최대 10회까지 튕깁니다. 부상당한 아군에게 접근하면 속도가 느려집니다",
        "ja": "弾の着弾時に味方を即時回復。Bouncing Spheresは接触時に最大10回バウンドします。負傷した味方に接近すると速度が低下します"
    },
    "Targeted ability that, when activated, summons a creature and detects allies within the area.": {
        "ko": "발동 시 생명체를 소환하고 범위 내 아군을 탐지하는 타겟 지정 스킬.",
        "ja": "発動時にクリーチャーを召喚しエリア内の味方を索敵するターゲット指定アビリティ。"
    },
    "During the ability's duration, linked allies will receive an additional 100 Bonus Health points per second, capping at 150. After breaking the link, this bonus starts to falloff after 1 second at a rate of 75 per/s": {
        "ko": "스킬 지속 중 연결된 아군은 초당 100의 Bonus Health를 추가로 받으며 최대 150까지 적용됩니다. 연결 해제 후 1초 뒤부터 초당 75의 속도로 감쇠하기 시작합니다",
        "ja": "アビリティ中、リンクされた味方は毎秒100のBonus Healthを追加獲得（最大150）。リンク解除後は1秒後から毎秒75の割合で減衰が始まります"
    },
    "Crosshair Direction": {
        "ko": "조준선 방향",
        "ja": "照準方向"
    },
    "Generate an item every 3s, including Armor Pack and Rocket Boots": {
        "ko": "Armor Pack 및 Rocket Boots를 포함한 아이템을 3초마다 생성",
        "ja": "Armor PackおよびRocket Bootsを含むアイテムを3秒ごとに生成"
    },
    "40s. You can reclaim the beacon by pressing E. When reclaimed, the cooldown will be reduced based on the beacon's remaining health. If you reclaim a full-health beacon, the minimum cooldown will be 5s": {
        "ko": "40초. E키를 눌러 비콘을 회수할 수 있습니다. 회수 시 비콘의 남은 체력에 따라 쿨다운이 감소합니다. 풀 체력 비콘 회수 시 최소 쿨다운은 5초입니다",
        "ja": "40秒。Eキーを押してビーコンを回収可能。回収時、ビーコンの残HPに応じてクールダウンが短縮されます。フルHPのビーコンを回収した場合、最小クールダウンは5秒です"
    },
    "Pressing SHIFT will exit the Team-Up status with Groot": {
        "ko": "SHIFT를 누르면 Groot와의 Team-Up 상태를 종료합니다",
        "ja": "SHIFTを押すとGrootとのTeam-Up状態を解除します"
    },

    # Rogue
    "The first two strikes deal 35 damage, while the third strike deals 45 damage": {
        "ko": "1~2타는 35 데미지, 3타는 45 데미지",
        "ja": "1〜2撃目は35ダメージ、3撃目は45ダメージ"
    },
    "The first two strikes: 0.33s/hit; the third strike: 0.73s/hit": {
        "ko": "1~2타: 타당 0.33초 | 3타: 타당 0.73초",
        "ja": "1〜2撃目: 1打あたり0.33秒 | 3撃目: 1打あたり0.73秒"
    },
    "Launch up the enemies hit": {
        "ko": "적중한 적을 띄움",
        "ja": "命中した敵を打ち上げる"
    },
    "The reduced damage transforms into backlash energy that powers up the next Southern Brawl.": {
        "ko": "경감된 피해는 반격 에너지로 전환되어 다음 Southern Brawl을 강화합니다.",
        "ja": "軽減されたダメージは反動エネルギーに変換され、次のSouthern Brawlを強化します。"
    },
    "Absorb 4% of ultimate ability energy per second": {
        "ko": "초당 궁극기 에너지 4% 흡수",
        "ja": "毎秒4%のアルティメットエネルギーを吸収"
    },
    "400 maximum health": {
        "ko": "최대 체력 400",
        "ja": "最大HP 400"
    },
    "Self healing 75/s": {
        "ko": "초당 75 자가 치유",
        "ja": "毎秒75の自己回復"
    },
    "Launch up enemies hit": {
        "ko": "적중한 적을 띄움",
        "ja": "命中した敵を打ち上げる"
    },
    "Cylindrical Spell Field with a height of 3m, whose radius will expand to 8m after 0.8s": {
        "ko": "높이 3m의 원기둥형 장판, 0.8초 후 반경이 8m로 확장",
        "ja": "高さ3mの円柱状フィールド、0.8秒後に半径が8mまで拡大"
    },
    "Box shaped spell field. Length: 6.5m; Width: 4.5m; Height: 2m": {
        "ko": "상자형 장판. 길이: 6.5m, 너비: 4.5m, 높이: 2m",
        "ja": "ボックス型フィールド。長さ: 6.5m、幅: 4.5m、高さ: 2m"
    },
    "Launch up the enemy hit, entering flight. The next two Power Surge Punch attacks become ranged, and Chrono Kick Combo can be unleashed again.": {
        "ko": "적중한 적을 띄우고 비행 상태에 진입합니다. 다음 2회의 Power Surge Punch가 원거리 공격으로 바뀌며 Chrono Kick Combo를 재시전할 수 있습니다.",
        "ja": "命中した敵を打ち上げ、飛行状態に突入。次の2回のPower Surge Punchが遠距離攻撃となり、Chrono Kick Comboを再発動可能になります。"
    },
    "After absorbing, replace Ability Absorption with one of their abilities or refresh Fatal Attraction.": {
        "ko": "흡수 후 Ability Absorption을 대상의 스킬 중 하나로 대체하거나 Fatal Attraction을 초기화합니다.",
        "ja": "吸収後、Ability Absorptionが対象のアビリティの1つに置き換わるか、Fatal Attractionをリセットします。"
    },
    "125 Maximum Health": {
        "ko": "최대 체력 125",
        "ja": "最大HP 125"
    },
    "Reduce 20 Maximum Health": {
        "ko": "최대 체력 20 감소",
        "ja": "最大HP 20減少"
    },
    "Reduce 3% damage dealt": {
        "ko": "주는 피해 3% 감소",
        "ja": "与ダメージ 3%減少"
    },
    "Self healing 20/s": {
        "ko": "초당 20 자가 치유",
        "ja": "毎秒20の自己回復"
    },
    "Reduce 4% healing dealt": {
        "ko": "주는 치유 4% 감소",
        "ja": "与回復量 4%減少"
    },
    "5+targets' 2% Maximum Health": {
        "ko": "5 + 대상 최대 체력의 2%",
        "ja": "5 + 対象の最大HPの2%"
    },

    # The Hood
    "26 per round": {
        "ko": "발당 26",
        "ja": "1発あたり26"
    },
    "21 per round": {
        "ko": "발당 21",
        "ja": "1発あたり21"
    },
    "4 per round": {
        "ko": "발당 4",
        "ja": "1発あたり4"
    },
    "40%, Max100": {
        "ko": "40%, 최대 100",
        "ja": "40%、最大100"
    },
    "Spread radius reaches 0.5m after 10 consecutive shots (calculated at 10m distance)": {
        "ko": "연속 10발 사격 후 탄 퍼짐 반경 0.5m 도달 (10m 거리 기준 계산)",
        "ja": "連続10発射撃後に拡散半径が0.5mに到達（10m地点換算）"
    },
    "90 + 10% of Target's Max Health": {
        "ko": "90 + 대상 최대 체력의 10%",
        "ja": "90 + 対象の最大HPの10%"
    },
    "140 + 15% of Target's Max Health": {
        "ko": "140 + 대상 최대 체력의 15%",
        "ja": "140 + 対象の最大HPの15%"
    },
    "40% during the Ability, decaying to 0% over 2s after it ends": {
        "ko": "스킬 중 40%, 종료 후 2초에 걸쳐 0%로 감쇠",
        "ja": "発動中40%、終了後2秒かけて0%まで減衰"
    },
    "Width: 8m, Height: 3.5m.": {
        "ko": "너비: 8m, 높이: 3.5m.",
        "ja": "幅: 8m、高さ: 3.5m。"
    },

    # Ultron
    "First constant beam; Second single-cast cylindrical spell field": {
        "ko": "1차 지속 광선, 2차 단발 원기둥형 장판",
        "ja": "1次 継続ビーム、2次 単発円柱状フィールド"
    },
    "First beam 6 rounds in 0.5s, 12 per hit; second single-cast spell field 75 per hit": {
        "ko": "1차 광선 0.5초 동안 6발, 타당 12 | 2차 단발 장판 타당 75",
        "ja": "1次ビーム 0.5秒で6発・1打あたり12 | 2次単発フィールド 1打あたり75"
    },
    "Grant bonus health to Ultron and Allies within range, centered around Ultron and the drones; the selected ally gains a 20% Movement Speed and 10% Damage boost": {
        "ko": "Ultron과 드론을 중심으로 범위 내 Ultron 및 아군에게 Bonus Health 부여. 선택된 아군은 이동 속도 20% 및 피해 10% 증가 획득",
        "ja": "Ultronとドローンを中心に、範囲内のUltronと味方にBonus Healthを付与。選択した味方は移動速度20%およびダメージ10%上昇を獲得"
    },
    "Ultron's Encephalo-Rays 18, Drone's Encephalo-Rays 12": {
        "ko": "Ultron의 Encephalo-Rays 18 | 드론의 Encephalo-Rays 12",
        "ja": "UltronのEncephalo-Rays 18 | ドローンのEncephalo-Rays 12"
    },
    "Starts at 1.5m after Encephalo-Rays explode, with a max falloff to 50% at 3m": {
        "ko": "Encephalo-Rays 폭발 후 1.5m에서 감쇠 시작, 3m에서 최대 50%까지 감쇠",
        "ja": "Encephalo-Rays爆発後1.5mで減衰開始、3mで最大50%まで低下"
    },
    "5 rounds": {
        "ko": "5발",
        "ja": "5発"
    },
    "Within the ultimate duration, Ultron grants an Unstoppable effect; Deals 125% damage to Bonus Health": {
        "ko": "궁극기 지속 시간 동안 Ultron에게 저지 불가(Unstoppable) 부여. Bonus Health에 125% 데미지 적용",
        "ja": "アルティメット持続中、Ultronに妨害無効（Unstoppable）を付与。Bonus Healthに対して125%ダメージ"
    },
    "Dynamic Flight can trigger a one-time dash followed by an constant accelerated effect.": {
        "ko": "Dynamic Flight는 1회 돌진 후 지속적인 가속 효과를 발동할 수 있습니다.",
        "ja": "Dynamic Flightは1回のダッシュ後に継続的な加速効果を発動できます。"
    },
    "Reticle direction combined with key input": {
        "ko": "키 입력과 결합된 조준점 방향",
        "ja": "キー入力と連動したレティクル方向"
    },
    "Imperative: Patch can deploy up to 2 drones, allowing support for two allies at once": {
        "ko": "Imperative: Patch는 최대 2대의 드론을 배치하여 동시에 두 명의 아군을 지원할 수 있습니다",
        "ja": "Imperative: Patchは最大2機のドローンを展開し、同時に2人の味方を支援可能です"
    },
    "2.5m radius, infinite length cylindrical spell field": {
        "ko": "반경 2.5m, 무한 길이의 원기둥형 장판",
        "ja": "半径2.5m、無限長の円柱状フィールド"
    },

    # White Fox
    "Direct hit: 50 per round; bounce hit: 35 per round": {
        "ko": "직격: 발당 50 | 바운드 적중: 발당 35",
        "ja": "直撃: 1発あたり50 | バウンド命中: 1発あたり35"
    },
    "Direct hit: 40 per round; bounce hit: 25 per round": {
        "ko": "직격: 발당 40 | 바운드 적중: 발당 25",
        "ja": "直撃: 1発あたり40 | バウンド命中: 1発あたり25"
    },
    "After casting, automatically apply the Blessed by the Nine effect to all allies within a 10m radius for 3s.": {
        "ko": "시전 후 반경 10m 이내 모든 아군에게 3초 동안 Blessed by the Nine 효과를 자동 부여합니다.",
        "ja": "発動後、半径10m以内の全味方に3秒間Blessed by the Nine効果を自動付与。"
    },
    "While the shield is active, it provides 20/s Healing Over Time to allies (including White Fox) within the shield's range": {
        "ko": "쉴드가 활성화된 동안 쉴드 범위 내의 아군(White Fox 포함)에게 초당 20의 지속 치유를 제공합니다",
        "ja": "シールド展開中、範囲内の味方（White Foxを含む）に毎秒20の継続回復を提供します"
    },
    "Transform 3 tails: 9s; 2 tails: 8s; 1 tail: 7s": {
        "ko": "변신 3꼬리: 9초 | 2꼬리: 8초 | 1꼬리: 7초",
        "ja": "変身 3本尾: 9秒 | 2本尾: 8秒 | 1本尾: 7秒"
    }
}

def validate_and_generate():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    missing = []
    purity_errors = []
    results = {}

    for en_key in source_data.keys():
        if en_key not in STRATEGISTS_TRANSLATIONS:
            missing.append(en_key)
            continue
        
        tr = STRATEGISTS_TRANSLATIONS[en_key]
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
        for m in missing[:30]:
            print(f"  Missing: {m}")
        if len(missing) > 30:
            print(f"  ...and {len(missing) - 30} more")
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
