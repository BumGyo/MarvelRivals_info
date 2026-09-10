from inspect_black_cat_tables import TreeBuilder
import urllib.request
import ssl

ctx = ssl._create_unverified_context()

hero_urls = {
    "MAGIK": "https://www.marvelrivals.com/20241120/41360_1194916.html",
    "Cloak & Dagger": "https://www.marvelrivals.com/20241205/41360_1198642.html",
    "Gambit": "https://www.marvelrivals.com/20251114/41360_1267862.html",
    "White Fox": "https://www.marvelrivals.com/20260320/41360_1291880.html"
}

for hname, url in hero_urls.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    builder = TreeBuilder()
    builder.feed(html)
    t0 = builder.root.find_all("table")[0]
    rows = t0.find_all("tr", recursive=False)
    tbodies = [c for c in t0.children if c.tag == "tbody"]
    if tbodies:
        rows = tbodies[0].find_all("tr", recursive=False)

    print(f"\n==================== {hname} ====================")
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
        print(f"[{idx:02d}] type={col0} | Key={stats_key:11s} | td_last={td_last:6s} | Name={name}")
