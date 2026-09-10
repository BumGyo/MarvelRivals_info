# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Team-Up Translations Generator
Generates data/translations/teamups.json for all 107 official team-ups.
Every team-up includes:
 - base (Solo effect) in KO & JA
 - enhanced (Team-up effect with partner) in KO & JA
 - full (Combined text) in KO & JA
"""

import json
import re
import os

TEAMUP_TRANSLATIONS = {
    # 1. ADAM WARLOCK - COSMIC CYCLONE (Partner: STORM)
    "COSMIC CYCLONE": {
        "base_ko": "영혼 결속(Soul Bond)으로 연결된 팀원의 이동 속도가 증가합니다.",
        "base_ja": "ソウルボンドで繋がれた味方の移動速度が上昇する。",
        "enhanced_ko": "스톰과 함께 플레이 시, 연결된 팀원의 공격력이 추가로 증가합니다.",
        "enhanced_ja": "ストームとチームアップ時、繋がれた味方の与ダメージがさらに上昇する。"
    },
    # 2. ADAM WARLOCK - FLAWLESS DESIGN (Partner: ULTRON)
    "FLAWLESS DESIGN": {
        "base_ko": "코스믹 클러스터(Cosmic Cluster)가 아군을 적중시키면 치유를 제공합니다.",
        "base_ja": "コズミック・クラスターが味方に命中した際、回復を与えるようになる。",
        "enhanced_ko": "울트론과 함께 플레이 시, 코스믹 클러스터가 착탄 시 폭발을 일으킵니다.",
        "enhanced_ja": "ウルトロンとチームアップ時、コズミック・クラスターが着弾時に爆発を引き起こす。"
    },
    # 3. ANGELA - ASGARDIANS OF THE GALAXY (Partner: STAR-LORD)
    "ASGARDIANS OF THE GALAXY": {
        "base_ko": "스킬 활성화 시 목표 영역 내의 적을 탐지(Reveal)합니다. 스킬을 재입력하면 강타 공격을 가하며, 적중당한 적은 지상으로 추락(Grounded)합니다.",
        "base_ja": "発動時に指定エリア内の敵を探知する。再発動で叩きつけ攻撃を行い、命中した敵を接地(飛行不可)状態にする。",
        "enhanced_ko": "스타로드와 함께 플레이 시, 강타 공격에 적중당한 적 수에 비례하여 안젤라가 추가 체력을 획득합니다.",
        "enhanced_ja": "スター・ロードとチームアップ時、叩きつけ攻撃が命中した敵の数に応じてアンジェラが追加体力を獲得する。"
    },
    # 4. ANGELA - ODIN'S UNACKNOWLEDGED (Partner: LOKI)
    "ODIN'S UNACKNOWLEDGED": {
        "base_ko": "전방으로 환영을 투사합니다. 환영은 암살자의 돌진(Assassin's Charge)을 사용하여 전방의 적을 들이받으며, 정면으로 충돌한 적을 잠시 공중으로 끌고 갑니다.",
        "base_ja": "前方へ幻影を投射する。幻影はアサシン・チャージを繰り出して敵に突進し、正面衝突した敵を短時間空中へ巻き込む。",
        "enhanced_ko": "로키와 함께 플레이 시, 이 스킬의 충전 횟수가 2회로 증가합니다.",
        "enhanced_ja": "ロキとチームアップ時、スキルのチャージ数が2回に増加する。"
    },
    # 5. BLACK CAT - FELINE ALLIANCE (Partner: BLACK PANTHER)
    "FELINE ALLIANCE": {
        "base_ko": "피해를 입으면 비브라늄 에너지가 축적됩니다. 특정 임계치에 도달하면 폭발을 일으켜 주변 적에게 피해를 주고 밀쳐내며, 잠시 이동 속도 증가와 추가 체력을 얻습니다.",
        "base_ja": "被ダメージ時にヴィブラニウム・エネルギーが蓄積する。一定閾値に達すると爆発を放ち、周囲の敵にダメージとノックバックを与えつつ、一時的な移動速度上昇と追加体力を獲得する。",
        "enhanced_ko": "블랙 팬서와 함께 플레이 시, 이 폭발이 에너지 임계치 제한 없이 언제든 즉시 발동 가능해집니다.",
        "enhanced_ja": "ブラックパンサーとチームアップ時、エネルギー閾値の制限がなくなり、いつでも即座に爆発を発動可能になる。"
    },
    # 6. BLACK CAT - BINDING TIES (Partner: SPIDER-MAN)
    "BINDING TIES": {
        "base_ko": "와이어 갈고리로 이동 시 주변 적들을 얽어매어 둔화시키고 약간의 데미지를 입힙니다.",
        "base_ja": "ワイヤーフック移動時、周囲の敵を絡め取って減速させ、軽微なダメージを与える。",
        "enhanced_ko": "스파이더맨과 함께 플레이 시, 와이어 이동 경로에 적을 완전히 묶어두는 거미줄 덫을 추가로 남깁니다.",
        "enhanced_ja": "スパイダーマンとチームアップ時、ワイヤー移動の軌跡に敵を完全に足止めする蜘蛛の巣トラップを設置する。"
    },
    # 7. BLACK PANTHER - DAMISA-YAO (Partner: MAGIK)
    "DAMISA-YAO": {
        "base_ko": "비브라늄 표식을 남긴 적을 처치하면 주변에 충격파를 방출하여 주변 적들에게 피해를 줍니다.",
        "base_ja": "ヴィブラニウムの刻印を付与した敵を撃破すると、周囲に衝撃波を放ち敵にダメージを与える。",
        "enhanced_ko": "매직과 함께 플레이 시, 다크차일드 차원 포털이 열려 추가 암흑 데미지를 가합니다.",
        "enhanced_ja": "マジックとチームアップ時、ダークチャイルドの次元ポータルが開き、追加暗黒ダメージを与える。"
    },
    # 8. BLACK PANTHER - DIMENSIONAL SHORTCUT (Partner: CLOAK & DAGGER)
    "DIMENSIONAL SHORTCUT": {
        "base_ko": "질주 및 도약 중 회피율이 상승하고 받는 피해가 감소합니다.",
        "base_ja": "疾走および跳躍中の回避率が上昇し、被ダメージが軽減される。",
        "enhanced_ko": "클록 & 대거와 함께 플레이 시, 어둠의 차원을 통과해 순간적으로 짧은 거리를 순간이동할 수 있습니다.",
        "enhanced_ja": "クローク＆ダガーとチームアップ時、闇の次元を経由して短距離を瞬間移動できるようになる。"
    },
    # 9. BLADE - BLADE OF KHONSHU (Partner: MOON KNIGHT)
    "BLADE OF KHONSHU": {
        "base_ko": "출혈 상태인 적을 공격하면 추가 생명력 흡수 효과를 얻습니다.",
        "base_ja": "出血状態の敵を攻撃すると、追加のライフスティール効果を得る。",
        "enhanced_ko": "문나이트와 함께 플레이 시, 콘슈의 달빛 축복을 받아 검격에 달빛 파동이 추가됩니다.",
        "enhanced_ja": "ムーンナイトとチームアップ時、コンシュの月光の加護を受け、剣撃に月光の衝撃波が追加される。"
    },
    # 10. BLADE - BLEED FOR BATTLE (Partner: WOLVERINE)
    "BLEED FOR BATTLE": {
        "base_ko": "적에게 입힌 출혈 데미지에 비례하여 블레이드의 이동 속도가 점진적으로 상승합니다.",
        "base_ja": "敵に与えた出血ダメージに応じて、ブレイドの移動速度が段階的に上昇する。",
        "enhanced_ko": "울버린과 함께 플레이 시, 광폭화가 발동하여 근접 공격력이 비약적으로 상승합니다.",
        "enhanced_ja": "ウルヴァリンとチームアップ時、狂暴化が発動して近接攻撃力が飛躍的に上昇する。"
    },
    # 11. BLACK WIDOW - ALLIED AGENTS (Partner: HAWKEYE)
    "ALLIED AGENTS": {
        "base_ko": "적의 약점(헤드샷)을 명중시키면 즉시 탄약이 일정량 재장전됩니다.",
        "base_ja": "敵の弱点(ヘッドショット)に命中させると、即座に弾薬が一定量リロードされる。",
        "enhanced_ko": "호크아이와 함께 플레이 시, 정찰 화살에 포착된 적에게 가하는 피해가 대폭 증가합니다.",
        "enhanced_ja": "ホークアイとチームアップ時、ソナー矢で探知された敵に対する与ダメージが大幅に上昇する。"
    },
    # 12. BLACK WIDOW - BURNING BULLETS (Partner: THE PUNISHER)
    "BURNING BULLETS": {
        "base_ko": "저격 모드에서 사격 시 타깃의 이동 속도를 감소시키는 특수 탄환을 장전합니다.",
        "base_ja": "スナイパーモードでの射撃時、対象の移動速度を低下させる特殊弾を装填する。",
        "enhanced_ko": "퍼니셔와 함께 플레이 시, 탄환이 소이탄으로 강화되어 폭발과 지속 화염 피해를 일으킵니다.",
        "enhanced_ja": "パニッシャーとチームアップ時、弾丸が焼夷弾へと強化され、爆発と継続燃焼ダメージを与える。"
    },
    # 13. CAPTAIN AMERICA - STARS ALIGNED (Partner: WINTER SOLDIER)
    "STARS ALIGNED": {
        "base_ko": "방패 방어 시 전방의 피해를 막아내고 아군의 방어 진형을 보호합니다.",
        "base_ja": "シールド防御時、前方の攻撃を遮断して味方の前線を防護する。",
        "enhanced_ko": "윈터 솔져와 함께 플레이 시, 연계 전술이 활성화되어 방패 던지기 후 윈터 솔져의 연계 사격이 강화됩니다.",
        "enhanced_ja": "ウィンター・ソルジャーとチームアップ時、連携戦術が発動し、シールド投擲後に連携射撃が強化される。"
    },
    # 14. CAPTAIN AMERICA - VOLTAIC UNION (Partner: THOR)
    "VOLTAIC UNION": {
        "base_ko": "비브라늄 방패 공격이 적중하면 방패에 충격 에너지가 충전됩니다.",
        "base_ja": "ヴィブラニウム・シールドの攻撃が命中すると、シールドに衝撃エネルギーが充填される。",
        "enhanced_ko": "토르와 함께 플레이 시, 방패를 칠 때마다 토르의 번개가 방패를 타고 흘러 연쇄 전격 피해를 줍니다.",
        "enhanced_ja": "ソーとチームアップ時、シールドを叩くたびに電撃が宿り、連鎖電撃ダメージを放つ。"
    },
    # 15. CLOAK & DAGGER - OBLIVION SHROUD (Partner: MOON KNIGHT)
    "OBLIVION SHROUD": {
        "base_ko": "어둠의 장막 속에 머무는 동안 자신과 아군의 체력이 지속 회복됩니다.",
        "base_ja": "闇の帳の中に留まっている間、自身と味方の体力が持続回復する。",
        "enhanced_ko": "문나이트와 함께 플레이 시, 장막 내에 있는 적의 방어력이 감소하고 받는 피해가 증가합니다.",
        "enhanced_ja": "ムーンナイトとチームアップ時、帳の中の敵の防御力が低下し、被ダメージが増加する。"
    },
    # 16. CLOAK & DAGGER - FROZEN HAVEN (Partner: LUNA SNOW)
    "FROZEN HAVEN": {
        "base_ko": "빛의 단검이 아군에게 명중하면 추가 치유를 부여하고 이동 속도를 높입니다.",
        "base_ja": "光のダガーが味方に命中すると、追加回復と移動速度上昇を付与する。",
        "enhanced_ko": "루나 스노우와 함께 플레이 시, 빛의 단검에 냉기 결계가 추가되어 아군에게 보호막을 씌워줍니다.",
        "enhanced_ja": "ルナ・スノーとチームアップ時、光のダガーに氷の結界が宿り、味方にシールドを展開する。"
    },
    # 17. CYCLOPS - SLIM AND RED (Partner: PHOENIX)
    "SLIM AND RED": {
        "base_ko": "옵틱 블래스트(Optic Blast)의 지속 집중 사격 시간이 증가합니다.",
        "base_ja": "オプティック・ブラストの継続照射時間が増加する。",
        "enhanced_ko": "피닉스와 함께 플레이 시, 피닉스 포스의 불꽃이 광선에 주입되어 방어막을 관통하고 폭발을 일으킵니다.",
        "enhanced_ja": "フェニックスとチームアップ時、フェニックスフォースの炎が宿り、バリアを貫通して大爆発を起こす。"
    },
    # 18. CYCLOPS - KINETIC KIN (Partner: HAVOK / EMMA FROST)
    "KINETIC KIN": {
        "base_ko": "전술 지휘를 통해 시야 내 아군의 치명타 확률을 높여줍니다.",
        "base_ja": "戦術指揮により、視界内の味方のクリティカル率を上昇させる。",
        "enhanced_ko": "엠마 프로스트와 함께 플레이 시, 텔레파시 링크가 형성되어 전술 명령의 범위가 전장 전체로 확장됩니다.",
        "enhanced_ja": "エマ・フロストとチームアップ時、テレパシーリンクが結ばれ、戦術指揮の範囲が戦場全体に拡大する。"
    },
    # 19. DEADPOOL - "HEL-YEAH, HONEY" (Partner: HELA)
    '"HEL-YEAH, HONEY"': {
        "base_ko": "전투 불능 시 부활 타이머가 단축되며, 부활 직후 이동 속도 증가 버프를 받습니다.",
        "base_ja": "リスポーン待機時間が短縮され、復活直後に移動速度上昇バフを獲得する。",
        "enhanced_ko": "헬라와 함께 플레이 시, 헬라의 죽음의 왕관에서 까마귀 지원 공격을 소환합니다.",
        "enhanced_ja": "ヘラとチームアップ時、ヘラの死の王冠からカラスの支援攻撃を召喚する。"
    },
    # 20. DEADPOOL - GUMBO CHIMICHANGAS (Partner: GAMBIT)
    "GUMBO CHIMICHANGAS": {
        "base_ko": "치미창가를 던져 아군에게 회복을, 적에게 물리적 타격을 줍니다.",
        "base_ja": "チミチャンガを投擲し、味方に回復を、敵に物理打撃を与える。",
        "enhanced_ko": "갬빗과 함께 플레이 시, 치미창가에 키네틱 카드가 충전되어 화려한 분홍빛 폭발을 일으킵니다.",
        "enhanced_ja": "ガンビットとチームアップ時、チミチャンガにキネティックエネルギーが充填され、ピンクの爆発を起こす。"
    },
    # 21. DEVIL DINOSAUR - PRIMAL PUNISHMENT (Partner: THE PUNISHER)
    "PRIMAL PUNISHMENT": {
        "base_ko": "적을 물어뜯을 때마다 분노가 쌓여 공격 속도가 점진적으로 상승합니다.",
        "base_ja": "敵に噛みつくたびに怒りが蓄積し、攻撃速度が段階的に上昇する。",
        "enhanced_ko": "퍼니셔와 함께 플레이 시, 등에 장착된 화기 포탑에서 지원 사격이 발사됩니다.",
        "enhanced_ja": "パニッシャーとチームアップ時、背中に搭載された重火器タレットから支援射撃が放たれる。"
    },
    # 22. DEVIL DINOSAUR - SURF & TURF (Partner: JEFF THE LAND SHARK)
    "SURF & TURF": {
        "base_ko": "지면을 강타할 때 주변 적들에게 감속 효과를 줍니다.",
        "base_ja": "地面を叩きつけた際、周囲の敵に鈍足効果を付与する。",
        "enhanced_ko": "제프 더 랜드 샤크와 함께 플레이 시, 공룡 등 위에 제프가 올라타 물대포를 뿜어내며 함께 싸웁니다.",
        "enhanced_ja": "ジェフ・ザ・ランド・シャークとチームアップ時、背中にジェフが乗り、ハイドロポンプを放ちながら共闘する。"
    },
    # 23. DOCTOR STRANGE - GAMMA MAELSTROM (Partner: HULK)
    "GAMMA MAELSTROM": {
        "base_ko": "아가모토의 눈을 통해 전방의 신비 마법 공격력이 강화됩니다.",
        "base_ja": "アガモットの瞳を通して前方の魔術攻撃の威力が強化される。",
        "enhanced_ko": "헐크와 함께 플레이 시, 마엘스트롬 포털에 감마선 에너지가 주입되어 거대한 감마 폭풍을 일으킵니다.",
        "enhanced_ja": "ハルクとチームアップ時、マエルストロムポータルにガンマ線が注入され、巨大なガンマ嵐を発生させる。"
    },
    # 24. DOCTOR STRANGE - PSIONIC VORTEX (Partner: SCARLET WITCH)
    "PSIONIC VORTEX": {
        "base_ko": "세라핌의 방패가 흡수한 데미지에 비례해 마법 에너지를 회복합니다.",
        "base_ja": "セラフィムの盾が吸収したダメージに応じて魔力エネルギーを回復する。",
        "enhanced_ko": "스칼렛 위치와 함께 플레이 시, 혼돈 마법이 결합되어 차원문에 흡수된 적을 뒤틀린 시공간에 가둡니다.",
        "enhanced_ja": "スカーレット・ウィッチとチームアップ時、混沌魔術が融合し、ポータルに引き込まれた敵を歪んだ時空に幽閉する。"
    },
    # 25. DAREDEVIL - COMPREHENSIVE DEFENSE (Partner: IRON FIST)
    "COMPREHENSIVE DEFENSE": {
        "base_ko": "레이더 센스를 활성화하여 은신 중인 적과 벽 뒤의 적을 감지합니다.",
        "base_ja": "レーダーセンスを発動し、ステルス中の敵や壁裏の敵を探知する。",
        "enhanced_ko": "아이언 피스트와 함께 플레이 시, 기(氣) 에너지가 공명하여 근접 반격 시 기합 파동이 발생합니다.",
        "enhanced_ja": "アイアン・フィストとチームアップ時、気エネルギーが共鳴し、近接反撃時に衝撃波を放つ。"
    },
    # 26. DAREDEVIL - DEVILISH AFFAIR (Partner: ELEKTRA / BLACK WIDOW)
    "DEVILISH AFFAIR": {
        "base_ko": "곤봉 던지기가 지형지물에 튕길 때마다 피해량이 증가합니다.",
        "base_ja": "ビリークラブの投擲が壁や障害物に跳弾するたびに威力が上昇する。",
        "enhanced_ko": "블랙 위도우와 함께 플레이 시, 치명적인 와이어 트랩이 추가되어 적의 목을 휘감습니다.",
        "enhanced_ja": "ブラック・ウィドウとチームアップ時、致命的なワイヤートラップが追加され、敵を拘束する。"
    },
    # 27. ELSA BLOODSTONE - PREHISTORIC TRAP (Partner: DEVIL DINOSAUR)
    "PREHISTORIC TRAP": {
        "base_ko": "특수 산탄총 사격 시 몬스터 사냥용 은 탄환을 발사합니다.",
        "base_ja": "特殊ショットガン射撃時、モンスター狩猟用の銀弾を発射する。",
        "enhanced_ko": "데빌 다이노소어와 함께 플레이 시, 공룡 덫을 소환하여 덫에 걸린 적을 거대한 이빨로 물어뜯게 합니다.",
        "enhanced_ja": "デビル・ダイナソーとチームアップ時、恐竜トラップを設置し、捕まった敵を巨大な牙で噛み砕かせる。"
    },
    # 28. ELSA BLOODSTONE - LOUDMOUTH MERCS (Partner: DEADPOOL)
    "LOUDMOUTH MERCS": {
        "base_ko": "적을 처치할 때마다 블러드스톤 목걸이가 빛나며 재장전 속도가 빨라집니다.",
        "base_ja": "敵を撃破するたびにブラッドストーンが輝き、リロード速度が上昇する。",
        "enhanced_ko": "데드풀과 함께 플레이 시, 둘의 입담이 폭발하며 주변 적들의 집중력을 흐트러뜨리고 방어력을 깎아냅니다.",
        "enhanced_ja": "デッドプールとチームアップ時、軽快な掛け合いが炸裂し、周囲の敵を動揺させて防御力を削り落とす。"
    },
    # 29. EMMA FROST - SPIRIT BREAKER (Partner: PSYLOCKE)
    "SPIRIT BREAKER": {
        "base_ko": "다이아몬드 형태로 변신 중 적의 물리 방어력을 무시하고 타격을 가합니다.",
        "base_ja": "ダイヤモンド形態中、敵の物理装甲を無視して打撃を叩き込む。",
        "enhanced_ko": "사일록과 함께 플레이 시, 사이킥 칼날이 다이아몬드 주먹에 깃들어 타격 시 정신 피해를 함께 입힙니다.",
        "enhanced_ja": "サイロックとチームアップ時、サイキックブレードが拳に宿り、打撃時に精神ダメージを同時に与える。"
    },
    # 30. EMMA FROST - ICED OUT DIAMOND (Partner: LUNA SNOW)
    "ICED OUT DIAMOND": {
        "base_ko": "다이아몬드 방어막이 파괴될 때 주변에 다이아몬드 파편을 사방으로 튀깁니다.",
        "base_ja": "ダイヤモンドシールド破壊時、周囲にダイヤモンドの破片を飛散させて攻撃する。",
        "enhanced_ko": "루나 스노우와 함께 플레이 시, 절대영도의 얼음이 다이아몬드를 감싸 타격받은 적을 즉시 빙결시킵니다.",
        "enhanced_ja": "ルナ・スノーとチームアップ時、絶対零度の氷が纏われ、攻撃を受けた敵を即座に凍結させる。"
    },
    # 31. GROOT - WILD WALL (Partner: ROCKET RACCOON)
    "WILD WALL": {
        "base_ko": "나무 벽 뒤에 숨어있는 동안 그루트의 자연 치유 속도가 증가합니다.",
        "base_ja": "木の壁の後ろに身を隠している間、グルートの自己回復速度が上昇する。",
        "enhanced_ko": "로켓 라쿤과 함께 플레이 시, 로켓이 그루트 어깨에 올라타 벽 너머로 강력한 폭격을 퍼붓습니다.",
        "enhanced_ja": "ロケット・ラクーンとチームアップ時、ロケットが肩に乗り、壁越しに強力な爆撃を浴びせる。"
    },
    # 32. GROOT - BUBBLE BUDDIES (Partner: JEFF THE LAND SHARK)
    "BUBBLE BUDDIES": {
        "base_ko": "덩굴로 적을 끌어당길 때 대상의 이동 속도를 잠시 빼앗아옵니다.",
        "base_ja": "蔓で敵を引き寄せた際、対象の移動速度を奪い取って自身を加速する。",
        "enhanced_ko": "제프 더 랜드 샤크와 함께 플레이 시, 끌려온 적 주변에 거품 방울을 터뜨려 주변 적들까지 함께 가둡니다.",
        "enhanced_ja": "ジェフ・ザ・ランド・シャークとチームアップ時、引き寄せた敵の周囲で水泡が炸裂し、周囲の敵もろとも拘束する。"
    },
    # 33. GAMBIT - FAVORABLE ODDS (Partner: ROGUE)
    "FAVORABLE ODDS": {
        "base_ko": "키네틱 카드를 연속 투척할 때마다 치명타 확률이 점진적으로 상승합니다.",
        "base_ja": "キネティックカードを連続投擲するたびにクリティカル率が段階的に上昇する。",
        "enhanced_ko": "로그와 함께 플레이 시, 서로의 호흡이 맞춰져 로그에게 키네틱 차징 능력을 부여합니다.",
        "enhanced_ja": "ローグとチームアップ時、抜群の呼吸が合わさり、ローグにキネティックチャージ能力を付与する。"
    },
    # 34. GAMBIT - SPARKLING STAFF (Partner: JUBILEE)
    "SPARKLING STAFF": {
        "base_ko": "봉 공격으로 지면을 내리칠 때 전방으로 키네틱 충격파를 발사합니다.",
        "base_ja": "棍棒攻撃で地面を叩いた際、前方へキネティック衝撃波を放つ。",
        "enhanced_ko": "쥬빌리와 함께 플레이 시, 폭죽 불꽃놀이 에너지가 봉 끝에 장전되어 눈부신 불꽃 폭발을 일으킵니다.",
        "enhanced_ja": "ジュビリーとチームアップ時、花火エネルギーが棍の先端に宿り、眩い閃光爆発を発生させる。"
    },
    # 35. HAWKEYE - SENBONZAKURA STRIKE (Partner: PSYLOCKE)
    "SENBONZAKURA STRIKE": {
        "base_ko": "활을 완전히 당겨 사격하면 화살이 적을 관통하여 날아갑니다.",
        "base_ja": "弓を最大まで引き絞って放つと、矢が敵を貫通して飛翔する。",
        "enhanced_ko": "사일록과 함께 플레이 시, 화살에 벚꽃 사이킥 나비가 깃들어 명중 시 사방으로 칼날 나비가 흩날립니다.",
        "enhanced_ja": "サイロックとチームアップ時、矢にサイキック蝶が宿り、命中時に千本桜のように無数の刃が舞い散る。"
    },
    # 36. HAWKEYE - MOONLIT SLASH (Partner: MOON KNIGHT)
    "MOONLIT SLASH": {
        "base_ko": "근접 전투 시 활을 회전시켜 접근한 적을 밀쳐냅니다.",
        "base_ja": "近接戦時、弓を素早く回転させて接近した敵をノックバックする。",
        "enhanced_ko": "문나이트와 함께 플레이 시, 초승달 다트의 궤적을 활시위로 튕겨 유도 궤적으로 전환합니다.",
        "enhanced_ja": "ムーンナイトとチームアップ時、三日月ダーツを弓で弾いて誘導軌道へと変化させる。"
    },
    # 37. HELA - Hel Tendrils (Partner: LOKI)
    "Hel Tendrils": {
        "base_ko": "적을 처치할 때마다 헬라 주변에 밤의 검이 하나씩 자동 생성됩니다.",
        "base_ja": "敵を撃破するたびに、ヘラの周囲に夜の剣が1本ずつ自動生成される。",
        "enhanced_ko": "로키와 함께 플레이 시, 로키의 분신 옆에도 헬라의 검이 소환되어 동시에 폭격을 가합니다.",
        "enhanced_ja": "ロキとチームアップ時、ロキの分身の周囲にもヘラの剣が召喚され、一斉射撃を放つ。"
    },
    # 38. HELA - DEEP WRATH (Partner: THOR)
    "DEEP WRATH": {
        "base_ko": "죽음의 기운을 모아 던지는 검의 투사체 속도가 증가합니다.",
        "base_ja": "死の魔力を凝縮して放つ剣の弾速が上昇する。",
        "enhanced_ko": "토르와 함께 플레이 시, 아스가르드의 번개가 죽음의 검과 융합되어 폭발적인 전격 피해를 줍니다.",
        "enhanced_ja": "ソーとチームアップ時、アスガルドの雷が死の剣と融合し、壊滅的な雷撃爆発を起こす。"
    },
    # 39. HULK - SAVAGE SLAM (Partner: IRON MAN)
    "SAVAGE SLAM": {
        "base_ko": "헐크의 지면 강타 충격파가 적들의 방어막에 2배의 피해를 입힙니다.",
        "base_ja": "ハルクの地面叩きつけ衝撃波が、敵のシールドに2倍のダメージを与える。",
        "enhanced_ko": "아이언맨과 함께 플레이 시, 아이언맨이 리펄서 레이저를 헐크의 주먹에 집중시켜 에너지 폭발을 배가합니다.",
        "enhanced_ja": "アイアンマンとチームアップ時、リパルサービームがハルクの拳に照射され、爆発威力を倍増させる。"
    },
    # 40. HULK - GAMMA FASTBALL (Partner: WOLVERINE)
    "GAMMA FASTBALL": {
        "base_ko": "헐크가 도약 착지할 때 지면을 부수며 주변 적들을 공중에 띄웁니다.",
        "base_ja": "ハルクが跳躍着地した際、地面を叩き割って周囲の敵をノックアップする。",
        "enhanced_ko": "울버린과 함께 플레이 시, 헐크가 울버린을 집어던지는 '패스트볼 스페셜'을 구사하여 울버린이 적진을 급습합니다.",
        "enhanced_ja": "ウルヴァリンとチームアップ時、ハルクがウルヴァリンを力任せに投げ飛ばす合体技『ファストボール・スペシャル』を発動する。"
    },
    # 41. HUMAN TORCH - FIERY SPARKS (Partner: STORM)
    "FIERY SPARKS": {
        "base_ko": "비행 중 화염 궤적을 남겨 뒤따라오는 적에게 지속적인 화상 피해를 줍니다.",
        "base_ja": "飛行時に炎の航跡を残し、追尾してくる敵に継続火傷ダメージを与える。",
        "enhanced_ko": "스톰과 함께 플레이 시, 폭풍우 바람이 불길을 확산시켜 전장 전체를 거대한 화염 폭풍(파이어스톰)으로 뒤덮습니다.",
        "enhanced_ja": "ストームとチームアップ時、嵐の突風が炎を拡散させ、戦場全域を巨大な火災旋風で包み込む。"
    },
    # 42. HUMAN TORCH - STORMING IGNITION (Partner: INVISIBLE WOMAN)
    "STORMING IGNITION": {
        "base_ko": "불덩어리를 연속 발사할 때 열기가 축적되어 사격 속도가 증가합니다.",
        "base_ja": "火炎弾を連射するたびに熱量が蓄積し、連射速度が上昇する。",
        "enhanced_ko": "인비저블 우먼과 함께 플레이 시, 투명 보호막 구체 안에 화염을 가두어 초고온 플라즈마 폭탄으로 폭파시킵니다.",
        "enhanced_ja": "インビジブル・ウーマンとチームアップ時、透明バリア球体内に熱量を封じ込め、超高温プラズマ爆弾として炸裂させる。"
    },
    # 43. IRON FIST - IRON & STONE (Partner: THE THING)
    "IRON & STONE": {
        "base_ko": "곤륜의 기(氣)를 모아 주먹 공격 시 전방에 원거리 기공파를 발사합니다.",
        "base_ja": "クン・ルンの気を凝縮し、拳撃時に前方へ遠距離気功波を放つ。",
        "enhanced_ko": "더 씽과 함께 플레이 시, 암석의 힘이 권법에 융합되어 주먹을 휘두를 때마다 지진 파편이 솟구칩니다.",
        "enhanced_ja": "ザ・シングとチームアップ時、岩石の剛力が拳法に宿り、殴打するたびに大地から岩石破片が隆起する。"
    },
    # 44. IRON FIST - KUMIHO PALM (Partner: WHITE FOX)
    "KUMIHO PALM": {
        "base_ko": "발차기 연타 성공 시 자신의 체력을 즉시 일정량 회복합니다.",
        "base_ja": "蹴り技の連打が命中すると、自身の体力を即座に一定量回復する。",
        "enhanced_ko": "화이트 폭스와 함께 플레이 시, 구미호의 영기가 깃들어 타격당한 적의 기력을 흡수하고 영혼 탈취 효과를 냅니다.",
        "enhanced_ja": "ホワイト・フォックスとチームアップ時、九尾の狐の霊気が宿り、打撃を与えた敵から精気を吸収する。"
    },
    # 45. IRON MAN - GAMMA CHARGE (Partner: HULK)
    "GAMMA CHARGE": {
        "base_ko": "아머의 리펄서 에너지 재충전 속도가 상시 상승합니다.",
        "base_ja": "アーマーのリパルサーエネルギー再充填速度が常時上昇する。",
        "enhanced_ko": "헐크와 함께 플레이 시, 아머의 아크 리액터에 감마선이 과충전되어 녹색 감마 레이저를 발사합니다.",
        "enhanced_ja": "ハルクとチームアップ時、アークリアクターにガンマ線が過充填され、強力な緑色ガンマレーザーを照射する。"
    },
    # 46. IRON MAN - THUNDER OVERDRIVE (Partner: THOR)
    "THUNDER OVERDRIVE": {
        "base_ko": "유니빔 사격 중 이동 속도 감소 페널티가 줄어듭니다.",
        "base_ja": "ユニビーム照射中の移動速度低下ペナルティが軽減される。",
        "enhanced_ko": "토르와 함께 플레이 시, 묠니르의 벼락이 아이언맨 아머를 감전 충전하여 공격력이 400% 증폭됩니다.",
        "enhanced_ja": "ソーとチームアップ時、ムジョルニアの雷霆がスーツに充電され、出力が劇的に過負荷増幅される。"
    },
    # 47. INVISIBLE WOMAN - UNITED SIBLINGS (Partner: HUMAN TORCH)
    "UNITED SIBLINGS": {
        "base_ko": "투명화 상태 중 아군에게 주는 지속 보호막 수치가 증가합니다.",
        "base_ja": "透明化中、味方に付与する持続シールド値が上昇する。",
        "enhanced_ko": "휴먼 토치와 함께 플레이 시, 보호막에 화염 속성이 깃들어 보호막을 두른 아군을 공격하는 적에게 화염 반사 피해를 줍니다.",
        "enhanced_ja": "ヒューマン・トーチとチームアップ時、シールドに炎属性が宿り、攻撃してきた敵へ火炎反射ダメージを与える。"
    },
    # 48. INVISIBLE WOMAN - FIRST FAMILY (Partner: MISTER FANTASTIC)
    "FIRST FAMILY": {
        "base_ko": "역장 방벽을 생성하여 적의 통과를 막고 물리 탄환을 튕겨냅니다.",
        "base_ja": "力場バリアを生成し、敵の通過を阻止して物理弾を弾き返す。",
        "enhanced_ko": "미스터 판타스틱과 함께 플레이 시, 역장 탄성이 극대화되어 아군이 방벽을 밟고 높이 도약할 수 있습니다.",
        "enhanced_ja": "ミスター・ファンタスティックとチームアップ時、力場の弾性が極大化し、味方がバリアを踏んで大ジャンプできるようになる。"
    },
    # 49. JEFF THE LAND SHARK - GUARDIAN OF THE DEEP (Partner: LUNA SNOW)
    "GUARDIAN OF THE DEEP": {
        "base_ko": "땅속에서 헤엄치는 동안 이동 속도가 빨라지고 방어력이 상승합니다.",
        "base_ja": "地面を潜航水泳している間、移動速度が上昇し防御力が高まる。",
        "enhanced_ko": "루나 스노우와 함께 플레이 시, 뿜어내는 물대포가 얼어붙어 얼음 미끄럼틀을 만들고 적을 빙결시킵니다.",
        "enhanced_ja": "ルナ・スノーとチームアップ時、吐き出す水流が氷結し、アイススライダーを生成して敵を凍結させる。"
    },
    # 50. JEFF THE LAND SHARK - MR. POOL'S INTERDIMENSIONAL TOY BOX (Partner: DEADPOOL)
    "MR. POOL'S INTERDIMENSIONAL TOY BOX": {
        "base_ko": "치유 거품을 뱉어 아군을 회복시키고 보호막을 제공합니다.",
        "base_ja": "回復の泡を吐き出し、味方を回復させてシールドを付与する。",
        "enhanced_ko": "데드풀과 함께 플레이 시, 데드풀의 장난감 상자에서 폭발 장난감이 튀어나와 적들에게 무작위 카오스 폭탄을 투척합니다.",
        "enhanced_ja": "デッドプールとチームアップ時、デッドプールのオモチャ箱から爆破トイが飛び出し、敵へランダム爆弾をばら撒く。"
    },
    # 51. JUBILATION LEE - HELLFIRE SPARKS (Partner: THE HOOD)
    "HELLFIRE SPARKS": {
        "base_ko": "플라즈마 폭죽을 발사하여 눈부신 빛과 함께 적에게 폭발 피해를 줍니다.",
        "base_ja": "プラズマ花火を発射し、眩い閃光とともに敵に爆発ダメージを与える。",
        "enhanced_ko": "더 후드와 함께 플레이 시, 암흑 지옥불이 폭죽에 결합되어 폭발 시 암흑 불길이 바닥에 잔류합니다.",
        "enhanced_ja": "ザ・フッドとチームアップ時、暗黒の地獄業火が花火に融合し、着弾地点に黒炎が残留する。"
    },
    # 52. JUBILATION LEE - VAMPIRIC KIN (Partner: BLADE)
    "VAMPIRIC KIN": {
        "base_ko": "폭죽이 적중한 적의 시야를 잠시 실명시키고 혼란을 줍니다.",
        "base_ja": "花火が命中した敵の視界を一時的に奪い、暗闇と混乱をもたらす。",
        "enhanced_ko": "블레이드와 함께 플레이 시, 뱀파이어 본능이 깨어나 폭발 피해의 일정 비율을 체력으로 흡수합니다.",
        "enhanced_ja": "ブレイドとチームアップ時、吸血鬼の本能が覚醒し、爆発ダメージの一部を自身の体力として吸収する。"
    },
    # 53. LOKI - VILLAIN'S ILLUSION (Partner: HELA)
    "VILLAIN'S ILLUSION": {
        "base_ko": "분신을 소환하여 로키의 주문을 동시에 시전하게 합니다.",
        "base_ja": "分身を召喚し、ロキの呪文を同時に連動詠唱させる。",
        "enhanced_ko": "헬라와 함께 플레이 시, 분신이 파괴될 때 헬라의 나이트소드가 사방으로 폭발하며 적들을 꿰뚫습니다.",
        "enhanced_ja": "ヘラとチームアップ時、分身が破壊された際に無数の夜の剣が四方へ爆裂し、敵を貫通する。"
    },
    # 54. LOKI - VIBRANT VITALITY (Partner: THOR)
    "VIBRANT VITALITY": {
        "base_ko": "로키가 은신하거나 기습할 때 치명타 데미지가 증가합니다.",
        "base_ja": "ロキがステルスまたは背後奇襲を行った際、クリティカルダメージが上昇する。",
        "enhanced_ko": "토르와 함께 플레이 시, 형제의 장난기가 발동하여 토르의 번개 환영을 만들어 적들을 기만합니다.",
        "enhanced_ja": "ソーとチームアップ時、兄弟の悪戯心が発動し、ソーの幻影雷撃を発生させて敵を翻弄する。"
    },
    # 55. LUNA SNOW - ATLAS BOND (Partner: NAMOR)
    "ATLAS BOND": {
        "base_ko": "얼음 스케이트를 타고 고속 질주하며 아군을 치유하는 얼음 오라를 내뿜습니다.",
        "base_ja": "アイススケートで高速滑走し、味方を癒やす氷のオーラを放つ。",
        "enhanced_ko": "네이머와 함께 플레이 시, 네이머의 바다 소환물에 빙결 속성이 부여되어 빙산 골렘으로 강화됩니다.",
        "enhanced_ja": "ネイモアとチームアップ時、召喚物に氷属性が付与され、強力な氷山ゴーレムへと強化される。"
    },
    # 56. LUNA SNOW - DUALITY DANCE (Partner: IRON FIST)
    "DUALITY DANCE": {
        "base_ko": "빛의 얼음과 어둠의 얼음을 번갈아 사용하여 치유와 공격 모드를 즉시 전환합니다.",
        "base_ja": "光の氷と闇の氷を交互に操り、回復と攻撃モードを即座に切り替える。",
        "enhanced_ko": "아이언 피스트와 함께 플레이 시, 기공 댄스가 조화를 이루어 춤추는 동안 주변 아군 전체의 공격력과 치유량이 동반 상승합니다.",
        "enhanced_ja": "アイアン・フィストとチームアップ時、気功ダンスが共鳴し、舞踏中に周囲の味方全体の攻撃力と回復量が共に上昇する。"
    },
    # 57. MAGIK - CHAIN OF CYTTORAK (Partner: DOCTOR STRANGE)
    "CHAIN OF CYTTORAK": {
        "base_ko": "소울소드를 휘둘러 림보 차원의 에너지를 방출합니다.",
        "base_ja": "ソウルソードを振り回し、リンボ次元の魔力エネルギーを放出する。",
        "enhanced_ko": "닥터 스트레인지와 함께 플레이 시, 사이토락의 붉은 쇠사슬이 소환되어 적들을 한곳으로 강하게 끌어모읍니다.",
        "enhanced_ja": "ドクター・ストレンジとチームアップ時、サイトラックの真紅の鎖が召喚され、敵を一箇所に引き寄せて拘束する。"
    },
    # 58. MAGIK - VOID PENTAGRAM (Partner: SCARLET WITCH)
    "VOID PENTAGRAM": {
        "base_ko": "스테핑 디스크를 타고 순간이동한 직후 공격력이 잠시 상승합니다.",
        "base_ja": "ステッピング・ディスクで瞬間移動した直後、短時間攻撃力が上昇する。",
        "enhanced_ko": "스칼렛 위치와 함께 플레이 시, 포털 주변에 혼돈의 오망진이 새겨져 텔레포트하는 적을 즉시 침묵시킵니다.",
        "enhanced_ja": "スカーレット・ウィッチとチームアップ時、ポータルの周囲に混沌の五芒星が刻まれ、通過した敵を即座に沈黙させる。"
    },
    # 59. MAGNETO - METALLIC CHAOS (Partner: SCARLET WITCH)
    "METALLIC CHAOS": {
        "base_ko": "주변에 자력 보호막을 형성하여 날아오는 모든 투사체를 반사합니다.",
        "base_ja": "周囲に磁気シールドを展開し、飛来する弾丸を跳ね返す。",
        "enhanced_ko": "스칼렛 위치와 함께 플레이 시, 금속 칼날에 혼돈 마법이 주입되어 유도 비행하는 거대 혼돈의 검으로 변합니다.",
        "enhanced_ja": "スカーレット・ウィッチとチームアップ時、金属片に混沌魔術が宿り、敵を追尾する巨大な混沌の魔剣へと変貌する。"
    },
    # 60. MAGNETO - MAGNETIC RESONANCE (Partner: EMMA FROST)
    "MAGNETIC RESONANCE": {
        "base_ko": "자력 폭풍을 일으켜 전방의 금속성 장애물과 적들을 끌어당깁니다.",
        "base_ja": "磁気嵐を発生させ、前方の敵を引き寄せる。",
        "enhanced_ko": "엠마 프로스트와 함께 플레이 시, 다이아몬드 공명이 일어나 자력 장벽의 내구도가 2배로 증가합니다.",
        "enhanced_ja": "エマ・フロストとチームアップ時、ダイヤモンド共鳴が起こり、磁気バリアの耐久値が2倍に増加する。"
    },
    # 61. MANTIS - STAR BLOSSOM (Partner: STAR-LORD)
    "STAR BLOSSOM": {
        "base_ko": "치유의 꽃잎을 날려 아군의 체력을 회복시키고 이동 속도를 높여줍니다.",
        "base_ja": "癒やしの花弁を散らし、味方の体力を回復させて移動速度を上昇させる。",
        "enhanced_ko": "스타로드와 함께 플레이 시, 스타로드의 부스터 추진제에 생명 에너지가 결합되어 스타로드의 회피 쿨다운이 즉시 리셋됩니다.",
        "enhanced_ja": "スター・ロードとチームアップ時、推進ブースターに生命エネルギーが融合し、回避スキルのクールダウンが即座にリセットされる。"
    },
    # 62. MANTIS - VITALITY PACT (Partner: ADAM WARLOCK)
    "VITALITY PACT": {
        "base_ko": "생체 감응 능력을 사용하여 주변 적들을 수면 상태로 만듭니다.",
        "base_ja": "精神感応能力を発動し、周囲の敵を深い睡眠状態に陥れる。",
        "enhanced_ko": "아담 워록과 함께 플레이 시, 코스믹 생명선이 연결되어 치유 중인 아군이 쓰러져도 즉시 1회 자동 부활합니다.",
        "enhanced_ja": "アダム・ウォーロックとチームアップ時、コズミック生命線が結ばれ、治療中の味方が倒れても即座に1回自動蘇生する。"
    },
    # 63. MOON KNIGHT - LUMINOUS MOON (Partner: CLOAK & DAGGER)
    "LUMINOUS MOON": {
        "base_ko": "초승달 다트를 연속으로 던져 적에게 표식을 남깁니다.",
        "base_ja": "三日月ダーツを連続投擲し、敵に月光の刻印を付与する。",
        "enhanced_ko": "클록 & 대거와 함께 플레이 시, 달빛 표식이 폭발할 때 어둠의 차원 왜곡이 발생하여 주변 적들을 눈멀게 합니다.",
        "enhanced_ja": "クローク＆ダガーとチームアップ時、月光刻印の爆発時に次元の歪みが生じ、周囲の敵の視界を奪う。"
    },
    # 64. MOON KNIGHT - BLOOD MOON (Partner: BLADE)
    "BLOOD MOON": {
        "base_ko": "공중에서 글라이딩 활공하며 지상의 적에게 암살 강타를 가합니다.",
        "base_ja": "空中を滑空しながら、地上の敵へ急降下暗殺ストライクを叩き込む。",
        "enhanced_ko": "블레이드와 함께 플레이 시, 핏빛 달이 떠올라 문나이트의 모든 공격이 출혈과 치유 감소를 유발합니다.",
        "enhanced_ja": "ブレイドとチームアップ時、紅い血の月が昇り、ムーンナイトの全攻撃に出血と回復低下が付与される。"
    },
    # 65. MISTER FANTASTIC - FANTASTIC AMPLIFIER (Partner: INVISIBLE WOMAN)
    "FANTASTIC AMPLIFIER": {
        "base_ko": "고무처럼 몸을 늘려 넓은 범위의 적들을 휘감아 가격합니다.",
        "base_ja": "ゴムのように肉体を伸縮させ、広範囲の敵を絡め取って攻撃する。",
        "enhanced_ko": "인비저블 우먼과 함께 플레이 시, 늘어난 몸 전체를 투명 보호막으로 감싸 돌진 시 무적 상태가 됩니다.",
        "enhanced_ja": "インビジブル・ウーマンとチームアップ時、伸長した全身を透明バリアが覆い、突進中が無敵状態となる。"
    },
    # 66. MISTER FANTASTIC - CLOBBERIN' RESEARCH DEPT. (Partner: THE THING)
    "CLOBBERIN' RESEARCH DEPT.": {
        "base_ko": "몸을 풍선처럼 부풀려 날아오는 포탄을 튕겨냅니다.",
        "base_ja": "身体を風船のように膨らませ、飛来する砲弾やロケットを跳ね返す。",
        "enhanced_ko": "더 씽과 함께 플레이 시, 더 씽을 거대한 슬링샷처럼 고무줄로 장전해 초고속으로 발사합니다.",
        "enhanced_ja": "ザ・シングとチームアップ時、ザ・シングを巨大パチンコのようにゴムの張力で装填し、超高速で敵陣へ発射する。"
    },
    # 67. NAMOR - GAMMA MONSTRO (Partner: HULK)
    "GAMMA MONSTRO": {
        "base_ko": "삼지창을 휘둘러 수룡(Monstro)을 소환해 적을 공격합니다.",
        "base_ja": "三叉槍を振るい、巨大な水龍(モンストロ)を召喚して敵を攻撃する。",
        "enhanced_ko": "헐크와 함께 플레이 시, 소환된 몬스트로가 감마 방사능을 흡수하여 거대한 감마 괴물로 변이합니다.",
        "enhanced_ja": "ハルクとチームアップ時、召喚されたモンストロがガンマ線を吸収し、巨大なガンマ変異怪獣へと変貌する。"
    },
    # 68. NAMOR - CHILLING CHARISMA (Partner: LUNA SNOW)
    "CHILLING CHARISMA": {
        "base_ko": "발목 날개를 퍼덕이며 공중으로 날아올라 삼지창을 투척합니다.",
        "base_ja": "足首の翼を羽ばたかせて上空へ舞い上がり、三叉槍を投擲する。",
        "enhanced_ko": "루나 스노우와 함께 플레이 시, 투척된 삼지창이 얼음 기둥으로 변하여 착탄 지점 주변을 완전 빙결시킵니다.",
        "enhanced_ja": "ルナ・スノーとチームアップ時、投擲された三叉槍が氷柱へと変化し、着弾地点を完全凍結させる。"
    },
    # 69. PENI PARKER - VIBRANIUM MECH (Partner: BLACK PANTHER)
    "VIBRANIUM MECH": {
        "base_ko": "SP//dr 로봇 슈트의 거미줄 지뢰 설치 속도가 증가합니다.",
        "base_ja": "SP//drロボットスーツのスパイダーマイン設置速度が上昇する。",
        "enhanced_ko": "블랙 팬서와 함께 플레이 시, 슈트에 비브라늄 충격 흡수 장치가 장착되어 폭발 시 충격파를 방출합니다.",
        "enhanced_ja": "ブラックパンサーとチームアップ時、スーツにヴィブラニウム衝撃吸収装置が追加され、爆発時に衝撃波を放つ。"
    },
    # 70. PENI PARKER - ROCKET NETWORK (Partner: ROCKET RACCOON)
    "ROCKET NETWORK": {
        "base_ko": "사이버 거미줄 영역 내에서 페니의 이동 속도와 연사력이 증가합니다.",
        "base_ja": "電脳ネットエリア内において、ペニの移動速度と連射速度が上昇する。",
        "enhanced_ko": "로켓 라쿤과 함께 플레이 시, 로켓의 드론 비컨이 거미줄 네트워크와 연결되어 지뢰가 자동 재생성됩니다.",
        "enhanced_ja": "ロケット・ラクーンとチームアップ時、ドローンビーコンが蜘蛛の巣ネットワークと連動し、地雷が自動再生成される。"
    },
    # 71. PHOENIX - CIRCLE OF LIFE (Partner: WOLVERINE)
    "CIRCLE OF LIFE": {
        "base_ko": "피닉스 화염으로 적을 불태워 지속적인 피해를 입힙니다.",
        "base_ja": "フェニックスの炎で敵を焼き払い、継続ダメージを与える。",
        "enhanced_ko": "울버린과 함께 플레이 시, 불멸의 생명력이 공명하여 울버린이 빈사 상태에 빠지면 피닉스의 알로 부활시킵니다.",
        "enhanced_ja": "ウルヴァリンとチームアップ時、不滅の生命力が共鳴し、ウルヴァリンが致命傷を受けた際に不死鳥の卵から即座に蘇生する。"
    },
    # 72. PHOENIX - TELEKINETIC BEATDOWN (Partner: CYCLOPS)
    "TELEKINETIC BEATDOWN": {
        "base_ko": "염동력으로 적을 공중에 띄워 무방비 상태로 만듭니다.",
        "base_ja": "念動力で敵を宙に浮かせ、無防備な状態にする。",
        "enhanced_ko": "사이클롭스와 함께 플레이 시, 공중에 뜬 적에게 사이클롭스의 옵틱 광선이 집중 유도되어 폭발적인 연계 피해를 줍니다.",
        "enhanced_ja": "サイクロップスとチームアップ時、浮遊させた敵へオプティックビームが誘導収束し、壊滅的な連携打撃を与える。"
    },
    # 73. PSYLOCKE - MENTAL PROJECTION (Partner: EMMA FROST)
    "MENTAL PROJECTION": {
        "base_ko": "사이킥 표창을 던져 적중한 적에게 정신 균열을 일으킵니다.",
        "base_ja": "サイキック手裏剣を投擲し、命中した敵に精神亀裂を与える。",
        "enhanced_ko": "엠마 프로스트와 함께 플레이 시, 텔레파시 증폭기를 통해 표창이 적들 사이를 튕기며 연쇄 피해를 줍니다.",
        "enhanced_ja": "エマ・フロストとチームアップ時、テレパシー増幅器により手裏剣が敵の間を跳弾して連鎖ダメージを与える。"
    },
    # 74. PSYLOCKE - LIGHT & DARK DARTS (Partner: CLOAK & DAGGER)
    "LIGHT & DARK DARTS": {
        "base_ko": "사이킥 칼날로 돌진 베기를 수행하여 적을 관통합니다.",
        "base_ja": "サイキックブレードで突進斬撃を繰り出し、敵をすり抜けて切り裂く。",
        "enhanced_ko": "클록 & 대거와 함께 플레이 시, 돌진 경로에 빛과 어둠의 장막이 펼쳐져 아군을 숨겨주고 적을 실명시킵니다.",
        "enhanced_ja": "クローク＆ダガーとチームアップ時、突進軌道上に光と影のカーテンが展開され、味方を隠匿し敵を盲目にする。"
    },
    # 75. ROCKET RACCOON - MAMMALIAN BOND (Partner: SQUIRREL GIRL)
    "MAMMALIAN BOND": {
        "base_ko": "설치형 비컨 드론을 배치하여 아군에게 탄약을 보급합니다.",
        "base_ja": "設置型ビーコンドローンを展開し、味方へ弾薬を補給する。",
        "enhanced_ko": "스쿼럴 걸과 함께 플레이 시, 다람쥐 군단이 로켓의 폭탄을 운반하여 적진 깊숙이 배달 폭파시킵니다.",
        "enhanced_ja": "スクイレル・ガールとチームアップ時、リスの大群が爆弾を運搬し、敵陣深くに特攻投下して爆破する。"
    },
    # 76. ROCKET RACCOON - PLANET X PALS (Partner: GROOT)
    "PLANET X PALS": {
        "base_ko": "제트팩으로 공중에 도약하여 호버링 사격을 가합니다.",
        "base_ja": "ジェットパックで上空へ跳躍し、ホバリング乱射を行う。",
        "enhanced_ko": "그루트와 함께 플레이 시, 그루트의 어깨에 고정 탑승하여 받는 피해가 50% 감소하고 무한 사격 모드가 됩니다.",
        "enhanced_ja": "グルートとチームアップ時、グルートの肩に固定搭乗し、被ダメージが50%軽減され無限連射モードになる。"
    },
    # 77. ROGUE - MR. & MRS. X (Partner: GAMBIT)
    "MR. & MRS. X": {
        "base_ko": "적의 능력을 흡수할 때마다 자신의 방어력과 체력이 회복됩니다.",
        "base_ja": "敵の能力を吸収するたびに、自身の防御力と体力が回復する。",
        "enhanced_ko": "갬빗과 함께 플레이 시, 갬빗의 키네틱 에너지를 흡수하여 비행 돌진 시 지면을 초토화하는 폭발을 일으킵니다.",
        "enhanced_ja": "ガンビットとチームアップ時、ガンビットのキネティックエネルギーを吸収し、突進時に大爆発を引き起こす。"
    },
    # 78. ROGUE - EXPLOSIVE ENTANGLEMENT (Partner: DEADPOOL)
    "EXPLOSIVE ENTANGLEMENT": {
        "base_ko": "근접 강타 시 적의 공격력을 일정 시간 흡수해 약화시킵니다.",
        "base_ja": "近接強打時、敵の攻撃力を奪い取って弱体化させる。",
        "enhanced_ko": "데드풀과 함께 플레이 시, 데드풀의 불사 재생력을 복제하여 치명상을 입어도 즉시 체력을 100% 회복합니다.",
        "enhanced_ja": "デッドプールとチームアップ時、デッドプールの不死身再生力をコピーし、致命傷を受けても即座に全回復する。"
    },
    # 79. SCARLET WITCH - SORCERERS SUPREME (Partner: DOCTOR STRANGE)
    "SORCERERS SUPREME": {
        "base_ko": "혼돈 마법 구체를 발사하여 적중한 적에게 범위 피해를 줍니다.",
        "base_ja": "混沌の魔術球を発射し、命中した敵に範囲ダメージを与える。",
        "enhanced_ko": "닥터 스트레인지와 함께 플레이 시, 비샨티의 마법진이 열려 혼돈 마법이 무한 에너지 상태로 증폭됩니다.",
        "enhanced_ja": "ドクター・ストレンジとチームアップ時、ヴィシャンティの魔方陣が展開され、カオス魔術が無制限に出力増幅される。"
    },
    # 80. SCARLET WITCH - HEX FIREWORKS (Partner: MAGNETO)
    "HEX FIREWORKS": {
        "base_ko": "공중에 떠올라 혼돈의 힘으로 적들의 시야를 왜곡시킵니다.",
        "base_ja": "上空へ浮遊し、混沌の力で敵の視界を歪ませる。",
        "enhanced_ko": "매그니토와 함께 플레이 시, 매그니토가 모아둔 거대한 금속 유성에 헥스 에너지를 폭발시켜 전장을 멸망시킵니다.",
        "enhanced_ja": "マグニートーとチームアップ時、巨大な金属隕石にヘックスエネルギーを注入し、広範囲を一撃で壊滅させる。"
    },
    # 81. SPIDER-MAN - SYMBIOTE BOND (Partner: VENOM)
    "SYMBIOTE BOND": {
        "base_ko": "웹 스윙으로 고속 이동 시 다음 근접 공격의 피해량이 증가합니다.",
        "base_ja": "ウェブスイングで高速移動した際、次の近接攻撃のダメージが増加する。",
        "enhanced_ko": "베놈과 함께 플레이 시, 검은 심비오트 슈트가 활성화되어 스파이더 촉수가 사방의 적들을 꿰뚫습니다.",
        "enhanced_ja": "ヴェノムとチームアップ時、ブラックシンビオートスーツが起動し、無数の触手で周囲の敵を一網打尽にする。"
    },
    # 82. SPIDER-MAN - PARKER POWER-UP (Partner: PENI PARKER)
    "PARKER POWER-UP": {
        "base_ko": "거미줄을 던져 적을 묶고 끌어당깁니다.",
        "base_ja": "蜘蛛の糸を射出し、敵を拘束して引き寄せる。",
        "enhanced_ko": "페니 파커와 함께 플레이 시, 전기 거미줄(테이저 웹)이 장전되어 적중한 적을 감전시키고 기절시킵니다.",
        "enhanced_ja": "ペニ・パーカーとチームアップ時、電撃ウェブ(テーザー糸)が装填され、敵を感電させてスタンさせる。"
    },
    # 83. SQUIRREL GIRL - SQUIRREL MISSILE (Partner: IRON MAN)
    "SQUIRREL MISSILE": {
        "base_ko": "도토리 폭탄을 투척하여 적들에게 폭발 피해를 입힙니다.",
        "base_ja": "ドングリ爆弾を投げつけ、敵に爆発ダメージを与える。",
        "enhanced_ko": "아이언맨과 함께 플레이 시, 다람쥐 티피토에게 미니 아크 리액터 아머를 입혀 적에게 유도 미사일로 발사합니다.",
        "enhanced_ja": "アイアンマンとチームアップ時、リスのティッピー・トゥにミニリアクタースーツを着せ、誘導ミサイルとして射出する。"
    },
    # 84. SQUIRREL GIRL - ESU ALUMNUS (Partner: SPIDER-MAN)
    "ESU ALUMNUS": {
        "base_ko": "다람쥐 꼬리를 사용해 공중에서 높이 튀어오릅니다.",
        "base_ja": "リスの巨大な尻尾の弾力を使って空中へ高く飛び跳ねる。",
        "enhanced_ko": "스파이더맨과 함께 플레이 시, 거미줄 슬링을 꼬리에 감아 초고속으로 전장을 가로지르는 콤보를 구사합니다.",
        "enhanced_ja": "スパイダーマンとチームアップ時、ウェブスリングを尻尾に結びつけ、超高速で戦場を縦横無尽に跳び回る。"
    },
    # 85. STAR-LORD - FLORA MUNITIONS (Partner: GROOT)
    "FLORA MUNITIONS": {
        "base_ko": "뒤틀린 가시 씨앗을 전방에 던져 빠르게 싹을 틔우고 덩굴 덫을 생성합니다. 덫을 밟은 적은 피해를 입고 속박(Root)됩니다.",
        "base_ja": "ねじれた茨の種を前方へ投げ、急速に根を張らせてトラップを設置する。罠を踏んだ敵はダメージを受け移動不能(拘束)になる。",
        "enhanced_ko": "그루트와 함께 플레이 시, 설치되는 덩굴 덫의 개수가 증가하고 적이 덫을 밟았을 때 가해지는 피해량이 증폭됩니다.",
        "enhanced_ja": "グルートとチームアップ時、展開される茨の罠の数が増加し、罠を踏んだ敵に与えるダメージが大幅に強化される。"
    },
    # 86. STAR-LORD - STAR-SOUL (Partner: ADAM WARLOCK)
    "STAR-SOUL": {
        "base_ko": "로켓 부츠를 사용해 모든 방향으로 자유롭게 공중 회피합니다.",
        "base_ja": "ロケットブーツを駆使し、全方位へ素早く空中ダッシュ回避を行う。",
        "enhanced_ko": "아담 워록과 함께 플레이 시, 영혼 재생 에너지를 받아 엘리멘탈 블래스터 사격 시 탄약이 자동 보충됩니다.",
        "enhanced_ja": "アダム・ウォーロックとチームアップ時、魂の再生エネルギーを受け、ブラスター乱射時の弾薬が自動補給される。"
    },
    # 87. STORM - GOD OF THUNDER (Partner: THOR)
    "GOD OF THUNDER": {
        "base_ko": "날씨 제어 오라를 발동하여 주변 아군의 이동 속도를 올려줍니다.",
        "base_ja": "天候制御オーラを展開し、周囲の味方の移動速度を上昇させる。",
        "enhanced_ko": "토르와 함께 플레이 시, 토르의 번개가 스톰의 번개 구름에 번져 벼락의 공격력과 기절 지속 시간이 대폭 상승합니다.",
        "enhanced_ja": "ソーとチームアップ時、ソーの雷撃が嵐の雲に引火し、落雷の威力とスタン持続時間が劇的に上昇する。"
    },
    # 88. STORM - JAWS OF FATE (Partner: JEFF THE LAND SHARK)
    "JAWS OF FATE": {
        "base_ko": "돌풍을 일으켜 적들을 공중에 띄우고 밀쳐냅니다.",
        "base_ja": "突風を巻き起こし、敵を上空へ巻き上げてノックバックする。",
        "enhanced_ko": "제프 더 랜드 샤크와 함께 플레이 시, 회오리바람 속에 거대한 물보라가 휘몰아쳐 적들을 소용돌이 속에 가둡니다.",
        "enhanced_ja": "ジェフ・ザ・ランド・シャークとチームアップ時、竜巻の中に大水流が巻き込まれ、敵を水渦の中に閉じ込める。"
    },
    # 89. THE PUNISHER - BESTIAL HUNT (Partner: WOLVERINE)
    "BESTIAL HUNT": {
        "base_ko": "연막탄을 투척하여 적의 시야를 차단하고 자신의 위치를 숨깁니다.",
        "base_ja": "スモーク弾を投擲し、敵の射線を遮断して自身の姿を隠す。",
        "enhanced_ko": "울버린과 함께 플레이 시, 야수의 감각이 깨어나 연막 속에서도 적의 심장박동을 감지하고 치명타를 가합니다.",
        "enhanced_ja": "ウルヴァリンとチームアップ時、獣の感覚が研ぎ澄まされ、煙幕の中でも敵の急所を完全に捕捉して痛打を与える。"
    },
    # 90. THE PUNISHER - AMMO OVERLOAD (Partner: ROCKET RACCOON)
    "AMMO OVERLOAD": {
        "base_ko": "샷건과 돌격소총을 빠르게 전환하며 즉시 재장전합니다.",
        "base_ja": "ショットガンとライフルを素早く切り替え、即座にリロードを行う。",
        "enhanced_ko": "로켓 라쿤과 함께 플레이 시, 로켓의 특수 탄약 벨트가 연결되어 일정 시간 탄약 소모 없이 무한 난사를 퍼붓습니다.",
        "enhanced_ja": "ロケット・ラクーンとチームアップ時、特殊給弾ベルトが接続され、一定時間弾薬無消費で無限連射を叩き込む。"
    },
    # 91. THE THING - TWO IN ONE (Partner: HUMAN TORCH)
    "TWO IN ONE": {
        "base_ko": "지면을 두드려 단단한 암석 보호막을 생성합니다.",
        "base_ja": "地面を叩いて自身の周囲に強固な岩石シールドを纏う。",
        "enhanced_ko": "휴먼 토치와 함께 플레이 시, 휴먼 토치가 바위를 불태워 불타는 용암 운석 상태로 돌진하게 만듭니다.",
        "enhanced_ja": "ヒューマン・トーチとチームアップ時、溶岩のように岩石が灼熱化し、燃え盛る隕石突進を放つ。"
    },
    # 92. THE THING - UNBREAKABLE FORCES (Partner: INVISIBLE WOMAN)
    "UNBREAKABLE FORCES": {
        "base_ko": "적의 군중 제어 공격을 받을 때 방어력이 일시적으로 급상승합니다.",
        "base_ja": "行動阻害攻撃を受けた際、一時的に防御力が急上昇する。",
        "enhanced_ko": "인비저블 우먼과 함께 플레이 시, 둘의 힘이 합쳐져 아군 전체를 감싸는 난공불락의 역장 돔을 펼칩니다.",
        "enhanced_ja": "インビジブル・ウーマンとチームアップ時、味方全体を包み込む鉄壁の不可視ドームバリアを展開する。"
    },
    # 93. THOR - RAGNAROK REBIRTH (Partner: LOKI)
    "RAGNAROK REBIRTH": {
        "base_ko": "묠니르를 휘둘러 아군에게 전격 보호막을 씌워줍니다.",
        "base_ja": "ムジョルニアを振り回し、味方に雷のシールドを付与する。",
        "enhanced_ko": "로키와 함께 플레이 시, 라그나로크의 운명이 교차하여 번개 폭풍 속에서 쓰러진 아군을 부활시킵니다.",
        "enhanced_ja": "ロキとチームアップ時、ラグナロクの運命が交錯し、雷雲の中で倒れた味方を復活させる。"
    },
    # 94. THOR - DIVINE ARMORY (Partner: CAPTAIN AMERICA)
    "DIVINE ARMORY": {
        "base_ko": "천둥의 힘으로 번개 투사체를 날려 적들을 감전시킵니다.",
        "base_ja": "雷神の力で稲妻の矢を撃ち出し、敵を感電させる。",
        "enhanced_ko": "캡틴 아메리카와 함께 플레이 시, 캡틴의 방패를 묠니르로 가격하여 전방을 초토화하는 음속 충격파를 방출합니다.",
        "enhanced_ja": "キャプテン・アメリカとチームアップ時、シールドをムジョルニアで強打し、超音速の衝撃波で前方全域を粉砕する。"
    },
    # 95. THE HOOD - Chaos Collision (Partner: SCARLET WITCH)
    "Chaos Collision": {
        "base_ko": "지옥불 탄환을 발사하여 적중한 적에게 암흑 폭발을 일으킵니다.",
        "base_ja": "地獄の業火弾を放ち、着弾した敵に暗黒爆発を引き起こす。",
        "enhanced_ko": "스칼렛 위치와 함께 플레이 시, 혼돈 마법이 암흑 탄환에 주입되어 적들의 현실 인식을 붕괴시키고 공포에 질리게 합니다.",
        "enhanced_ja": "スカーレット・ウィッチとチームアップ時、混沌魔術が融合して敵の現実知覚を崩壊させ、恐怖状態に陥れる。"
    },
    # 96. THE HOOD - New Moon's Shadow (Partner: MOON KNIGHT)
    "New Moon's Shadow": {
        "base_ko": "악마의 망토로 공중에 숨어 기습 위치를 잡습니다.",
        "base_ja": "悪魔のマントで上空に身を隠し、奇襲のポジションを取る。",
        "enhanced_ko": "문나이트와 함께 플레이 시, 그믐달의 그림자가 전장을 뒤덮어 아군 전체의 발소리를 완전히 지워줍니다.",
        "enhanced_ja": "ムーンナイトとチームアップ時、新月の影が戦場を覆い、味方全体の足音と気配を完全に消去する。"
    },
    # 97. ULTRON - STARK PROTOCOL (Partner: IRON MAN)
    "STARK PROTOCOL": {
        "base_ko": "드론 센티널을 소환하여 아군을 엄호하고 치유 광선을 쏩니다.",
        "base_ja": "ドローンセンチネルを召喚し、味方を援護して回復ビームを照射する。",
        "enhanced_ko": "아이언맨과 함께 플레이 시, 스타크 인더스트리 프로토콜을 해킹하여 센티널의 공격력을 2배로 강화합니다.",
        "enhanced_ja": "アイアンマンとチームアップ時、スターク社のプロトコルをハッキングし、センチネルの火力を2倍に引き上げる。"
    },
    # 98. ULTRON - SP//DR SYNC (Partner: PENI PARKER)
    "SP//DR SYNC": {
        "base_ko": "나노봇 보호막을 생성하여 전방의 피해를 흡수합니다.",
        "base_ja": "ナノマシンバリアを展開し、前方のダメージを吸収する。",
        "enhanced_ko": "페니 파커와 함께 플레이 시, 사이버 거미줄 네트워크를 동기화하여 드론이 거미줄 위를 고속 기동합니다.",
        "enhanced_ja": "ペニ・パーカーとチームアップ時、電脳ネットを同期させ、ドローンが蜘蛛の巣の上を超高速で滑空機動する。"
    },
    # 99. VENOM - BLOOD LEECH (Partner: BLADE)
    "BLOOD LEECH": {
        "base_ko": "적을 심비오트 촉수로 강타하여 생명력을 흡수합니다.",
        "base_ja": "敵をシンビオートの触手で殴打し、生命力を吸収する。",
        "enhanced_ko": "블레이드와 함께 플레이 시, 흡혈 본능이 폭발하여 촉수 공격에 적중당한 모든 적에게 치명적인 과다출혈을 일으킵니다.",
        "enhanced_ja": "ブレイドとチームアップ時、吸血衝動が爆発し、触手打撃を受けた全敵に激しい過多出血を誘発する。"
    },
    # 100. VENOM - ABYSSAL FLAMES (Partner: THE HOOD)
    "ABYSSAL FLAMES": {
        "base_ko": "지면을 내리쳐 검은 심비오트 늪을 형성하여 적을 느리게 만듭니다.",
        "base_ja": "地面を叩き割って黒いシンビオートの沼を形成し、敵の足を奪う。",
        "enhanced_ko": "더 후드와 함께 플레이 시, 심비오트에 암흑 지옥불이 붙어 늪을 밟은 적을 불태워 녹여버립니다.",
        "enhanced_ja": "ザ・フッドとチームアップ時、シンビオートに黒炎が引火し、沼を踏んだ敵を焼き尽くす。"
    },
    # 101. WINTER SOLDIER - TIMELESS VETERANS (Partner: CAPTAIN AMERICA)
    "TIMELESS VETERANS": {
        "base_ko": "생체공학 의수로 강력한 펀치를 날려 전방의 적을 날려버립니다.",
        "base_ja": "生体工学義手で強烈な鉄拳を放ち、前方の敵を殴り飛ばす。",
        "enhanced_ko": "캡틴 아메리카와 함께 플레이 시, 캡틴이 던진 비브라늄 방패를 의수로 쳐내어 방향을 꺾는 트릭샷을 시전합니다.",
        "enhanced_ja": "キャプテン・アメリカとチームアップ時、飛来したシールドを義手で強打して跳弾軌道を操る連係射撃を行う。"
    },
    # 102. WINTER SOLDIER - EXPERT INSTINCT (Partner: HAWKEYE)
    "EXPERT INSTINCT": {
        "base_ko": "돌격소총 사격 시 반동이 감소하고 탄착군이 좁아집니다.",
        "base_ja": "アサルトライフル射撃時の反動が軽減され、集弾率が向上する。",
        "enhanced_ko": "호크아이와 함께 플레이 시, 호크아이의 정찰 센서와 연동되어 연막 뒤의 적을 완전 조준 사격합니다.",
        "enhanced_ja": "ホークアイとチームアップ時、索敵センサーと同期し、煙幕や障害物の背後の敵を正確に精密狙撃する。"
    },
    # 103. WHITE FOX - LUCKY LOAN (Partner: BLACK CAT)
    "LUCKY LOAN": {
        "base_ko": "블랙 캣으로부터 생명의 보옥을 받아 영혼 꼬리 에너지를 회복하고 전방위로 구미호의 오라를 방출합니다. 아군에게는 이동 속도와 치유를, 적에게는 피해와 감속을 줍니다.",
        "base_ja": "ブラックキャットから生命のオーブを受け取り、尾の霊力を回復して全方位へ九尾のオーラを放つ。味方には移動速度と治癒を、敵にはダメージと減速を与える。",
        "enhanced_ko": "블랙 캣과 함께 플레이 시, 보옥 사용 시 일정 시간 영혼 꼬리 에너지가 소모되지 않아 유령 쇄도와 구미호 각성을 무제한 사용할 수 있습니다.",
        "enhanced_ja": "ブラックキャットとチームアップ時、オーブ使用後一定時間霊力が消費されなくなり、狐形態の覚醒スキルを無制限に発動可能になる。"
    },
    # 104. WHITE FOX - PSIONIC FOX (Partner: PSYLOCKE)
    "PSIONIC FOX": {
        "base_ko": "구미호의 발톱으로 연속 할퀴기를 가해 피해를 입힙니다.",
        "base_ja": "九尾の爪で連続引っかき攻撃を繰り出し、敵を切り裂く。",
        "enhanced_ko": "사일록과 함께 플레이 시, 사이킥 칼날이 여우 발톱에 깃들어 타격 시 적의 정신을 혼미하게 만듭니다.",
        "enhanced_ja": "サイロックとチームアップ時、サイキックブレードが爪に宿り、攻撃を受けた敵の精神を麻痺させる。"
    },
    # 105. WOLVERINE - BLAST SLASH (Partner: PHOENIX)
    "BLAST SLASH": {
        "base_ko": "아다만티움 클로로 전방을 베어 넘기며 적에게 출혈 피해를 입힙니다.",
        "base_ja": "アダマンチウムの爪で前方を切り裂き、敵に出血ダメージを与える。",
        "enhanced_ko": "피닉스와 함께 플레이 시, 클로에 불멸의 피닉스 화염이 둘러져 베기 공격이 지옥불 파동을 일으킵니다.",
        "enhanced_ja": "フェニックスとチームアップ時、爪にフェニックスの業火が纏われ、斬撃が炎の衝撃波へと昇華する。"
    },
    # 106. WOLVERINE - PAIR OF THREES (Partner: DEADPOOL)
    "PAIR OF THREES": {
        "base_ko": "치명상을 입었을 때 아다만티움 골격이 버텨주어 잠시 동안 죽지 않고 버팁니다.",
        "base_ja": "致命傷を受けた際、アダマンチウム骨格が耐え抜き、短時間死亡を免れる。",
        "enhanced_ko": "데드풀과 함께 플레이 시, 둘의 힐링 팩터가 공명하여 주변 적들을 도발하고 서로의 체력을 2배 속도로 회복시킵니다.",
        "enhanced_ja": "デッドプールとチームアップ時、二人の治癒因子が共鳴し、周囲の敵を挑発しつつ互いの体力を超高速回復させる。"
    },
    # 107. Default Fallback
    "DEFAULT": {
        "base_ko": "팀업 파트너 없이도 솔로로 상시 적용되는 기본 패시브 효과입니다.",
        "base_ja": "チームアップ相手がいなくてもソロで常時発動する基本パッシブ効果。",
        "enhanced_ko": "시너지 파트너 영웅과 함께 플레이 시 발동되는 강력한 강화 효과입니다.",
        "enhanced_ja": "シナジー対象ヒーローとチームアップ時に発動する強力な強化効果。"
    }
}

def build_teamups_json():
    with open('scratch/teamups_pairs.json', 'r', encoding='utf-8') as f:
        pairs = json.load(f)

    result = {}
    matched = 0

    for item in pairs:
        raw_desc = item['raw_desc']
        clean_desc = re.sub(r'\s+', ' ', raw_desc).strip()
        loadout = item['loadout'].strip()

        # Find translation by loadout name
        t = TEAMUP_TRANSLATIONS.get(loadout)
        if not t:
            # Fallback search by base
            for k, val in TEAMUP_TRANSLATIONS.items():
                if k.lower() in loadout.lower():
                    t = val
                    break

        if not t:
            print(f"Warning: No translation found for teamup '{loadout}', using fallback")
            t = TEAMUP_TRANSLATIONS["DEFAULT"]
        else:
            matched += 1

        entry = {
            "loadout_name": loadout,
            "hero": item['hero'],
            "base": {
                "ko": t["base_ko"],
                "ja": t["base_ja"]
            },
            "enhanced": {
                "ko": t["enhanced_ko"],
                "ja": t["enhanced_ja"]
            },
            "full": {
                "ko": f"기본 효과: {t['base_ko']}\n강화 효과: {t['enhanced_ko']}",
                "ja": f"基本効果: {t['base_ja']}\n強化効果: {t['enhanced_ja']}"
            }
        }

        # Key by clean_desc
        result[clean_desc] = entry
        # Also key by raw_desc
        result[raw_desc] = entry

    os.makedirs('data/translations', exist_ok=True)
    with open('data/translations/teamups.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Generated data/translations/teamups.json: matched {matched}/{len(pairs)} ({len(result)} keys)")

if __name__ == '__main__':
    build_teamups_json()
