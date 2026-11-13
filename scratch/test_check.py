import json
import subprocess

content = subprocess.check_output(['git', 'show', '69162d8:data/heroes.json'], encoding='utf-8')
data_old = json.loads(content)

with open('data/heroes.json', 'r', encoding='utf-8') as f:
    data_new = json.load(f)

old_heroes = {h.get('name').upper(): h for h in data_old}
new_heroes = {h.get('name').upper(): h for h in data_new}

print('Old count:', len(old_heroes))
print('New count:', len(new_heroes))

missing = set(old_heroes.keys()) - set(new_heroes.keys())
added = set(new_heroes.keys()) - set(old_heroes.keys())
print('Missing in new:', missing)
print('Added in new:', added)

