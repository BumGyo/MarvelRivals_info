import re
from html.parser import HTMLParser

with open('scratch/black_cat_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

builder = TreeBuilder()
builder.feed(html)
tables = builder.root.find_all("table")
print(f"Total tables found: {len(tables)}")

for t_idx, table in enumerate(tables):
    rows = table.find_all("tr", recursive=False)
    # also check if table has tbody
    tbodies = [c for c in table.children if c.tag == "tbody"]
    if tbodies:
        rows = tbodies[0].find_all("tr", recursive=False)
    print(f"\n--- Table {t_idx} (rows: {len(rows)}) ---")
    for r_idx, tr in enumerate(rows):
        tds = [c for c in tr.children if c.tag == "td"]
        td_texts = [td.get_text().strip().replace('\n', ' ') for td in tds]
        if len(td_texts) > 1:
            print(f"Row {r_idx}: type={td_texts[0]}, name={td_texts[1]}, tds_count={len(tds)}")
            if len(td_texts) > 3:
                print(f"   desc preview: {td_texts[3][:60]}...")
            if len(td_texts) > 4:
                # check sub table
                sub_t = tds[4].find_all("table")
                if sub_t:
                    sub_rows = sub_t[0].find_all("tr")
                    sub_stats = []
                    for sr in sub_rows:
                        std = [c.get_text().strip() for c in sr.children if c.tag == "td"]
                        if len(std) >= 2:
                            sub_stats.append(f"{std[0]}={std[1]}")
                    print(f"   stats: {', '.join(sub_stats[:4])}")
