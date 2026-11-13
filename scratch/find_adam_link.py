import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
req = urllib.request.Request('https://www.marvelrivals.com/heroes/index.html?heroId=0', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='replace')

for line in html.splitlines():
    if 'heroId=0' in line or 'ADAM' in line:
        print(line[:200])

