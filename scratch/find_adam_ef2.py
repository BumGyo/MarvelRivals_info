with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
for m in re.finditer(r'ef4511de', js):
    start = max(0, m.start() - 100)
    end = min(len(js), m.end() + 100)
    print("MATCH:", js[start:end])

