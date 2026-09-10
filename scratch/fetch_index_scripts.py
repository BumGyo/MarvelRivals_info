import urllib.request
import ssl
import re

ctx = ssl._create_unverified_context()
BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
print("Scripts in heroes/index.html:")
for s in scripts:
    print(" -", s)
