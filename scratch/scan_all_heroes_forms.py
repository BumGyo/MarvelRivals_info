import json
import urllib.request
import ssl
import re
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"
req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
items = re.findall(pattern, html, re.DOTALL)

heroes = []
seen = set()
for url, hid, tag, title, inner in items:
    title = title.strip()
    if hid in seen:
        continue
    seen.add(hid)
    heroes.append({"id": hid, "title": title, "url": url})

print(f"Total heroes to scan: {len(heroes)}")

class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []
        self.text = []

    def get_text(self):
        txt = "".join(self.text)
        for c in self.children:
            txt += c.get_text()
        return txt.strip()

    def find_all(self, tag, recursive=True):
        res = []
        for c in self.children:
            if c.tag == tag:
                res.append(c)
            if recursive:
                res.extend(c.find_all(tag, recursive=True))
        return res

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Node("root", {})
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in ["img", "br", "hr", "meta", "link", "input"]:
            self.current = node

    def handle_endtag(self, tag):
        if self.current.parent and self.current.tag == tag:
            self.current = self.current.parent

    def handle_data(self, data):
        self.current.text.append(data)

def analyze_hero(h):
    try:
        req = urllib.request.Request(h["url"], headers={"User-Agent": "Mozilla/5.0"})
        h_html = urllib.request.urlopen(req, context=ctx, timeout=15).read().decode('utf-8')
    except Exception as e:
        return {"title": h["title"], "error": str(e)}

    builder = TreeBuilder()
    builder.feed(h_html)
    tables = builder.root.find_all("table")
    if not tables:
        return {"title": h["title"], "error": "No table"}

    t0 = tables[0]
    rows = t0.find_all("tr", recursive=False)
    tbodies = [c for c in t0.children if c.tag == "tbody"]
    if tbodies:
        rows = tbodies[0].find_all("tr", recursive=False)

    type0_rows = []
    normal_skills = []

    for idx, r in enumerate(rows):
        tds = [c for c in r.children if c.tag == "td"]
        if not tds:
            continue
        col0 = tds[0].get_text().strip()
        name = tds[1].get_text().strip() if len(tds) > 1 else ""
        td_last = tds[-1].get_text().strip() if tds else ""
        imgs = tds[2].find_all("img") if len(tds) > 2 else []
        img_src = imgs[0].attrs.get("src", "") if imgs else ""

        if col0 == "0":
            type0_rows.append({
                "index": len(type0_rows),
                "name": name,
                "avatar": img_src
            })
        elif col0.isdigit() and int(col0) in [1, 2, 3]:
            # Normal skill
            normal_skills.append({
                "name": name,
                "type": int(col0),
                "td_last": td_last
            })

    unique_td_lasts = sorted(list(set([s["td_last"] for s in normal_skills if s["td_last"].isdigit()])))

    return {
        "title": h["title"],
        "type0_count": len(type0_rows),
        "type0_forms": type0_rows,
        "skills_count": len(normal_skills),
        "skill_form_indices": unique_td_lasts
    }

results = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(analyze_hero, h): h for h in heroes}
    for f in as_completed(futures):
        res = f.result()
        results.append(res)

with open('scratch/all_heroes_forms_scan.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Scan complete. Saved scratch/all_heroes_forms_scan.json")
