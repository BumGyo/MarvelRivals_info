import json
import urllib.request
import ssl
import re

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
items = re.findall(pattern, html, re.DOTALL)

hulk_url = None
for url, hid, tag, title, inner in items:
    if title.strip().lower() == "hulk":
        hulk_url = url
        print(f"Found Hulk: {title}, id={hid}, url={url}")
        break

if hulk_url:
    hulk_html = urllib.request.urlopen(urllib.request.Request(hulk_url, headers={"User-Agent": "Mozilla/5.0"}), context=ctx).read().decode('utf-8')
    with open('scratch/hulk_page.html', 'w', encoding='utf-8') as f:
        f.write(hulk_html)
    print("Saved scratch/hulk_page.html")
