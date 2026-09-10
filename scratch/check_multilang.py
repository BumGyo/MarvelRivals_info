import urllib.request, ssl, re
ctx = ssl._create_unverified_context()

req = urllib.request.Request('https://www.marvelrivals.com/kr/heroes/index.html', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='replace')
with open('scratch/kr_heroes.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved kr_heroes.html, checking scripts and anchors...")
scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts:", scripts)
anchors = re.findall(r'<a[^>]*href="([^"]+)"', html)
print("Anchors count:", len(anchors))
