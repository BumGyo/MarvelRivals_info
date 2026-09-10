from inspect_black_cat_tables import TreeBuilder

def inspect_type0(filename, hero_name):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    builder = TreeBuilder()
    builder.feed(html)
    t0 = builder.root.find_all("table")[0]
    rows = t0.find_all("tr", recursive=False)
    tbodies = [c for c in t0.children if c.tag == "tbody"]
    if tbodies:
        rows = tbodies[0].find_all("tr", recursive=False)

    print(f"\n=== {hero_name} Type 0 Rows ===")
    for idx, r in enumerate(rows):
        tds = [c for c in r.children if c.tag == "td"]
        if tds and tds[0].get_text().strip() == "0":
            name = tds[1].get_text().strip() if len(tds) > 1 else ""
            imgs = tds[2].find_all("img") if len(tds) > 2 else []
            img_src = imgs[0].attrs.get("src", "") if imgs else ""
            stats_table = tds[3].find_all("table") if len(tds) > 3 else []
            stats = []
            if stats_table:
                for str_row in stats_table[0].find_all("tr"):
                    std = [c.get_text().strip() for c in str_row.children if c.tag == "td"]
                    if len(std) >= 2:
                        stats.append(f"{std[0]}: {std[1]}")
            print(f"Form {idx}: Name='{name}', Img='{img_src}', Stats='{', '.join(stats)}'")

inspect_type0('scratch/hulk_page.html', 'HULK')
inspect_type0('scratch/black_cat_page.html', 'BLACK CAT')
