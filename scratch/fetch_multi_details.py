import urllib.request
import ssl
import re
from inspect_black_cat_tables import TreeBuilder

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
items = re.findall(pattern, html, re.DOTALL)

target_names = ["MAGIK", "Cloak & Dagger", "Gambit", "White Fox"]
targets = {}
for url, hid, tag, title, inner in items:
    for tn in target_names:
        if tn.lower() == title.strip().lower():
            targets[tn] = url

print("Target URLs:", targets)

output_lines = []
for tn, url in targets.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    h_html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    builder = TreeBuilder()
    builder.feed(h_html)
    t0 = builder.root.find_all("table")[0]
    rows = t0.find_all("tr", recursive=False)
    tbodies = [c for c in t0.children if c.tag == "tbody"]
    if tbodies:
        rows = tbodies[0].find_all("tr", recursive=False)

    output_lines.append(f"\n==================== {tn} ====================")
    for idx, r in enumerate(rows):
        tds = [c for c in r.children if c.tag == "td"]
        if not tds:
            continue
        col0 = tds[0].get_text().strip()
        name = tds[1].get_text().strip() if len(tds) > 1 else ""
        td_last = tds[-1].get_text().strip() if tds else ""
        stats_key = ""
        st = tds[4].find_all("table") if len(tds) > 4 else []
        if st:
            for str_row in st[0].find_all("tr"):
                std = [c.get_text().strip() for c in str_row.children if c.tag == "td"]
                if len(std) >= 2 and std[0] == "Key":
                    stats_key = std[1]
        output_lines.append(f"[{idx:02d}] type={col0} | Key={stats_key:11s} | td_last={td_last:6s} | Name={name}")

with open('scratch/multi_forms_details.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Saved scratch/multi_forms_details.txt")
