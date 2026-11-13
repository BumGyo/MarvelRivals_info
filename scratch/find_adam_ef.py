with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.findall(r'[^\'"]*ef4511de[^\'"]*', js)
print('matches:', matches)

