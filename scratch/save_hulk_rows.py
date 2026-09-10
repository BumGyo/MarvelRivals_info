from inspect_black_cat_tables import TreeBuilder

with open('scratch/hulk_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

builder = TreeBuilder()
builder.feed(html)
t0 = builder.root.find_all("table")[0]

rows = t0.find_all("tr", recursive=False)
tbodies = [c for c in t0.children if c.tag == "tbody"]
if tbodies:
    rows = tbodies[0].find_all("tr", recursive=False)

lines = []
for idx, r in enumerate(rows):
    tds = [c for c in r.children if c.tag == "td"]
    if len(tds) >= 4:
        col0 = tds[0].get_text().strip()
        name = tds[1].get_text().strip()
        desc = tds[3].get_text().strip()[:50].replace('\n', ' ')
        td_last = tds[-1].get_text().strip() if tds else ""
        stats_key = ""
        st = tds[4].find_all("table") if len(tds) > 4 else []
        if st:
            for str_row in st[0].find_all("tr"):
                std = [c.get_text().strip() for c in str_row.children if c.tag == "td"]
                if len(std) >= 2 and std[0] == "Key":
                    stats_key = std[1]
        lines.append(f"[{idx:02d}] type={col0} | Key={stats_key:11s} | Name={name:25s} | td_last={td_last:8s} | Desc={desc}")

with open('scratch/hulk_rows_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Wrote scratch/hulk_rows_summary.txt")
