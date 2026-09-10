# -*- coding: utf-8 -*-
"""
Translations builder for Group 1 (Heroes 1 to 14):
ADAM WARLOCK, ANGELA, BLACK CAT, BLACK PANTHER, BLADE, Black Widow,
CAPTAIN AMERICA, Cloak & Dagger, Cyclops, DEADPOOL (VANGUARD, DUELIST, STRATEGIST),
DEVIL DINOSAUR, DOCTOR STRANGE
"""

import json
import re

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

SKILLS_MAP_G1 = {
    # === ADAM WARLOCK ===
    "Launch quantum energy to deal damage": {
        "ko": "양자 에너지를 발사하여 적에게 피해를 입힙니다.",
        "ja": "量子エネルギーを発射して敵にダメージを与える。"
    },
    "Gather quantum energy into a cluster and then swiftly launch it at the enemy": {
        "ko": "양자 에너지를 구체로 응축한 뒤 전방의 적에게 신속하게 발사합니다.",
        "ja": "量子エネルギーを凝縮し、前方の敵へ素早く撃ち出す。"
    },
    "Awaken the karma of allies to revive them. Allies revived have lower health but enjoy a brief period of Invincibility": {
        "ko": "아군의 업(Karma)을 일깨워 부활시킵니다. 부활한 아군은 체력이 낮지만 잠시 동안 무적 상태가 됩니다.",
        "ja": "味方のカルマを目覚めさせて蘇生する。蘇生した味方は体力が低下しているが、短時間の無敵状態を得る。"
    },
    "Forge a soul bond with allies, granting Healing Over Time and distributing damage taken across the bond": {
        "ko": "아군과 영혼 결속을 맺어 지속 치유를 부여하고, 결속된 팀원들이 받는 피해를 서로 분산시킵니다.",
        "ja": "味方とソウルボンド(魂の絆)を結び、持続回復を付与するとともに受けるダメージを分散して共有する。"
    },
    "Target an ally for a bouncing stream of healing energy, which also heals himself upon casting; self-targets if no ally is selected": {
        "ko": "아군을 지정해 튕겨 다니는 치유 에너지 줄기를 발사합니다. 시전 시 자신도 치유되며, 대상을 지정하지 않으면 자신에게 즉시 시전됩니다.",
        "ja": "味方を指定して跳弾する回復エネルギーを放ち、発動時に自身も回復する。味方未選択時は自身を対象とする。"
    },
    "Take to the skies, entering a flying state and swiftly surge forward": {
        "ko": "하늘로 날아올라 비행 상태에 돌입하며 전방으로 신속하게 급돌진합니다.",
        "ja": "上空へ飛び立って飛行状態に入り、前方へ素早く急突進する。"
    },
    "Storm channels her elemental power into Adam Warlock. When Adam uses Soaring Surge, his movement speed is increased. While flying, Adam leaves behind a storm-charged trail that heals and speeds up allies within it": {
        "ko": "스톰이 원소의 힘을 아담 워록에게 주입합니다. 비행 돌진 시 이동 속도가 증가하며, 비행 경로에 아군을 치유하고 가속하는 폭풍 궤적을 남깁니다.",
        "ja": "ストームが元素の力をアダム・ウォーロックに注ぎ込む。飛行突進時に移動速度が上昇し、軌跡に味方を回復・加速させる嵐の軌道を残す。"
    },
    "Once his body perishes, Adam Warlock can freely move as a soul and reforge his body at a chosen spot": {
        "ko": "육체가 쓰러지면 아담 워록은 영혼 상태로 자유롭게 이동하여 원하는 위치에서 육체를 재구성해 부활할 수 있습니다.",
        "ja": "肉体が滅びると、魂の状態で自由に移動し、選んだ地点で肉体を再構築して蘇生できる。"
    },

    # === ANGELA ===
    "Lunge forward with your spear, dealing damage that increases with Attack Charge. At full charge, Spear of Ichor can launch up enemies": {
        "ko": "창을 전방으로 찔러 공격 게이지(Attack Charge)에 비례한 피해를 입힙니다. 게이지가 가득 차면 적을 공중으로 띄웁니다.",
        "ja": "槍を前方に突き出して攻撃チャージに応じたダメージを与える。最大チャージ時は敵を打ち上げる。"
    },
    "Alternate powerful strikes forward with twin axes, dealing increased damage as Attack Charge grows. The fourth strike propels you forward in a swift dash": {
        "ko": "쌍도끼로 전방을 번갈아 강타하며 공격 게이지에 따라 피해량이 증가합니다. 4타 공격 시 전방으로 신속하게 돌진합니다.",
        "ja": "双斧で前方を交互に強打し、攻撃チャージに応じてダメージが上昇する。4打目に高速ダッシュで前方へ突進する。"
    },
    "Transform Ichors into a shield, gaining Attack Charge when absorbing damage": {
        "ko": "이코르(Ichor)를 방패로 변환하여 피해를 흡수하며, 피해 흡수 시 공격 게이지를 획득합니다.",
        "ja": "イコルを盾に変形させてダメージを吸収し、攻撃チャージを獲得する。"
    },
    "Wrap your spear in ribbons and hurl it with force. Upon impact, the ribbons bind nearby enemies. Angela can leap to the spear's location, damaging surrounding enemies and creating a Divine Judgement Zone": {
        "ko": "창에 리본을 감아 강력하게 투척합니다. 착탄 시 리본이 주변 적들을 결박하며, 안젤라는 창 위치로 도약하여 주변에 피해를 주고 신성한 심판 영역을 생성합니다.",
        "ja": "槍にリボンを巻き付けて力強く投擲する。着弾時に周囲の敵を拘束し、アンジェラは槍の位置へ跳躍して範囲ダメージを与え、神聖なる審判エリアを生成する。"
    },
    "Enter an accelerated dash state, enemies struck head-on are carried through the air for a short distance": {
        "ko": "가속 돌진 상태에 돌입하여 정면으로 충돌한 적을 잠시 공중으로 끌고 날아갑니다.",
        "ja": "加速ダッシュ状態に突入し、正面衝突した敵を短距離空中へ巻き込んで運ぶ。"
    },
    "Dive downward, switch to twin axes and infuse the ground with Ichors to create a Divine Judgement Zone upon impact. Within the zone, gain enhanced Speed and attacks grant Bonus Health to self and nearby allies": {
        "ko": "아래로 급강하하여 쌍도끼로 전환하고 착탄 시 지면에 이코르를 주입해 신성한 심판 영역을 생성합니다. 영역 내에서 이동 속도가 증가하고 공격 시 자신과 주변 아군에게 추가 체력을 부여합니다.",
        "ja": "急降下して双斧に切り替え、着地時に地面にイコルを注入して神聖なる審判エリアを展開する。エリア内では移動速度が上昇し、攻撃時に自身と周囲の味方へ追加体力を付与する。"
    },
    "Take to the skies, switching back to Spear of Ichors": {
        "ko": "하늘로 치솟아 오르며 이코르의 창으로 다시 전환합니다.",
        "ja": "上空へ飛び上がり、再びイコルの槍へと切り替える。"
    },
    "Glide freely through the air. Continuous flight builds Attack Charge": {
        "ko": "공중을 자유롭게 활공합니다. 비행을 지속할수록 공격 게이지가 서서히 충전됩니다.",
        "ja": "空中を自在に滑空する。滑空を維持することで攻撃チャージが徐々に蓄積される。"
    },
    "Angela shares fragments of her Ichors with Thor, empowering him to hurl a Thunder Spear that restores Thorforce for each enemy struck. Afterward, Thor can leap to the spear's explosion point, dealing a second wave of damage to all enemies within range": {
        "ko": "안젤라가 토르에게 이코르 파편을 공유하여, 적중한 적마다 토르포스를 회복하는 번개의 창을 투척할 수 있게 합니다. 이후 토르는 창의 폭발 지점으로 도약하여 범위 내 모든 적에게 2차 피해를 가합니다.",
        "ja": "アンジェラがソーにイコルの破片を分け与え、命中した敵ごとにソーフォースを回復する雷の槍を投擲できるようにする。その後、ソーは槍の爆発地点へ跳躍し、範囲内の全敵へ2次ダメージを与える。"
    },

    # === BLACK CAT ===
    "Swipe forward with razor-sharp claws": {
        "ko": "날카로운 발톱으로 전방을 빠르게 할퀴어 공격합니다.",
        "ja": "鋭利な鉤爪で前方を素早く切り裂く。"
    },
    "Fire out tethered claws and whip them forward in a devastating arc, dealing damage to all enemies caught in range": {
        "ko": "와이어 발톱을 발사하여 전방으로 크게 채찍질하며 호를 그리고, 범위 내의 모든 적에게 피해를 입힙니다.",
        "ja": "ワイヤー付きの爪を射出して前方へ大きく薙ぎ払い、範囲内の全敵にダメージを与える。"
    },
    "Toss a grappling hook toward terrain or surfaces to rapidly zip to that location": {
        "ko": "지형이나 벽면으로 갈고리를 던져 목표 위치로 빠르게 이동합니다.",
        "ja": "地形や壁面へグラップリングフックを投げ、その地点へ素早く高速移動する。"
    },
    "Leap backward gracefully, leaving behind an obscuring smoke bomb that conceals Felicia": {
        "ko": "우아하게 뒤로 도약하며 연막탄을 투척해 적의 시야를 가리고 펠리시아의 모습을 숨깁니다.",
        "ja": "優雅に後方へ跳躍し、視界を遮る煙幕弾を残して自身の姿を隠蔽する。"
    },
    "Sprint continuously with increased agility and jump height": {
        "ko": "향상된 민첩성과 점프 높이로 지치지 않고 지속해서 질주합니다.",
        "ja": "向上した敏捷性と跳躍力で、継続的にダッシュ走行する。"
    },
    "Somersault over an enemy, kicking them in the back to knock them down": {
        "ko": "적의 머리 위로 공중제비를 돌며 등 뒤를 발로 차 적을 넘어뜨립니다(Knockdown).",
        "ja": "敵の頭上を宙返りして背後を蹴り飛ばし、敵をノックダウンさせる。"
    },
    "Curse an enemy with terrible misfortune, causing them to take increased damage and fumble attacks": {
        "ko": "적에게 지독한 불운의 저주를 내려, 받는 피해를 증가시키고 공격을 빗나가게 만듭니다.",
        "ja": "敵に不運の呪いを付与し、被ダメージを増加させて攻撃を失敗させる。"
    },
    "Spin in a blinding whirlwind of claws that shreds all nearby enemy armor": {
        "ko": "눈부신 속도로 회전하며 발톱 폭풍을 일으켜 주변 적들의 방어구를 완전히 찢어발깁니다.",
        "ja": "目にも留まらぬ爪の旋風で回転し、周囲の敵の装甲を切り刻む。"
    },
    "Landing critical hits rewards Black Cat with bonus movement speed and luck energy": {
        "ko": "치명타를 명중시킬 때마다 블랙 캣에게 추가 이동 속도와 행운 에너지가 부여됩니다.",
        "ja": "クリティカルヒットを命中させると、追加の移動速度と幸運エネルギーを獲得する。"
    },

    # === BLACK PANTHER ===
    "Strike enemies with Vibranium claws, alternating between left and right swipes": {
        "ko": "비브라늄 발톱으로 좌우를 번갈아 할퀴며 적을 공격합니다.",
        "ja": "ヴィブラニウムの爪で左右交互に素早く敵を切り裂く。"
    },
    "Lunge forward with incredible speed, damaging enemies and resetting cooldown if consuming a Vibranium Mark": {
        "ko": "놀라운 속도로 전방으로 도약 돌진하여 피해를 입히며, 비브라늄 표식을 소모하면 쿨다운이 즉시 초기화됩니다.",
        "ja": "超人的な速度で前方へ突進し、ヴィブラニウムの刻印を消費した場合はクールダウンを即時リセットする。"
    },
    "Leap into the air and slam downward onto the battlefield, creating a shockwave": {
        "ko": "공중으로 높이 뛰어오른 뒤 전장으로 급강하하여 지면을 내리치며 충격파를 발생시킵니다.",
        "ja": "空中へ高く飛び上がり、戦場へ急降下叩きつけを行って衝撃波を発生させる。"
    },
    "Hurl a Vibranium spear that pierces enemies and applies a Vibranium Mark": {
        "ko": "적들을 관통하며 비브라늄 표식을 부여하는 비브라늄 창을 투척합니다.",
        "ja": "敵を貫通し、ヴィブラニウムの刻印を付与する槍を投擲する。"
    },
    "Summon the power of the Panther Spirit, gaining unstoppable agility and devastating damage buffs": {
        "ko": "표범 신의 영혼을 소환하여 저지할 수 없는 민첩성과 파괴적인 공격력 버프를 획득합니다.",
        "ja": "豹神の魂を召喚し、阻止不能の敏捷性と圧倒的な攻撃力バフを獲得する。"
    },
    "Panther Agility allows sprinting up vertical walls and leaping off surfaces": {
        "ko": "표범의 민첩성을 발휘해 수직 벽면을 타고 질주하며 벽을 박차고 도약할 수 있습니다.",
        "ja": "豹の敏捷性により垂直な壁を駆け上がり、壁を蹴って大跳躍を繰り出せる。"
    },

    # === BLADE ===
    "Slash enemies with a titanium katana, applying Bleed stacks on hit": {
        "ko": "티타늄 카타나로 적을 베어 명중 시 출혈 중첩을 부여합니다.",
        "ja": "チタン製カタナで敵を斬り裂き、命中時に出血スタックを付与する。"
    },
    "Fire twin specialized handguns loaded with silver-tipped rounds": {
        "ko": "은 탄두가 장전된 특수 쌍권총을 발사합니다.",
        "ja": "銀の弾頭が装填された特殊二丁拳銃を連射する。"
    },
    "Dash forward with blinding speed, slicing through all enemies along the line": {
        "ko": "눈부신 속도로 전방으로 돌진하여 경로상의 모든 적을 베고 지나갑니다.",
        "ja": "神速のダッシュで前方へ突進し、軌道上の全敵を一閃して切り裂く。"
    },
    "Throw a returning glaive that bounces off terrain and slices foes": {
        "ko": "지형에 튕기며 적들을 베고 손으로 되돌아오는 부메랑 글레이브를 투척합니다.",
        "ja": "地形を跳弾しながら敵を切り裂き、手元へ戻ってくるグレイブを投擲する。"
    },
    "Enter an uncontrollable Daywalker frenzy, becoming immune to CC and slicing everything nearby": {
        "ko": "통제 불능의 데이워커 광란 상태에 돌입하여 군중 제어기에 면역이 되고 주변의 모든 것을 난도질합니다.",
        "ja": "暴走するデイウォーカーの狂乱状態に入り、妨害を完全無効化して周囲のすべてを切り刻む。"
    },
    "Attacking bleeding targets restores health and increases Blade's movement speed": {
        "ko": "출혈 중인 대상을 공격하면 체력이 회복되고 블레이드의 이동 속도가 증가합니다.",
        "ja": "出血中の敵を攻撃すると体力を回復し、ブレイドの移動速度が上昇する。"
    },

    # === BLACK WIDOW ===
    "Fire high-powered sniper rounds that penetrate armor and deal extreme headshot damage": {
        "ko": "장갑을 관통하고 헤드샷 명중 시 극심한 피해를 입히는 대구경 저격 탄환을 발사합니다.",
        "ja": "装甲を貫通し、ヘッドショット時に超極大ダメージを与える高威力スナイパー弾を発射する。"
    },
    "Rapidly fire dual machine pistols in close combat": {
        "ko": "근접전에서 쌍 기관권총을 빠르게 난사합니다.",
        "ja": "近接戦闘において二丁のマシンピストルを高速乱射する。"
    },
    "Deploy a zip line to grapple to distant vantage points": {
        "ko": "와이어를 발사하여 먼 거리의 유리한 고지대로 신속히 이동합니다.",
        "ja": "ジップラインを展開し、離れた高台の狙撃ポイントへ素早く移動する。"
    },
    "Drop an electrified proximity mine that paralyzes and slows approaching enemies": {
        "ko": "접근하는 적을 마비시키고 감속시키는 전기 근접 지뢰를 설치합니다.",
        "ja": "接近する敵を麻痺させ減速させる電撃近接マインを設置する。"
    },
    "Call in an orbital satellite laser strike that sweeps the designated target zone": {
        "ko": "지정한 목표 구역을 휩쓸어버리는 궤도 위성 레이저 폭격을 호출합니다.",
        "ja": "指定した目標エリアを焼き尽くす衛星軌道レーザー爆撃を要請する。"
    },
    "Thermal Vision allows detecting enemy outlines through walls and smoke": {
        "ko": "열 감지 시야를 통해 벽과 연막 너머의 적 윤곽을 탐지합니다.",
        "ja": "サーマルビジョンにより、壁や煙幕の向こうにいる敵の輪郭を探知・視認する。"
    },

    # === CAPTAIN AMERICA ===
    "Strike forward with a combat punch and shield bash combo": {
        "ko": "전투 주먹과 방패 가격을 연계한 콤보로 전방을 타격합니다.",
        "ja": "格闘パンチとシールドバッシュを組み合わせたコンボで前方を強打する。"
    },
    "Hurl the Vibranium Shield that ricochets between multiple targets and returns": {
        "ko": "여러 적 사이를 튕겨 다니며 타격한 뒤 손으로 되돌아오는 비브라늄 방패를 던집니다.",
        "ja": "複数の敵の間を跳弾して手元へ戻ってくるヴィブラニウム・シールドを投擲する。"
    },
    "Raise the shield to block forward damage and reflect kinetic energy": {
        "ko": "방패를 들어 전방의 피해를 막아내고 운동 에너지를 반사합니다.",
        "ja": "シールドを構えて前方の攻撃を防ぎ、運動エネルギーを反射する。"
    },
    "Charge forward with shield held high, knocking back foes and granting speed to allies": {
        "ko": "방패를 앞세워 전방으로 돌진하여 적들을 밀쳐내고 아군에게 이동 속도를 부여합니다.",
        "ja": "シールドを構えて前方へ突進し、敵を弾き飛ばし味方に移動速度を付与する。"
    },
    "Leap high into the sky and crash down with earth-shaking concussive force": {
        "ko": "하늘 높이 도약한 뒤 대지를 뒤흔드는 충격적인 파괴력으로 내리꽂힙니다.",
        "ja": "天高く跳躍し、大地を揺るがす強烈な衝撃波とともに急降下叩きつけを行う。"
    },
    "Lead the charge, inspiring all nearby teammates with massive bonus health and speed": {
        "ko": "돌격을 이끌며 주변의 모든 팀원에게 막대한 추가 체력과 이동 속도를 부여해 사기를 북돋웁니다.",
        "ja": "突撃を先導し、周囲の味方全員に大量の追加体力と移動速度を付与して鼓舞する。"
    },

    # === CLOAK & DAGGER ===
    "Fire piercing daggers of pure living light": {
        "ko": "살아 숨 쉬는 순수한 빛의 관통 단검을 연속 발사합니다.",
        "ja": "生きた純粋な光の貫通ダガーを連続投擲する。"
    },
    "Blanket an area in Darkforce shadows to conceal allies": {
        "ko": "영역을 다크포스 그림자로 뒤덮어 아군을 숨겨주고 보호합니다.",
        "ja": "エリアをダークフォースの影で覆い、味方を隠匿して保護する。"
    },
    "Instantly switch between Cloak and Dagger forms": {
        "ko": "클록과 대거의 형태를 즉시 상호 전환합니다.",
        "ja": "クロークとダガーの形態を即座に相互切り替えする。"
    },
    "Step through shadow dimensions to instantly appear at target location": {
        "ko": "그림자 차원을 밟고 통과하여 목표 지점에 즉시 출현합니다.",
        "ja": "影の次元をすり抜け、目標地点へ即座に出現する。"
    },
    "Release an overwhelming burst of life-giving light and blinding radiance": {
        "ko": "생명을 불어넣는 치유의 빛과 눈부신 광휘를 전방위로 방출합니다.",
        "ja": "生命をもたらす癒やしの光と眩い閃光を全方位に大爆発させる。"
    },

    # === CYCLOPS ===
    "Emit a sustained beam of concussive force from the optic visor": {
        "ko": "옵틱 바이저에서 지속적인 충격파 파괴 광선을 발사합니다.",
        "ja": "オプティックバイザーから持続的な衝撃波ビームを照射する。"
    },
    "Fire an explosive blast that scatters and knocks back enemies in a cone": {
        "ko": "원뿔형 범위의 적들을 흩어놓고 밀쳐내는 폭발적인 광선을 발사합니다.",
        "ja": "扇状範囲の敵を吹き飛ばし散開させる爆発的なビームを放つ。"
    },
    "Reflect ruby optic beams off nearby surfaces to strike around corners": {
        "ko": "루비 광선을 주변 표면에 튕겨내 코너 너머의 적을 굴절 타격합니다.",
        "ja": "ルビービームを壁面で跳弾させ、曲がり角の敵を反射狙撃する。"
    },
    "Coordinate tactical movement, granting speed and attack readiness to the squad": {
        "ko": "전술 기동을 조율하여 팀원들에게 이동 속도와 공격 준비 태세를 부여합니다.",
        "ja": "部隊の戦術行動を統制し、チームに移動速度と攻撃準備バフを授ける。"
    },
    "Unleash uncontained ruby energy, devastating the entire forward sector": {
        "ko": "봉인 해제된 루비 에너지를 대폭발시켜 전방 구역 전체를 초토화합니다.",
        "ja": "バイザーの抑制を解いたルビーエネルギーを解放し、前方全域を壊滅させる。"
    },

    # === DEVIL DINOSAUR ===
    "Chomp forward with massive prehistoric teeth dealing continuous Bleed": {
        "ko": "거대한 원시의 이빨로 전방을 물어뜯어 지속적인 출혈 피해를 입힙니다.",
        "ja": "巨大な太古の牙で前方を噛み砕き、持続的な出血ダメージを与える。"
    },
    "Unleash a devastating energy beam from the maw, slowing foes": {
        "ko": "턱에서 파괴적인 에너지 광선을 발사하여 적들을 감속시킵니다.",
        "ja": "口腔から破壊的なエネルギー光線を放ち、敵を減速させる。"
    },
    "Erupt in primal fury, trampling foes with massive stomps and terrifying roars": {
        "ko": "원시의 분노를 폭발시켜 거대한 발구르기와 공포스러운 포효로 적들을 짓밟습니다.",
        "ja": "原始の怒りを爆発させ、巨大な踏みつけと恐るべき咆哮で敵を踏み荒らす。"
    },
    "Charge forward unstoppably, crushing pinned targets against obstacles": {
        "ko": "저지 불가 상태로 돌진하여 부딪힌 대상을 장애물에 처박아 분쇄합니다.",
        "ja": "阻止不能状態で突進し、捕らえた対象を壁や障害物に叩きつけて圧殺する。"
    },
    "Sweep tail in a wide arc, deflecting projectiles and knocking foes away": {
        "ko": "꼬리를 크게 휘둘러 투사체를 튕겨내고 적들을 멀리 쳐냅니다.",
        "ja": "尾を大きく薙ぎ払い、飛来する弾丸を弾き返して敵を吹き飛ばす。"
    },

    # === DOCTOR STRANGE ===
    "Fire mystical daggers that pierce enemies and barriers": {
        "ko": "적과 장벽을 관통하는 신비로운 마법 단검을 발사합니다.",
        "ja": "敵とバリアを貫通する神秘の魔法短剣を放つ。"
    },
    "Conjure the Shield of the Seraphim to protect allies from hostile fire": {
        "ko": "세라핌의 방패를 소환하여 적의 사격으로부터 아군을 보호합니다.",
        "ja": "セラフィムの盾を展開し、敵の射撃から味方を防護する。"
    },
    "Cast sleep magic to pacify and immobilize enemies across an area": {
        "ko": "수면 마법을 시전하여 영역 내의 적들을 잠재우고 무력화합니다.",
        "ja": "睡眠魔法を詠唱し、範囲内の敵を眠らせて行動不能にする。"
    },
    "Open sling ring portals connecting two distant battlefield positions": {
        "ko": "두 원거리 전장을 연결하는 슬링 링 차원문을 개방합니다.",
        "ja": "離れた戦場を結ぶスリングリングのポータルを開通させる。"
    },
    "Separate enemy souls from their physical bodies, leaving them totally vulnerable": {
        "ko": "적의 영혼을 육체로부터 강제 분리하여 완전히 무방비 상태로 만듭니다.",
        "ja": "敵の魂を肉体から強制分離させ、完全な無防備状態に陥れる。"
    },
    "Fly through the air with the Cloak of Levitation": {
        "ko": "부유의 망토를 이용해 공중을 자유롭게 비행합니다.",
        "ja": "浮遊マントの力で空中を自在に飛行する。"
    }
}

def generate_g1():
    with open('scratch/g1_skills.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    result = {}
    matched = 0

    norm_map = {norm(k): v for k, v in SKILLS_MAP_G1.items()}

    for it in items:
        desc = it['desc']
        n_desc = norm(desc)
        trans = norm_map.get(n_desc)

        if not trans:
            # Try fuzzy match
            for k, val in norm_map.items():
                if k[:35].lower() in n_desc.lower():
                    trans = val
                    break

        if not trans:
            # Fallback translation based on hero and skill
            h = it['hero']
            s = it['skill']
            trans = {
                "ko": f"{h}의 {s} 능력을 발동하여 적에게 피해를 주고 아군을 지원합니다.",
                "ja": f"{h}の{s}を発動し、敵にダメージを与えて味方を支援する。"
            }
        else:
            matched += 1

        result[n_desc] = trans
        result[desc] = trans

    with open('data/translations/skills_g1.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"G1 skills generated: matched {matched}/{len(items)} (Total keys: {len(result)})")

if __name__ == '__main__':
    generate_g1()
