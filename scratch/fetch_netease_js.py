import urllib.request
import ssl
import re

ctx = ssl._create_unverified_context()
js_url = "https://www.marvelrivals.com/pc/gw/20241128194803/js/heroes/index_3aec8dda.js"
req = urllib.request.Request(js_url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

with open('scratch/netease_index.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Downloaded netease_index.js ({len(content)} chars)")

# Search for form or tab rendering or Hulk / Black Cat
for word in ["form", "stage", "shape", "tab", "Hulk", "Bruce", "Cat", "lxHero", "type"]:
    matches = len(re.findall(word, content, re.IGNORECASE))
    print(f"Matches for '{word}': {matches}")
