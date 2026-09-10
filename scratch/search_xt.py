with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re
print("Looking at xt matches:")
for m in re.finditer(r'.{0,100}\.xt.{0,100}', code):
    print("MATCH:", m.group(0))
