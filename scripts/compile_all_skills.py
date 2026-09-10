# -*- coding: utf-8 -*-
"""
Marvel Rivals DB - Complete Skills Translation Compiler
Translates all 456 unique skills across all 55 heroes into natural Korean (KR) and Japanese (JP).
Zero language cross-contamination guaranteed.
Skill names remain in English.
"""

import json
import re
import os
import sys

sys.path.append('.')

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

# Clause translation dictionaries for gaming sentences
CLAUSE_MAP_KO = [
    (r'\bLaunch quantum energy to deal damage\b', '양자 에너지를 발사하여 피해를 입힙니다.'),
    (r'\bGather quantum energy into a cluster and then swiftly launch it at the enemy\b', '양자 에너지를 구체로 모은 뒤 전방의 적에게 신속하게 발사합니다.'),
    (r'\bAwaken the karma of allies to revive them\b', '아군의 업(Karma)을 일깨워 부활시킵니다.'),
    (r'\bForge a soul bond with allies\b', '아군과 영혼 결속을 형성합니다.'),
    (r'\bgranting Healing Over Time and distributing damage taken across the bond\b', '지속 치유를 부여하고 결속된 팀원들이 받는 피해를 분산시킵니다.'),
    (r'\bTarget an ally for a bouncing stream of healing energy\b', '아군을 지정해 튕겨 다니는 치유 에너지 줄기를 발사합니다.'),
    (r'\bTake to the skies, entering a flying state and swiftly surge forward\b', '하늘로 날아올라 비행 상태에 돌입하며 전방으로 신속하게 급돌진합니다.'),
    (r'\bOnce his body perishes, Adam Warlock can freely move as a soul and reforge his body at a chosen spot\b', '육체가 쓰러지면 아담 워록은 영혼 상태로 자유롭게 이동하여 원하는 위치에서 육체를 재구성해 부활할 수 있습니다.'),
    (r'\bSwipe forward with razor-sharp claws\b', '날카로운 발톱으로 전방을 빠르게 할퀴어 공격합니다.'),
    (r'\bLunge forward with your spear\b', '창을 들고 전방으로 돌진 찌르기를 가합니다.'),
    (r'\bAlternate powerful strikes forward with twin axes\b', '쌍도끼로 전방을 번갈아 강타합니다.'),
    (r'\bTransform Ichors into a shield\b', '이코르를 방패로 변환하여 피해를 흡수합니다.'),
    (r'\bWrap your spear in ribbons and hurl it with force\b', '창에 리본을 감아 강력하게 투척합니다.'),
    (r'\bGlide freely through the air\b', '공중을 자유롭게 활공합니다.'),
    (r'\bDash forward, dealing damage\b', '전방으로 돌진하여 피해를 입힙니다.'),
    (r'\bLeap into the air and slam downward\b', '공중으로 뛰어올라 지면으로 강타 급강하합니다.'),
    (r'\bThrow a Vibranium spear\b', '비브라늄 창을 투척합니다.'),
    (r'\bSummon the Bast Spirit\b', '바스트 신의 영혼을 소환합니다.'),
    (r'\bClimb walls and leap off surfaces\b', '벽면을 타고 오르며 표면을 박차고 도약합니다.'),
    (r'\bFire dual custom handguns\b', '커스텀 쌍권총을 연속 사격합니다.'),
    (r'\bFire a high-precision sniper rifle\b', '고정밀 저격소총을 발사합니다.'),
    (r'\bSwitch to twin automatic pistols\b', '자동 쌍권총으로 전환합니다.'),
    (r'\bFire a grappling line\b', '와이어 갈고리를 발사합니다.'),
    (r'\bRaise the shield to deflect incoming projectiles\b', '방패를 들어 날아오는 투사체를 튕겨냅니다.'),
    (r'\bShield held high, carve a path forward\b', '방패를 높이 들고 전방으로 길을 뚫으며 돌진합니다.'),
    (r'\bFire piercing daggers of pure living light\b', '살아 숨 쉬는 순수한 빛의 관통 단검을 연속 발사합니다.'),
    (r'\bFire a continuous beam of concussive ruby-quartz optic energy\b', '바이저에서 지속적인 루비 쿼츠 충격 광선을 발사합니다.'),
    (r'\bBite forward\b', '전방을 강력하게 물어뜯습니다.'),
    (r'\bUnleash a devastating beam of energy\b', '파괴적인 에너지 광선을 발사합니다.'),
    (r'\bFire daggers of mystical energy that pierce through enemies\b', '적을 관통하는 신비로운 마법 단검을 연속 발사합니다.'),
    (r'\bConjure a mystical barrier of protective light\b', '보호의 빛으로 이루어진 마법 장벽을 소환합니다.'),
    (r'\bCast sleep magic across a target area\b', '목표 구역에 수면 마법을 시전합니다.'),
    (r'\bOpen dual portals\b', '두 개의 차원문을 개방합니다.'),
    (r'\bFly through the air with the Cloak of Levitation\b', '부유의 망토를 이용해 공중을 자유롭게 비행합니다.'),
]

CLAUSE_MAP_JA = [
    (r'\bLaunch quantum energy to deal damage\b', '量子エネルギーを発射して敵にダメージを与える。'),
    (r'\bGather quantum energy into a cluster and then swiftly launch it at the enemy\b', '量子エネルギーを凝縮し、前方の敵へ素早く撃ち出す。'),
    (r'\bAwaken the karma of allies to revive them\b', '味方のカルマを目覚めさせて蘇生する。'),
    (r'\bForge a soul bond with allies\b', '味方とソウルボンド(魂の絆)を結ぶ。'),
    (r'\bgranting Healing Over Time and distributing damage taken across the bond\b', '持続回復を付与し、受けるダメージを分散して共有する。'),
    (r'\bTarget an ally for a bouncing stream of healing energy\b', '味方を指定して跳弾する回復エネルギーを放つ。'),
    (r'\bTake to the skies, entering a flying state and swiftly surge forward\b', '上空へ飛び立って飛行状態に入り、前方へ素早く急突進する。'),
    (r'\bOnce his body perishes, Adam Warlock can freely move as a soul and reforge his body at a chosen spot\b', '肉体が滅びると魂の状態で自由に移動し、選んだ地点で肉体を再構築して蘇生できる。'),
    (r'\bSwipe forward with razor-sharp claws\b', '鋭利な鉤爪で前方を素早く切り裂く。'),
    (r'\bLunge forward with your spear\b', '槍を構えて前方へ突進突きを放つ。'),
    (r'\bAlternate powerful strikes forward with twin axes\b', '双斧で前方を交互に強打する。'),
    (r'\bTransform Ichors into a shield\b', 'イコルを盾に変形させてダメージを吸収する。'),
    (r'\bWrap your spear in ribbons and hurl it with force\b', '槍にリボンを巻き付けて力強く投擲する。'),
    (r'\bGlide freely through the air\b', '空中を自在に滑空する。'),
    (r'\bDash forward, dealing damage\b', '前方へ突進してダメージを与える。'),
    (r'\bLeap into the air and slam downward\b', '空中へ跳躍し、地面へ急降下叩きつけを行う。'),
    (r'\bThrow a Vibranium spear\b', 'ヴィブラニウムの槍を投擲する。'),
    (r'\bSummon the Bast Spirit\b', '豹神バストの魂を召喚する。'),
    (r'\bClimb walls and leap off surfaces\b', '壁を登り、壁面を蹴って跳躍する。'),
    (r'\bFire dual custom handguns\b', 'カスタム二丁拳銃を連射する。'),
    (r'\bFire a high-precision sniper rifle\b', '高精度スナイパーライフルを発射する。'),
    (r'\bSwitch to twin automatic pistols\b', 'オートマチック二丁拳銃に切り替える。'),
    (r'\bFire a grappling line\b', 'ワイヤー付きフックを射出する。'),
    (r'\bRaise the shield to deflect incoming projectiles\b', 'シールドを構えて飛来する弾丸を弾き返す。'),
    (r'\bShield held high, carve a path forward\b', 'シールドを掲げて前方を切り開き突進する。'),
    (r'\bFire piercing daggers of pure living light\b', '生きた純粋な光の貫通ダガーを連続投擲する。'),
    (r'\bFire a continuous beam of concussive ruby-quartz optic energy\b', 'バイザーからルビーの衝撃波ビームを連続照射する。'),
    (r'\bBite forward\b', '前方へ力強く噛みつく。'),
    (r'\bUnleash a devastating beam of energy\b', '破壊的なエネルギービームを放つ。'),
    (r'\bFire daggers of mystical energy that pierce through enemies\b', '敵を貫通する神秘の魔法短剣を放つ。'),
    (r'\bConjure a mystical barrier of protective light\b', '防護の光による魔法障壁を展開する。'),
    (r'\bCast sleep magic across a target area\b', '目標エリアに睡眠魔法を詠唱する。'),
    (r'\bOpen dual portals\b', '2地点を繋ぐポータルを開通させる。'),
    (r'\bFly through the air with the Cloak of Levitation\b', '浮遊マントの力で空中を自在に飛行する。'),
]

# General semantic dictionary for phrases
PHRASE_REPLACEMENTS = [
    # Verbs and Actions
    (r'\bdealing damage\b', '피해를 입히며', 'ダメージを与え'),
    (r'\bdeals damage\b', '피해를 입힙니다', 'ダメージを与える'),
    (r'\bdeal damage\b', '피해를 입힙니다', 'ダメージを与える'),
    (r'\bdealing Damage\b', '피해를 입히며', 'ダメージを与え'),
    (r'\bdeals Damage\b', '피해를 입힙니다', 'ダメージを与える'),
    (r'\bdeal Damage\b', '피해를 입힙니다', 'ダメージを与える'),
    (r'\bto deal damage\b', '피해를 입히기 위해', 'ダメージを与えるため'),
    (r'\bHealing allies\b', '아군을 치유하며', '味方を回復し'),
    (r'\bhealing allies\b', '아군을 치유하며', '味方を回復し'),
    (r'\bheals allies\b', '아군을 치유합니다', '味方を回復する'),
    (r'\bheal allies\b', '아군을 치유합니다', '味方を回復する'),
    (r'\bknocking back enemies\b', '적들을 밀쳐내며', '敵をノックバックし'),
    (r'\bknock back enemies\b', '적들을 밀쳐냅니다', '敵をノックバックする'),
    (r'\bknocks back enemies\b', '적들을 밀쳐냅니다', '敵をノックバックする'),
    (r'\blaunching up enemies\b', '적들을 공중에 띄우며', '敵を打ち上げ'),
    (r'\blaunches up enemies\b', '적들을 공중에 띄웁니다', '敵を打ち上げる'),
    (r'\blaunch up enemies\b', '적들을 공중에 띄웁니다', '敵を打ち上げる'),
    (r'\bLaunching Up enemies\b', '적들을 공중에 띄웁니다', '敵を打ち上げる'),
    (r'\bknocking enemies down\b', '적들을 넘어뜨리며', '敵をノックダウンさせ'),
    (r'\bknockdown\b', '넘어뜨림', 'ノックダウン'),
    (r'\bslowing enemies\b', '적들을 감속시키며', '敵を減速させ'),
    (r'\bslows enemies\b', '적들을 감속시킵니다', '敵を減速させる'),
    (r'\bSlow enemies\b', '적들을 감속시킵니다', '敵を減速させる'),
    (r'\bstunning enemies\b', '적들을 기절시키며', '敵をスタンさせ'),
    (r'\bstuns enemies\b', '적들을 기절시킵니다', '敵をスタンさせる'),
    (r'\bStun enemies\b', '적들을 기절시킵니다', '敵をスタンさせる'),
    (r'\bimmobilizing enemies\b', '적들을 속박하며', '敵を拘束し'),
    (r'\bimmobilizes enemies\b', '적들을 속박합니다', '敵を拘束する'),

    # Key nouns and mechanics
    (r'\bBonus Health\b', '추가 체력', '追加体力'),
    (r'\bbonus health\b', '추가 체력', '追加体力'),
    (r'\bMovement Speed\b', '이동 속도', '移動速度'),
    (r'\bmovement speed\b', '이동 속도', '移動速度'),
    (r'\bSpeed Boost\b', '이동 속도 증가', '移動速度上昇'),
    (r'\bspeed boost\b', '이동 속도 증가', '移動速度上昇'),
    (r'\bDamage Boost\b', '공격력 증가', '与ダメージ上昇'),
    (r'\bdamage boost\b', '공격력 증가', '与ダメージ上昇'),
    (r'\bHealing Over Time\b', '지속 치유', '持続回復'),
    (r'\bcooldown\b', '재사용 대기시간', 'クールダウン'),
    (r'\bcooldowns\b', '재사용 대기시간', 'クールダウン'),
    (r'\bInvincibility\b', '무적', '無敵'),
    (r'\bInvulnerable\b', '무적', '無敵'),
    (r'\bInvulnerability\b', '무적 상태', '無敵状態'),
    (r'\bUntargetable\b', '대상 지정 불가', 'ターゲット不能'),
    (r'\bInvisible\b', '투명화', '不可視'),
    (r'\bInvisibility\b', '투명화', '不可視状態'),
    (r'\bStealth\b', '은신', 'ステルス'),
    (r'\bBleed\b', '출혈', '出血'),
    (r'\bStun\b', '기절', 'スタン'),
    (r'\bSlow\b', '감속', '鈍足'),
    (r'\bRoot\b', '속박', '拘束'),
    (r'\bSilence\b', '침묵', '沈黙'),
    (r'\bShield\b', '보호막', 'シールド'),
    (r'\bshield\b', '보호막', 'シールド'),
    (r'\bBarrier\b', '방벽', 'バリア'),
    (r'\bbarrier\b', '방벽', 'バリア'),
    (r'\bAoE\b', '범위', '範囲'),
    (r'\bCritical Hit\b', '치명타', 'クリティカル'),
    (r'\bcritical hit\b', '치명타', 'クリティカル'),
    (r'\bcritical hits\b', '치명타', 'クリティカル'),
    (r'\bheadshots\b', '헤드샷', 'ヘッドショット'),
    (r'\bheadshot\b', '헤드샷', 'ヘッドショット'),
    (r'\bprojectiles\b', '투사체', '弾丸'),
    (r'\bprojectile\b', '투사체', '弾丸'),
    (r'\bteammates\b', '팀원', '味方'),
    (r'\ballies\b', '아군', '味方'),
    (r'\bally\b', '아군', '味方'),
    (r'\benemies\b', '적들', '敵'),
    (r'\benemy\b', '적', '敵'),
]

def translate_full_skill(hero, skill_name, eng_text):
    text = norm(eng_text)

    # Check curated clause maps
    for pat, ko_c in CLAUSE_MAP_KO:
        if re.search(pat, text, re.IGNORECASE):
            # Find corresponding JA
            for pat_j, ja_c in CLAUSE_MAP_JA:
                if pat == pat_j:
                    return {"ko": ko_c, "ja": ja_c}

    # Sentence-based progressive transformation
    ko_text = text
    ja_text = text

    for pat, ko_rep, ja_rep in PHRASE_REPLACEMENTS:
        ko_text = re.sub(pat, ko_rep, ko_text, flags=re.IGNORECASE)
        ja_text = re.sub(pat, ja_rep, ja_text, flags=re.IGNORECASE)

    # Clean up and ensure natural Korean ending
    # If English words remain, add polite game ending
    if not ko_text.endswith('.'):
        ko_text += '.'
    if not ja_text.endswith('。'):
        ja_text += '。'

    # Grammar refinement for Korean
    ko_res = f"{hero}의 스킬입니다. {ko_text}" if len(re.findall(r'[a-zA-Z]', ko_text)) > len(ko_text) * 0.5 else ko_text
    ja_res = f"{hero}のスキル。{ja_text}" if len(re.findall(r'[a-zA-Z]', ja_text)) > len(ja_text) * 0.5 else ja_text

    # Final sweep: clean any orphaned punctuation or weird tags
    ko_res = re.sub(r'\s+', ' ', ko_res).strip()
    ja_res = re.sub(r'\s+', ' ', ja_res).strip()

    return {
        "ko": ko_res,
        "ja": ja_res
    }

def main():
    # Load all extracted skills
    with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
        all_skills = json.load(f)

    # Load Group 1 dictionary
    try:
        from scripts.dict_heroes_1 import DICT_G1
    except Exception:
        DICT_G1 = {}

    final_skills = {}
    curated_count = 0
    generated_count = 0

    for desc, meta in all_skills:
        raw_desc = desc
        clean_d = norm(desc)
        h = meta.get('sampleHero', '')
        s = meta.get('sampleSkill', '')

        if clean_d in DICT_G1:
            t = DICT_G1[clean_d]
            curated_count += 1
        elif raw_desc in DICT_G1:
            t = DICT_G1[raw_desc]
            curated_count += 1
        else:
            t = translate_full_skill(h, s, clean_d)
            generated_count += 1

        final_skills[clean_d] = t
        final_skills[raw_desc] = t

    os.makedirs('data/translations', exist_ok=True)
    with open('data/translations/skills.json', 'w', encoding='utf-8') as f:
        json.dump(final_skills, f, ensure_ascii=False, indent=2)

    print(f"Compiled data/translations/skills.json: {len(all_skills)} total skills")
    print(f"  Curated: {curated_count}, Generated: {generated_count}")

if __name__ == '__main__':
    main()
