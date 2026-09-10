# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Vanguard Skills Translations Builder
Maps all 144 Vanguard skill descriptions to natural, authentic Korean (KR) and Japanese (JP).
"""

import json
import re
import os

VANGUARD_DICT = {
    # === ANGELA ===
    "Lunge forward with your spear, dealing damage that increases with Attack Charge. At full charge, Spear of Ichor can launch up enemies": {
        "ko": "창을 전방으로 찔러 공격 게이지(Attack Charge)에 비례한 피해를 입힙니다. 게이지가 가득 차면 적을 공중으로 띄웁니다.",
        "ja": "槍を前方に突き出して攻撃チャージに応じたダメージを与える。最大チャージ時は敵を打ち上げる。"
    },
    "Alternate powerful strikes forward with twin axes, dealing increased damage as Attack Charge grows. The fourth strike propels you forward in a swift dash": {
        "ko": "쌍도끼로 번갈아 강력한 전방 타격을 가하며 공격 게이지에 따라 피해량이 증가합니다. 네 번째 타격 시 전방으로 신속하게 돌진합니다.",
        "ja": "双斧による強力な交互連撃を繰り出し、攻撃チャージに応じてダメージが上昇する。4打目に高速ダッシュで前方へ突進する。"
    },
    "Transform Ichors into a shield, gaining Attack Charge when absorbing damage": {
        "ko": "이코르(Ichor)를 방패 형태로 변환하여 피해를 흡수하며, 피해 흡수 시 공격 게이지를 획득합니다.",
        "ja": "イコルを盾に変形させてダメージを吸収し、攻撃チャージを獲得する。"
    },
    "Wrap your spear in ribbons and hurl it with force. Upon impact, the ribbons bind nearby enemies. Angela can leap to the spear's location, damaging surrounding enemies and creating a Divine Judgement Zone": {
        "ko": "창에 리본을 감아 강력하게 투척합니다. 착탄 시 리본이 주변 적들을 결박하며, 안젤라는 창 위치로 도약하여 주변에 피해를 주고 신성한 심판 영역을 생성합니다.",
        "ja": "槍にリボンを巻き付けて力強く投擲する。着弾時に周囲の敵を拘束し、アンジェラは槍の位置へ跳躍して範囲ダメージを与え、神聖なる審判エリアを生成する。"
    },
    "Enter an accelerated dash state, \xa0enemies struck head-on are carried through the air for a short distance": {
        "ko": "가속 돌진 상태에 돌입하여 정면으로 충돌한 적을 잠시 공중으로 끌고 날아갑니다.",
        "ja": "加速ダッシュ状態に突入し、正面衝突した敵を短距離空中へ巻き込んで運ぶ。"
    },
    "Dive downward, switch to twin axes and infuse the ground with Ichors to create a Divine Judgement Zone": {
        "ko": "아래로 급강하하여 쌍도끼로 전환하고 지면에 이코르를 주입하여 신성한 심판 영역을 생성합니다.",
        "ja": "急降下して双斧に切り替え、地面にイコルを注入して神聖なる審判エリアを展開する。"
    },
    "Take to the skies, switching back to Spear of Ichors": {
        "ko": "하늘로 치솟아 오르며 이코르의 창으로 다시 전환합니다.",
        "ja": "上空へ飛び上がり、再びイコルの槍へと切り替える。"
    },
    "Glide freely through the air. Continuous flight builds Attack Charge": {
        "ko": "공중을 자유롭게 활공합니다. 비행을 지속할수록 공격 게이지가 서서히 충전됩니다.",
        "ja": "空中を自在に滑空する。滑空を維持することで攻撃チャージが徐々に蓄積される。"
    },
    "Angela shares fragments of her Ichors with Thor, empowering him to hurl a Thunder Spear that strikes through enemies": {
        "ko": "안젤라가 토르에게 이코르 파편을 공유하여 적들을 꿰뚫는 번개의 창을 투척할 수 있게 강화합니다.",
        "ja": "アンジェラがソーにイコルの破片を分け与え、敵を貫く雷の槍を投擲できるように強化する。"
    },

    # === CAPTAIN AMERICA ===
    "Get up close to strike enemies. Landing the second hit enables a shield throw that bounces between foes": {
        "ko": "적에게 접근하여 타격합니다. 2타 명중 시 적들 사이를 튕겨 다니는 방패 던지기가 활성화됩니다.",
        "ja": "敵に接近して打撃を与える。2打目を命中させると、敵間を跳弾するシールド投擲が可能になる。"
    },
    "Slam down from the sky onto the targeted area, Launching Up enemies": {
        "ko": "공중에서 목표 구역으로 급강하 강타하여 적들을 공중에 띄웁니다.",
        "ja": "上空から目標地点へ急降下叩きつけを行い、敵を打ち上げる。"
    },
    "Raise the shield to deflect incoming projectiles, sending them ricocheting in random directions and generating Bonus Health on successful blocks": {
        "ko": "방패를 들어 날아오는 투사체를 튕겨내 무작위 방향으로 반사시키며, 방어 성공 시 추가 체력을 생성합니다.",
        "ja": "シールドを構えて飛来する弾丸を弾き返し、防御成功時に追加体力を生成する。"
    },
    "Shield held high, carve a path forward, granting both himself and allies along the path a Movement Boost, as well as granting himself Bonus Health": {
        "ko": "방패를 높이 들고 전방으로 돌진하여 자신과 경로상의 아군에게 이동 속도 증가를 부여하고 자신은 추가 체력을 얻습니다.",
        "ja": "シールドを高く掲げて前方へ突進し、自身と進路上の味方に移動速度上昇を付与し、自身は追加体力を獲得する。"
    },
    "Boost speed and enable Fearless Leap to leap into the air": {
        "ko": "이동 속도를 높이고 용맹한 도약(Fearless Leap)을 활성화하여 공중으로 높이 뛰어오릅니다.",
        "ja": "移動速度を上昇させ、勇敢なる跳躍で空中へ高く飛び上がる。"
    },
    "Hurl the energy-charged shield to strike enemies in a path": {
        "ko": "에너지가 충전된 방패를 던져 경로상의 적들을 강타합니다.",
        "ja": "エネルギーが充填されたシールドを投擲し、進路上の敵を一撃する。"
    },
    "Raise the shield and charge forward": {
        "ko": "방패를 들고 전방으로 신속하게 돌진합니다.",
        "ja": "シールドを構えて前方へ突進する。"
    },
    "Black Cat shares her luck with her allies. When White Fox embraces her newfound luck, she gains a full heal and maximum energy": {
        "ko": "블랙 캣이 아군과 행운을 공유합니다. 화이트 폭스가 행운을 받으면 체력이 완전히 회복되고 에너지가 최대치로 충전됩니다.",
        "ja": "ブラックキャットが味方に幸運を分ける。ホワイト・フォックスが幸運を得ると、体力が全回復しエネルギーが最大になる。"
    },
    "Inspired by Captain America's resolve, Winter Soldier can leap to the aid of a damaged ally, knocking back enemies in the area": {
        "ko": "캡틴 아메리카의 결의에 고무되어, 윈터 솔져가 피해를 입은 아군 위치로 도약해 주변 적들을 밀쳐냅니다.",
        "ja": "キャプテン・アメリカの覚悟に鼓舞され、ウィンター・ソルジャーが被弾した味方へ跳躍救援し、周囲の敵を弾き飛ばす。"
    },

    # === DEADPOOL (VANGUARD) ===
    "Nobody lays a finger on my teammates! Anyone tries, and I'm firing these big boys to blast them into next week!": {
        "ko": "내 팀원한테 손가락 하나라도 대봐! 손대는 놈은 이 무식하게 큰 총으로 다음 주까지 날려버릴 테니까!",
        "ja": "ウチのチームメイトに指一本触れさせねえぞ！手を出した奴はこのデカい銃で来週までぶっ飛ばしてやる！"
    },
    "Protecting my team means my katanas go full savage. No mercy for the baddies!": {
        "ko": "팀을 지키기 위해서라면 내 카타나는 완전 인정사정없지. 악당 놈들에게 자비란 없다!",
        "ja": "仲間を守るためなら俺の刀は容赦しねえ！悪党どもに慈悲なんてねえんだよ！"
    },
    "Plushie power! It stops every single attack those chumps throw, giving my team a safe zone. When things get sticky, it's unicorn time!": {
        "ko": "인형 파워! 멍청이들이 날리는 공격을 몽땅 막아내서 우리 팀에게 안전지대를 만들어주지. 골치 아플 땐 유니콘이 최고야!",
        "ja": "ぬいぐるみパワー！雑魚どもの攻撃を全部防いで味方に安全地帯を作るぜ。ピンチの時はユニコーンにお任せ！"
    },
    "Try getting to my teammates, I dare you! My dash slash knocks fools down, and if they keep pestering, they get a slice of my explosive pie!": {
        "ko": "우리 팀한테 다가와 봐, 어디 한번! 돌진 베기로 멍청이들을 넘어뜨리고, 그래도 깐족대면 내 폭탄 파이 맛을 보여주마!",
        "ja": "ウチの仲間を狙ってみろ、返り討ちだ！突進斬りでノックダウンさせて、まだしつこいなら爆破パイをお見舞いしてやるぜ！"
    },
    "You! Yeah, you - the hyper one! Eyes off my friends. I sentence you to...whatever this hammer does!": {
        "ko": "너! 그래 너, 거기 설쳐대는 놈! 내 친구들한테서 눈 떼라. 널... 이 망치가 하는 무언가에 처형한다!",
        "ja": "そこのお前！そう、調子乗ってるお前だ！仲間に手を出すな。このハンマーの刑に処してやる！"
    },
    "Wake the #!&% up, hero! We've got a game to win! Speed and healing buffs for star players like us!": {
        "ko": "정신 #!&% 차려, 히어로! 이겨야 할 판이라고! 우리 같은 특급 스타 플레이어를 위한 이속과 힐 버프 들어간다!",
        "ja": "おい起きろや#!&%ヒーロー！試合に勝つぞ！俺たちスタープレイヤーに移動速度と回復バフのプレゼントだ！"
    },
    "Want to hurt my team? Good luck! I hit you with a taunt, mess up your vision, and take all the glory. My friends stay safe, and I look amazing!": {
        "ko": "우리 팀을 치겠다고? 어림없지! 도발을 걸고, 시야를 어지럽히고, 스포트라이트는 내가 다 받는다! 내 친구들은 안전하고 난 멋있지!",
        "ja": "仲間を傷つけたい？無理無理！挑発で視界を狂わせて、栄光は全部俺がいただくぜ。仲間は無傷、俺は最高にクール！"
    },
    "I'm here to smack baddies, get XP, and shield my friends! When my XP is full, I level up and gain insane upgrade effects. Talk about a pro gamer move!": {
        "ko": "악당을 패고, 경험치를 쌓고, 친구들을 지킨다! 경험치가 다 차면 레벨업해서 정신 나간 강화 효과를 얻지. 이게 바로 프로게이머 무빙이다!",
        "ja": "悪党をブチのめし、経験値を稼いで仲間を守る！ゲージが満タンになったらレベルアップしてヤバい強化効果ゲットだぜ。プロゲーマーの動きだな！"
    },
    "Yup, I can double jump in midair! During The Big Test and its upgrade, I can also super leap and glide! Mobility for the win!": {
        "ko": "맞아, 나 공중 2단 점프 된다! '더 빅 테스트'랑 그 업그레이드 중엔 슈퍼 점프에 활공까지 가능하지! 기동성이 최고야!",
        "ja": "そう、空中で2段ジャンプできるんだぜ！『ザ・ビッグテスト』とその強化中はスーパージャンプと滑空も可能！機動性最強！"
    },
    "Out of combat? I'm healing up, staying battle-ready to protect my team. And if I take too much damage, I can cheat death once!": {
        "ko": "전투가 끝났다고? 체력 채우면서 팀을 지킬 전투 태세를 유지하지. 그리고 피해를 너무 많이 받으면 한 번쯤 죽음을 속여넘길 수도 있다고!",
        "ja": "非戦闘中？体力を回復して仲間を守る臨戦態勢をキープだ。ダメージを受けすぎても、1回だけ死を回避できるんだぜ！"
    },
    "Listen up, eyes on the prize, don't wander off! Every time my abilities land on enemies, they get taunted, keeping my team safe from their attacks!": {
        "ko": "잘 들어, 승리에 집중하고 한눈팔지 마! 내 스킬이 적에게 맞을 때마다 놈들을 도발해서 우리 팀을 공격하지 못하게 막아주지!",
        "ja": "よく聞け、勝利を見据えて余所見するな！俺のスキルが当たるたびに敵を挑発し、仲間を攻撃から守るんだ！"
    },
    "Deadpool hands Jeff the Land Shark a plushie with attitude. Jeff can spit it ahead, causing a distraction with continuous sound and visuals": {
        "ko": "데드풀이 제프 더 랜드 샤크에게 건방진 인형을 건넵니다. 제프가 인형을 앞으로 뱉으면 요란한 소리와 시각 효과로 적들의 주의를 분산시킵니다.",
        "ja": "デッドプールがジェフに生意気なぬいぐるみを渡す。ジェフが前方へ吐き出すと、騒音と派手なエフェクトで敵の注意を引きつける。"
    },

    # === DEVIL DINOSAUR ===
    "Snap with massive prehistoric jaws to crush enemies in close combat": {
        "ko": "거대한 원시의 턱으로 적을 물어뜯어 강력한 근접 피해를 입힙니다.",
        "ja": "巨大な原始の顎で敵に噛みつき、強力な近接ダメージを与える。"
    },
    "Sweep tail in a wide horizontal arc to damage and knock away surrounding enemies": {
        "ko": "꼬리를 넓은 수평 궤적으로 휘둘러 주변 적들에게 피해를 입히고 멀리 쳐냅니다.",
        "ja": "尾を水平に大きく薙ぎ払い、周囲の敵にダメージを与えて弾き飛ばす。"
    },
    "Emit a primal roar that terrifies nearby foes, reducing their damage and movement speed": {
        "ko": "원시의 포효를 내질러 주변 적들을 공포에 질리게 하고, 공격력과 이동 속도를 감소시킵니다.",
        "ja": "原始の咆哮を放ち、周囲の敵を威圧して与ダメージと移動速度を低下させる。"
    },
    "Stomp down with immense weight, creating shockwaves that slow and damage enemies": {
        "ko": "엄청난 무게로 지면을 강타하여 충격파를 일으키고 적들을 감속시키며 피해를 줍니다.",
        "ja": "強大な重量で地を踏み鳴らし、衝撃波で敵にダメージと鈍足効果を与える。"
    },
    "Rampage forward uncontrollably, crushing obstacles and carrying pinned enemies along the charge": {
        "ko": "제어할 수 없는 분노로 돌진하여 장애물을 부수고 정면의 적들을 들이받아 함께 끌고 갑니다.",
        "ja": "猛烈な勢いで暴走突進し、進路上の障害物を粉砕して接触した敵を巻き込み突進する。"
    },
    "Thick prehistoric scales provide natural armor, reducing incoming damage from all sources": {
        "ko": "두터운 원시 비늘이 단단한 방어력을 제공하여 모든 유형의 받는 피해를 줄여줍니다.",
        "ja": "分厚い太古の鱗が装甲となり、あらゆる受けるダメージを軽減する。"
    },

    # === DOCTOR STRANGE ===
    "Fire daggers of mystical energy that pierce through enemies": {
        "ko": "적을 관통하는 신비로운 마법 단검 투사체를 연속 발사합니다.",
        "ja": "敵を貫通する神秘のエネルギー短剣を連続発射する。"
    },
    "Conjure a mystical barrier of protective light to block incoming hostile fire": {
        "ko": "보호의 빛으로 이루어진 마법 장벽을 소환하여 전방의 적 공격을 막아냅니다.",
        "ja": "防護の光による魔法の障壁を展開し、敵の射撃攻撃を遮断する。"
    },
    "Cast sleep magic across a target area, putting enemies into a deep slumber": {
        "ko": "목표 구역에 수면 마법을 시전하여 영역 내의 적들을 깊은 잠에 빠뜨립니다.",
        "ja": "目標エリアに睡眠魔法を放ち、範囲内の敵を深い眠りに落とし込む。"
    },
    "Open dual portals, allowing allies and friendly projectiles to instantly teleport across space": {
        "ko": "두 개의 차원문을 열어 아군과 아군 투사체가 공간을 넘어 즉시 순간이동할 수 있게 합니다.",
        "ja": "2つのポータルを開き、味方や弾丸を空間を超えて即座にテレポートさせる。"
    },
    "Separate souls from physical bodies in a wide radius, rendering foes helpless and vulnerable": {
        "ko": "넓은 반경 내 적들의 영혼을 육체에서 분리시켜 무방비 상태로 만들고 받는 피해를 극대화합니다.",
        "ja": "広範囲の敵の魂を肉体から引き離し、無防備にして被ダメージを増大させる。"
    },
    "Levitate effortlessly through the air with the Cloak of Levitation": {
        "ko": "부유의 망토를 착용하여 공중을 부드럽게 날아다닙니다.",
        "ja": "浮遊マントの魔力により、空中を軽やかに浮遊飛行する。"
    },

    # === EMMA FROST ===
    "Fire concentrated psionic beams from fingertips that pierce and damage foes": {
        "ko": "손끝에서 응축된 사이킥 광선을 발사하여 적을 관통하고 피해를 줍니다.",
        "ja": "指先から凝縮されたサイキックビームを発射し、敵を貫通してダメージを与える。"
    },
    "Shift into organic diamond form, gaining complete crowd control immunity and high physical resistance": {
        "ko": "유기농 다이아몬드 형태로 전환하여 모든 군중 제어 효과에 면역이 되고 높은 물리 저항력을 얻습니다.",
        "ja": "有機ダイヤモンド形態へと変化し、全行動妨害を完全無効化して高い物理耐性を獲得する。"
    },
    "Unleash a diamond backfist strike that breaks through enemy shields": {
        "ko": "다이아몬드 주먹으로 백너클을 날려 적의 방어막을 깨부수고 타격을 입힙니다.",
        "ja": "ダイヤモンドの拳で強烈なバックハンドを放ち、敵のシールドを打ち砕く。"
    },
    "Project a diamond defensive barrier to shield allies behind Emma": {
        "ko": "다이아몬드 방어 장벽을 투사하여 엠마의 뒤에 있는 아군들을 보호합니다.",
        "ja": "ダイヤモンドの防御障壁を展開し、自身の後方にいる味方を守る。"
    },
    "Release a devastating psionic blast that confuses enemies and disrupts their controls": {
        "ko": "치명적인 사이킥 폭풍을 방출하여 적들을 혼란에 빠뜨리고 조작을 방해합니다.",
        "ja": "壊滅的なサイキックブラストを放ち、敵を混乱させて操作を妨害する。"
    },

    # === GROOT ===
    "Strike forward with heavy wooden fists dealing solid physical damage": {
        "ko": "묵직한 나무 주먹으로 전방을 가격하여 물리 피해를 입힙니다.",
        "ja": "重厚な木の拳で前方を強打し、物理ダメージを与える。"
    },
    "Erect a massive wooden barrier from the earth to deny enemy passage and absorb fire": {
        "ko": "지면에서 거대한 목재 장벽을 솟아오르게 하여 적의 통행을 차단하고 사격을 흡수합니다.",
        "ja": "地面から巨大な木の壁を隆起させ、敵の進入を阻んで射撃を吸収する。"
    },
    "Extend creeping roots forward to ensnare and pull targets toward Groot": {
        "ko": "전방으로 뻗어나가는 뿌리를 발사해 적을 옭아매고 그루트 앞으로 끌어당깁니다.",
        "ja": "前方へ根を伸ばして敵を捕らえ、グルートの目の前へと引き寄せる。"
    },
    "Form a wooden fortress around nearby allies to grant continuous shielding": {
        "ko": "주변 아군들을 감싸는 나무 요새를 형성하여 지속적인 보호막을 부여합니다.",
        "ja": "周囲の味方を包み込む木の要塞を形成し、継続シールドを付与する。"
    },
    "Unleash a massive tangle of briars that roots and constricts all enemies within": {
        "ko": "거대한 가시덤불을 방출하여 영역 내의 모든 적을 속박하고 압박 피해를 줍니다.",
        "ja": "巨大な茨の繁茂を放ち、範囲内の敵全員を拘束して締め付けダメージを与える。"
    },

    # === HULK ===
    "Slam fists into enemies with unstoppable raw strength": {
        "ko": "멈출 수 없는 순수한 힘으로 주먹을 휘둘러 적들을 강타합니다.",
        "ja": "止められない圧倒的な力で拳を振り下ろし、敵を殴り倒す。"
    },
    "Clap hands with thunderous force, unleashing a concussive blast ahead": {
        "ko": "두 손을 천둥처럼 강하게 마주쳐 전방으로 강력한 충격파를 발사합니다.",
        "ja": "両手を雷鳴のごとく激しく打ち合わせ、前方へ衝撃波を放つ。"
    },
    "Leap across vast distances and slam into target areas with immense force": {
        "ko": "먼 거리를 단숨에 도약하여 목표 구역으로 거대하게 내리꽂힙니다.",
        "ja": "長距離を一気に跳躍し、強大な質量で目標地点へ突撃着地する。"
    },
    "Seize an enemy and smash them relentlessly against the terrain": {
        "ko": "적 하나를 움켜쥐고 지면에 사정없이 패대기칩니다.",
        "ja": "敵を一人掴み上げ、地面に何度も叩きつけて粉砕する。"
    },
    "Ascend into World Breaker form, gaining immense durability, size, and power": {
        "ko": "월드 브레이커 형태로 각성하여 압도적인 체력, 거대한 체격, 파괴력을 얻습니다.",
        "ja": "ワールド・ブレイカー形態へと覚醒し、圧倒的な耐久力、巨大な体躯、破壊力を獲得する。"
    },
    "Hulk accumulates rage upon taking damage, empowering his physical abilities": {
        "ko": "헐크는 피해를 입을 때마다 분노를 축적하여 신체 능력을 더욱 강화합니다.",
        "ja": "ハルクはダメージを受けるほど怒りを蓄積し、肉体能力を強化していく。"
    },
    "Fire a ray gun that deals moderate energy damage (Banner form)": {
        "ko": "광선총을 발사하여 에너지 피해를 입힙니다 (배너 형태).",
        "ja": "光線銃を発射してエネルギーダメージを与える (バナー形態)。"
    },
    "Toss a gamma bomb that explodes upon impact (Banner form)": {
        "ko": "착탄 시 폭발하는 감마 폭탄을 투척합니다 (배너 형태).",
        "ja": "着弾時に爆発するガンマ爆弾を投擲する (バナー形態)。"
    },
    "Transform into the Incredible Hulk upon reaching full gamma charge (Banner form)": {
        "ko": "감마 에너지가 가득 차면 인크레더블 헐크로 변신합니다 (배너 형태).",
        "ja": "ガンマゲージが満タンになるとインクレディブル・ハルクへと変身する (バナー形態)。"
    },

    # === MAGNETO ===
    "Fire magnetized metal shards that deal damage to targets": {
        "ko": "자화된 금속 파편을 발사하여 목표에게 피해를 입힙니다.",
        "ja": "磁化された金属破片を発射し、対象にダメージを与える。"
    },
    "Erect a massive electromagnetic shield to deflect enemy projectiles": {
        "ko": "거대한 전자기 방패를 세워 날아오는 적 투사체를 막아냅니다.",
        "ja": "巨大な電磁シールドを展開し、敵の飛来弾を遮断する。"
    },
    "Wrap an ally or himself in a magnetic sphere that absorbs incoming damage": {
        "ko": "아군이나 자신을 구형 자기장으로 감싸 들어오는 모든 피해를 흡수합니다.",
        "ja": "味方または自身を球状の磁気バリアで包み、被ダメージを吸収する。"
    },
    "Condense environmental metal into a colossal meteor and crush the target zone": {
        "ko": "주변의 금속을 압축해 거대한 운석을 형성한 뒤 목표 구역을 분쇄합니다.",
        "ja": "周囲の金属を凝縮して巨大隕石を形成し、目標エリアを押し潰す。"
    },
    "Levitate effortlessly through manipulation of local magnetic fields": {
        "ko": "주변 자기장을 조작하여 공중에 부유하고 부드럽게 활공합니다.",
        "ja": "局所磁場を操り、空中を自在に浮遊・滑空する。"
    },

    # === PENI PARKER ===
    "Fire twin cyber-web shots from SP//dr suit to damage and slow enemies": {
        "ko": "SP//dr 슈트에서 사이버 거미줄을 발사하여 피해를 주고 적을 감속시킵니다.",
        "ja": "SP//drスーツから電脳蜘蛛の糸を連射し、敵にダメージと鈍足効果を与える。"
    },
    "Deploy autonomous arachno-mines that track approaching hostile units": {
        "ko": "접근하는 적을 자동으로 추적하는 자율 거미 지뢰를 설치합니다.",
        "ja": "接近する敵を自動追尾する自律型スパイダーマインを設置する。"
    },
    "Fire a tether line to rapidly pull the SP//dr suit toward terrain": {
        "ko": "와이어를 발사하여 지형지물 쪽으로 SP//dr 슈트를 빠르게 견인합니다.",
        "ja": "ワイヤーを射出して地形へSP//drスーツを高速牽引する。"
    },
    "Set up a cyber-web field that immobilizes enemies and repairs SP//dr": {
        "ko": "사이버 웹 장판을 설치하여 적을 구속하고 SP//dr의 체력을 지속 수리합니다.",
        "ja": "電脳ネット領域を展開し、侵入した敵を拘束しつつSP//drを修復する。"
    },
    "Overclock SP//dr, launching an overwhelming barrage of cybernetic webs": {
        "ko": "SP//dr을 오버클럭하여 전장에 압도적인 사이버 거미줄 폭풍을 퍼붓습니다.",
        "ja": "SP//drをオーバークロックし、圧倒的な電脳ウェブの嵐を戦場に展開する。"
    },

    # === ROGUE ===
    "Strike with supercharged physical strength, dealing high damage in close range": {
        "ko": "초인적인 완력으로 주먹을 날려 근접 범위의 적에게 높은 피해를 입힙니다.",
        "ja": "超人的な腕力で拳を叩き込み、近距離の敵に大ダメージを与える。"
    },
    "Drain life force and steal abilities through skin-to-skin touch": {
        "ko": "적과의 직접 접촉을 통해 생명력을 흡수하고 대상의 핵심 스킬을 복제합니다.",
        "ja": "素肌での接触により生命力を吸収し、対象の主要スキルを奪い取る。"
    },
    "Dash forward swiftly in flight, crashing into enemy frontlines": {
        "ko": "비행 추진력으로 전방으로 급돌진하여 적의 전선에 들이받습니다.",
        "ja": "飛行速度を活かして前方へ高速突進し、敵の前線へ突撃する。"
    },
    "Absorb all incoming attacks in an impervious defensive stance": {
        "ko": "난공불락의 방어 자세를 취해 들어오는 모든 공격을 흡수합니다.",
        "ja": "鉄壁の防御体勢を構え、受ける全攻撃を吸収する。"
    },
    "Release absorbed kinetic and psionic energies in a catastrophic burst": {
        "ko": "흡수한 모든 운동 에너지와 초능력을 파괴적인 파동으로 일거에 방출합니다.",
        "ja": "吸収したすべての運動・精神エネルギーを一気に破滅的爆発として解放する。"
    },

    # === THE THING ===
    "Throw heavy rocky punches that stagger and damage enemies": {
        "ko": "묵직한 바위 주먹을 내질러 적을 비틀거리게 만들고 피해를 입힙니다.",
        "ja": "重厚な岩石パンチを放ち、敵を怯ませてダメージを与える。"
    },
    "Excavate a giant rock from the terrain and hurl it at foes": {
        "ko": "지면에서 거대한 암석을 뜯어내 적을 향해 강력하게 집어던집니다.",
        "ja": "地面から巨大な岩塊を引き抜き、敵陣へ力任せに投げつける。"
    },
    "Charge forward unstoppably, knocking aside all obstacles and enemies": {
        "ko": "저지 불가 상태로 전방으로 돌진하여 경로상의 모든 적을 옆으로 쳐냅니다.",
        "ja": "阻止不能状態で猛進し、進路上の障害物と敵をすべて弾き飛ばす。"
    },
    "Execute the iconic ground slam, creating a violent earthquake that knocks foes airborne": {
        "ko": "상징적인 지면 강타를 작렬시켜 거대한 지진을 일으키고 적들을 공중에 띄웁니다.",
        "ja": "象徴的な地面叩きつけを炸裂させ、激震で敵全員を宙へ打ち上げる。"
    },
    "Thick rocky hide provides innate damage resistance against all physical harm": {
        "ko": "두터운 암석 외피가 상시 물리 저항력을 부여하여 받는 피해를 감소시킵니다.",
        "ja": "分厚い岩石の表皮が常時物理耐性を付与し、被ダメージを軽減する。"
    },

    # === THOR ===
    "Swing Mjolnir to strike enemies, or throw it to damage foes and return": {
        "ko": "묠니르를 휘둘러 적을 가격하거나 전방으로 던져 적을 치고 손으로 회수합니다.",
        "ja": "ムジョルニアを振り回して敵を叩き、または投擲して敵を攻撃して手元へ戻す。"
    },
    "Call down divine lightning from the heavens to strike surrounding foes": {
        "ko": "하늘에서 신성한 벼락을 소환하여 주변의 적들을 내리칩니다.",
        "ja": "天から神聖な雷霆を呼び寄せ、周囲の敵を撃ち抜く。"
    },
    "Supercharge all attacks with crackling godly electricity": {
        "ko": "몸에 번쩍이는 신의 번개를 둘러 모든 공격을 전격 속성으로 강화합니다.",
        "ja": "全身に神の雷撃を纏い、すべての攻撃を電撃属性へと超強化する。"
    },
    "Spin Mjolnir at high speed to fly forward across the skies": {
        "ko": "묠니르를 고속 회전시켜 추진력을 얻어 하늘을 가로질러 날아갑니다.",
        "ja": "ムジョルニアを高速回転させて推進力を生み出し、空を飛翔する。"
    },
    "Leap into the storm clouds and slam down with god-level thunderous fury": {
        "ko": "폭풍우 구름 속으로 솟구친 뒤 신의 분노가 담긴 거대한 벼락과 함께 지면을 강타합니다.",
        "ja": "嵐の雲へと舞い上がり、神の怒りを込めた大雷霆とともに地面へ急降下叩きつけを行う。"
    },

    # === THE HOOD ===
    "Fire dual demonic pistols infused with dark hellfire": {
        "ko": "암흑 지옥불이 깃든 쌍권총을 발사하여 화염 피해를 입힙니다.",
        "ja": "暗黒の地獄炎が宿る二丁拳銃を乱射し、火炎ダメージを与える。"
    },
    "Activate the demon cloak to turn invisible and gain a burst of speed": {
        "ko": "악마의 망토를 발동하여 투명화 상태가 되고 폭발적인 이동 속도를 얻습니다.",
        "ja": "悪魔のマントを発動して透明化し、爆発的な移動速度を獲得する。"
    },
    "Release a flock of hellfire bats that burn and disorient targets": {
        "ko": "적을 불태우고 시야를 방해하는 지옥박쥐 무리를 방출합니다.",
        "ja": "敵を炎上させ視界を狂わせる地獄コウモリの群れを解き放つ。"
    },
    "Channel dark magic to levitate above the battlefield": {
        "ko": "암흑 마법을 집중하여 전장 상공에 떠올라 사격합니다.",
        "ja": "暗黒魔法を集中させ、戦場の上空に浮遊して狙撃する。"
    },
    "Transform into a terrifying demonic avatar, raining destruction across the area": {
        "ko": "공포스러운 악마의 화신으로 변신하여 전역에 파멸의 불길을 퍼붓습니다.",
        "ja": "恐るべき悪魔の化身へと変貌し、範囲全域に破滅の炎の雨を降らせる。"
    },

    # === VENOM ===
    "Slash and whip with symbiotic tentacles in brutal melee combat": {
        "ko": "잔혹한 심비오트 촉수로 전방을 채찍질하고 베어 근접 피해를 줍니다.",
        "ja": "凶暴なシンビオートの触手で薙ぎ払いと切り裂きを行い、近接ダメージを与える。"
    },
    "Fire a tendril line to web-swing with massive momentum": {
        "ko": "촉수 줄을 쏘아 거대한 탄성을 이용해 웹 스윙으로 고속 이동합니다.",
        "ja": "触手ラインを射出し、強大な運動量でウェブスイング滑空する。"
    },
    "Dive down from midair, slamming into the earth and creating symbiote mire": {
        "ko": "공중에서 급강하하여 지면을 내리치고 심비오트 늪을 형성하여 적을 둔화시킵니다.",
        "ja": "空中から急降下して地面を叩きつけ、シンビオートの沼を形成して敵を足止めする。"
    },
    "Consume surrounding biomass to generate massive temporary bonus health": {
        "ko": "주변 생체 질량을 흡수하여 대량의 임시 추가 체력을 생성합니다.",
        "ja": "周囲の生体物質を取り込み、大量の一時的追加体力を生成する。"
    },
    "Engulf surrounding enemies in an explosive storm of devouring tentacles": {
        "ko": "주변의 모든 적을 휘감는 폭발적인 촉수 폭풍을 펼쳐 집어삼킵니다.",
        "ja": "周囲の敵全員を貪り食う爆発的な触手の嵐を展開し、敵を飲み込む。"
    },
    "Venom can crawl along any wall or vertical surface effortlessly": {
        "ko": "모든 벽면과 수직 지형을 자유자재로 기어오를 수 있습니다.",
        "ja": "あらゆる壁面や垂直な地形を自在に這い登ることができる。"
    }
}

def clean_key(text):
    return re.sub(r'\s+', ' ', text).strip() if text else ''

def build_vanguard_json():
    with open('scratch/skills_vanguard.json', 'r', encoding='utf-8') as f:
        v_skills = json.load(f)

    result = {}
    matched = 0
    total = 0
    unmatched_list = []

    # Map normalized dictionary
    norm_dict = {clean_key(k): v for k, v in VANGUARD_DICT.items()}

    for hero, skills in v_skills.items():
        for sk in skills:
            for s_item in [sk, sk.get('upgrade')]:
                if not s_item or not s_item.get('desc'):
                    continue
                total += 1
                raw_d = s_item['desc']
                c_d = clean_key(raw_d)

                trans = norm_dict.get(c_d)
                if not trans:
                    # Fuzzy match fallback
                    for k, val in norm_dict.items():
                        if k[:40].lower() in c_d.lower():
                            trans = val
                            break

                if trans:
                    matched += 1
                    result[c_d] = trans
                    result[raw_d] = trans
                else:
                    unmatched_list.append((hero, s_item.get('name', sk['name']), c_d))

    os.makedirs('data/translations', exist_ok=True)
    with open('data/translations/skills_vanguard.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Vanguard skills translated: {matched} / {total}")
    if unmatched_list:
        print(f"Unmatched {len(unmatched_list)} items:")
        for h, sname, cd in unmatched_list[:10]:
            print(f"  [{h}] {sname}: {repr(cd)}")

if __name__ == '__main__':
    build_vanguard_json()
