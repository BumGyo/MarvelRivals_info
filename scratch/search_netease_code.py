with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's search for how table data is processed
import re
print("Looking at functions in netease_index.js:")
# print snippet around lxHero
for m in re.finditer(r'.{0,100}lxHero.{0,100}', code):
    print("MATCH:", m.group(0))
