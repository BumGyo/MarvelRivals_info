import json, re

with open('scratch/extracted_skills.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

# Game vocabulary
VOCAB = {
    "deal damage": ("피해를 입힙니다", "ダメージを与える"),
    "deals damage": ("피해를 입힙니다", "ダメージを与える"),
    "dealing damage": ("피해를 입히며", "ダメージを与え"),
    "healing allies": ("아군을 치유하며", "味方を回復し"),
    "heals allies": ("아군을 치유합니다", "味方を回復する"),
    "heal allies": ("아군을 치유합니다", "味方を回復する"),
    "Bonus Health": ("추가 체력", "追加体力"),
    "bonus health": ("추가 체력", "追加体力"),
    "Movement Speed": ("이동 속도", "移動速度"),
    "movement speed": ("이동 속도", "移動速度"),
    "Speed Boost": ("이동 속도 증가", "移動速度上昇"),
    "cooldown": ("재사용 대기시간", "クールダウン"),
    "cooldowns": ("재사용 대기시간", "クールダウン"),
    "allies": ("아군", "味方"),
    "enemies": ("적들", "敵"),
    "enemy": ("적", "敵"),
    "Bleed": ("출혈", "出血"),
    "Stun": ("기절", "スタン"),
    "Slow": ("감속", "減速"),
    "Root": ("속박", "拘束"),
    "Launch up": ("공중으로 띄움", "ノックアップ"),
    "Knock back": ("밀쳐냄", "ノックバック"),
    "Knockdown": ("넘어뜨림", "ノックダウン"),
    "Invincibility": ("무적", "無敵"),
    "Untargetable": ("대상 지정 불가", "ターゲット不能"),
    "Invisible": ("투명화", "不可視"),
    "flight": ("비행", "飛行"),
    "flying state": ("비행 상태", "飛行状態"),
}

print("Testing vocab matches...")
matched = 0
for desc, meta in skills:
    found = [k for k in VOCAB if k.lower() in desc.lower()]
    if found:
        matched += 1

print(f"Vocab matches in {matched} / {len(skills)} skills")
