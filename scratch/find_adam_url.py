import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
req = urllib.request.Request('https://www.marvelrivals.com/heroes/index.html?heroId=0', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='replace')

print('ef4511de in html?', 'ef4511de' in html)
if 'ef4511de' in html:
    for line in html.splitlines():
        if 'ef4511de' in line:
            print('Line with ef4511de:', line[:200])

# Let's search where Adam Warlock's content URL or art-inner-content is!
urls = re.findall(r'https?://[^\s"\'<>]+(?:11956|1198|12|13)[^\s"\'<>]+', html)
print('Found content URLs matching pattern:', len(urls))
for u in set(urls):
    print(u)

