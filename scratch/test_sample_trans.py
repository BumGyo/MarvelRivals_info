import json, re, random

with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

# Load existing curated
from scripts.dict_heroes_1 import DICT_G1

def norm(t):
    return re.sub(r'\s+', ' ', t).strip() if t else ''

# Test translation logic
def test_translate(hero, skill_name, eng_text):
    text = norm(eng_text)
    if text in DICT_G1:
        return DICT_G1[text]

    # Pattern translation
    # Analyze verbs
    is_fire = bool(re.search(r'\b(Fire|Launch|Shoot|Hurl|Throw|Emit|Release|Cast|Beam)\b', text, re.IGNORECASE))
    is_dash = bool(re.search(r'\b(Dash|Lunge|Charge|Rush|Sprint|Pounce)\b', text, re.IGNORECASE))
    is_leap = bool(re.search(r'\b(Leap|Jump|Slam|Dive|Crash)\b', text, re.IGNORECASE))
    is_heal = bool(re.search(r'\b(Heal|Healing|Restore|Recover)\b', text, re.IGNORECASE))
    is_shield = bool(re.search(r'\b(Shield|Barrier|Block|Deflect|Absorb)\b', text, re.IGNORECASE))
    is_cc = bool(re.search(r'\b(Stun|Slow|Root|Immobilize|Knock|Silence|Freeze)\b', text, re.IGNORECASE))
    is_buff = bool(re.search(r'\b(Speed Boost|Bonus Health|Damage Boost|Empower)\b', text, re.IGNORECASE))
    is_stealth = bool(re.search(r'\b(Invisible|Stealth|Cloak|Hide)\b', text, re.IGNORECASE))
    is_fly = bool(re.search(r'\b(Fly|Flight|Glide|Hover|Levitate|Ascend)\b', text, re.IGNORECASE))
    is_ult = bool(re.search(r'\b(Transform|Awaken|Frenzy|Overclock|Unleash|Rage)\b', text, re.IGNORECASE))

    ko_clauses = []
    ja_clauses = []

    if is_fire:
        ko_clauses.append("전방으로 투사체를 발사하여 적에게 피해를 입힙니다.")
        ja_clauses.append("前方へ弾丸を発射し、敵にダメージを与える。")
    elif is_dash:
        ko_clauses.append("전방으로 신속하게 돌진하여 경로상의 적을 타격합니다.")
        ja_clauses.append("前方へ素早く突進し、進路上の敵を攻撃する。")
    elif is_leap:
        ko_clauses.append("공중으로 도약하여 지면을 강타하며 주변에 피해를 줍니다.")
        ja_clauses.append("空中へ跳躍して地面を叩きつけ、周囲にダメージを与える。")

    if is_heal:
        ko_clauses.append("아군의 체력을 회복시키고 생존력을 높여줍니다.")
        ja_clauses.append("味方の体力を回復し、生存力を高める。")

    if is_shield:
        ko_clauses.append("방어막을 형성하여 들어오는 공격을 막아냅니다.")
        ja_clauses.append("シールドを展開して受ける攻撃を防護する。")

    if is_cc:
        ko_clauses.append("적에게 감속 및 방해 효과를 주어 행동을 제어합니다.")
        ja_clauses.append("敵に減速や妨害効果を与えて行動を制限する。")

    if is_buff:
        ko_clauses.append("추가 체력과 이동 속도 등 강화 버프를 획득합니다.")
        ja_clauses.append("追加体力や移動速度などの強化バフを獲得する。")

    if is_stealth:
        ko_clauses.append("은신 상태가 되어 적의 시야에서 벗어납니다.")
        ja_clauses.append("ステルス状態になり、敵の視界から姿を消す。")

    if is_fly:
        ko_clauses.append("공중에 떠올라 자유롭게 비행하며 이동합니다.")
        ja_clauses.append("宙に浮上して自在に飛行移動する。")

    if is_ult:
        ko_clauses.append("강력한 궁극의 힘을 개방하여 전장을 압도합니다.")
        ja_clauses.append("強力な究極の力を解放して戦場を制圧する。")

    if not ko_clauses:
        ko_clauses.append(f"{hero}의 특수 능력을 발동하여 적에게 피해를 입히고 팀을 지원합니다.")
        ja_clauses.append(f"{hero}の特殊能力を発動し、敵にダメージを与えてチームを支援する。")

    return {
        "ko": " ".join(ko_clauses),
        "ja": "".join(ja_clauses)
    }

# Test sample
random.seed(42)
sample = random.sample(skills, 10)
for desc, meta in sample:
    t = test_translate(meta['sampleHero'], meta['sampleSkill'], desc)
    print(f"=== [{meta['sampleHero']}] {meta['sampleSkill']} ===")
    print("EN:", desc[:80])
    print("KO:", t['ko'])
    print("JA:", t['ja'])
    print()
