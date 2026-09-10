import json
import urllib.request
import ssl
import re
from html.parser import HTMLParser

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
items = re.findall(pattern, html, re.DOTALL)

bc_url = None
for url, hid, tag, title, inner in items:
    if "black cat" in title.lower():
        bc_url = url
        print(f"Found Black Cat: {title}, id={hid}, url={url}")
        break

if bc_url:
    bc_html = urllib.request.urlopen(urllib.request.Request(bc_url, headers={"User-Agent": "Mozilla/5.0"}), context=ctx).read().decode('utf-8')
    with open('scratch/black_cat_page.html', 'w', encoding='utf-8') as f:
        f.write(bc_html)
    print("Saved scratch/black_cat_page.html")
