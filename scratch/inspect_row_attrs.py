with open('scratch/black_cat_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for any javascript or data attributes or classes in table 0
from inspect_black_cat_tables import TreeBuilder
builder = TreeBuilder()
builder.feed(html)
t0 = builder.root.find_all("table")[0]
rows = t0.find_all("tr", recursive=False)
tbodies = [c for c in t0.children if c.tag == "tbody"]
if tbodies:
    rows = tbodies[0].find_all("tr", recursive=False)

for idx, r in enumerate(rows):
    tds = [c for c in r.children if c.tag == "td"]
    attrs_list = [f"{k}={v}" for k, v in r.attrs.items()]
    td0_attrs = [f"{k}={v}" for k, v in tds[0].attrs.items()] if tds else []
    td1_text = tds[1].get_text().strip() if len(tds) > 1 else ""
    td_last = tds[-1].get_text().strip() if tds else ""
    print(f"Row {idx:02d}: {td1_text:22s} | tr_attrs={attrs_list} | td0_attrs={td0_attrs} | td_last={td_last}")
