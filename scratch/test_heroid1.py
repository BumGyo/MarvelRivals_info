import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
req = urllib.request.Request('https://www.marvelrivals.com/heroes/index.html?heroId=1', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='replace')

pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
items = re.findall(pattern, html, re.DOTALL)
print('With heroId=1, items count:', len(items))
for item in items:
    if 'ADAM' in item[3].upper():
        print('Found Adam in heroId=1:', item)

