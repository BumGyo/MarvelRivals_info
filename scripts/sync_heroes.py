#!/usr/bin/env python3
"""
Marvel Rivals Official Hero Skill & Team-Up Data Sync Script
Faithfully replicates official NetEase frontend parser (index_3aec8dda.js).
Accurately extracts:
 - Hero base stats (Health, Movement Speed normalized to 'X m/s', Movement Mode)
 - Normal Abilities with exact official names, icons, and stats
 - Team-Up Loadouts 1 & 2 with exact partner hero avatar, partner hero name (KO/JA/EN),
   exact skill name, icon, Base Effect stats, and Enhanced Effect stats.
"""

import os
import sys
import re
import json
import ssl
import urllib.request
from html import unescape
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl._create_unverified_context()

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"

HERO_NAMES = {
    "The Hood": {"ko": "더 후드", "ja": "ザ・フッド"},
    "Jubilation Lee": {"ko": "쥬빌리", "ja": "ジュビリー"},
    "Jubilee": {"ko": "쥬빌리", "ja": "ジュビリー"},
    "Cyclops": {"ko": "사이클롭스", "ja": "サイクロップス"},
    "DEVIL DINOSAUR": {"ko": "데빌 다이노소어", "ja": "デビル・ダイナソー"},
    "Devil Dinosaur": {"ko": "데빌 다이노소어", "ja": "デビル・ダイナソー"},
    "BLACK CAT": {"ko": "블랙 캣", "ja": "ブラックキャット"},
    "Black Cat": {"ko": "블랙 캣", "ja": "ブラックキャット"},
    "IRON MAN": {"ko": "아이언맨", "ja": "アイアンマン"},
    "Iron Man": {"ko": "아이언맨", "ja": "アイアンマン"},
    "HULK": {"ko": "헐크", "ja": "ハルク"},
    "Hulk": {"ko": "헐크", "ja": "ハルク"},
    "SPIDER-MAN": {"ko": "스파이더맨", "ja": "スパイダーマン"},
    "Spider-Man": {"ko": "스파이더맨", "ja": "スパイダーマン"},
    "THE PUNISHER": {"ko": "더 퍼니셔", "ja": "パニッシャー"},
    "The Punisher": {"ko": "더 퍼니셔", "ja": "パニッシャー"},
    "PUNISHER": {"ko": "더 퍼니셔", "ja": "パニッシャー"},
    "THOR": {"ko": "토르", "ja": "ソー"},
    "Thor": {"ko": "토르", "ja": "ソー"},
    "STORM": {"ko": "스톰", "ja": "ストーム"},
    "Storm": {"ko": "스톰", "ja": "ストーム"},
    "MAGNETO": {"ko": "매그니토", "ja": "マグニートー"},
    "Magneto": {"ko": "매그니토", "ja": "マグニートー"},
    "SCARLET WITCH": {"ko": "스칼렛 위치", "ja": "スカーレット・ウィッチ"},
    "Scarlet Witch": {"ko": "스칼렛 위치", "ja": "スカーレット・ウィッチ"},
    "LOKI": {"ko": "로키", "ja": "ロキ"},
    "Loki": {"ko": "로키", "ja": "ロキ"},
    "DOCTOR STRANGE": {"ko": "닥터 스트레인지", "ja": "ドクター・ストレンジ"},
    "Doctor Strange": {"ko": "닥터 스트레인지", "ja": "ドクター・ストレンジ"},
    "VENOM": {"ko": "베놈", "ja": "ヴェノム"},
    "Venom": {"ko": "베놈", "ja": "ヴェノム"},
    "GROOT": {"ko": "그루트", "ja": "グルート"},
    "Groot": {"ko": "그루트", "ja": "グルート"},
    "ROCKET RACCOON": {"ko": "로켓 라쿤", "ja": "ロケット・ラクーン"},
    "Rocket Raccoon": {"ko": "로켓 라쿤", "ja": "ロケット・ラクーン"},
    "STAR-LORD": {"ko": "스타로드", "ja": "スター・ロード"},
    "Star-Lord": {"ko": "스타로드", "ja": "スター・ロード"},
    "Peni Parker": {"ko": "페니 파커", "ja": "ペニ・パーカー"},
    "PENI PARKER": {"ko": "페니 파커", "ja": "ペニ・パーカー"},
    "MANTIS": {"ko": "맨티스", "ja": "マンティス"},
    "Mantis": {"ko": "맨티스", "ja": "マンティス"},
    "LUNA SNOW": {"ko": "루나 스노우", "ja": "ルナ・スノー"},
    "Luna Snow": {"ko": "루나 스노우", "ja": "ルナ・スノー"},
    "MAGIK": {"ko": "매직", "ja": "マジック"},
    "Magik": {"ko": "매직", "ja": "マジック"},
    "NAMOR": {"ko": "네이머", "ja": "ネイモア"},
    "Namor": {"ko": "네이머", "ja": "ネイモア"},
    "BLACK PANTHER": {"ko": "블랙 팬서", "ja": "ブラックパンサー"},
    "Black Panther": {"ko": "블랙 팬서", "ja": "ブラックパンサー"},
    "HELA": {"ko": "헬라", "ja": "ヘラ"},
    "Hela": {"ko": "헬라", "ja": "ヘラ"},
    "JEFF THE LAND SHARK": {"ko": "제프 더 랜드 샤크", "ja": "ジェフ・ザ・ランド・シャーク"},
    "Jeff the Land Shark": {"ko": "제프 더 랜드 샤크", "ja": "ジェフ・ザ・ランド・シャーク"},
    "ADAM WARLOCK": {"ko": "아담 워록", "ja": "アダム・ウォーロック"},
    "Adam Warlock": {"ko": "아담 워록", "ja": "アダム・ウォーロック"},
    "CAPTAIN AMERICA": {"ko": "캡틴 아메리카", "ja": "キャプテン・アメリカ"},
    "Captain America": {"ko": "캡틴 아메리카", "ja": "キャプテン・アメリカ"},
    "WINTER SOLDIER": {"ko": "윈터 솔져", "ja": "ウィンター・ソルジャー"},
    "Winter Soldier": {"ko": "윈터 솔져", "ja": "ウィンター・ソルジャー"},
    "HAWKEYE": {"ko": "호크아이", "ja": "ホークアイ"},
    "Hawkeye": {"ko": "호크아이", "ja": "ホークアイ"},
    "CLOAK & DAGGER": {"ko": "클록 & 대거", "ja": "クローク＆ダガー"},
    "Cloak & Dagger": {"ko": "클록 & 대거", "ja": "クローク＆ダガー"},
    "IRON FIST": {"ko": "아이언 피스트", "ja": "アイアン・フィスト"},
    "Iron Fist": {"ko": "아이언 피스트", "ja": "アイアン・フィスト"},
    "MISTER FANTASTIC": {"ko": "미스터 판타스틱", "ja": "ミスター・ファンタスティック"},
    "Mister Fantastic": {"ko": "미스터 판타스틱", "ja": "ミスター・ファンタスティック"},
    "INVISIBLE WOMAN": {"ko": "인비저블 우먼", "ja": "インビジブル・ウーマン"},
    "Invisible Woman": {"ko": "인비저블 우먼", "ja": "インビジブル・ウーマン"},
    "HUMAN TORCH": {"ko": "휴먼 토치", "ja": "ヒューマン・トーチ"},
    "Human Torch": {"ko": "휴먼 토치", "ja": "ヒューマン・トーチ"},
    "THE THING": {"ko": "더 씽", "ja": "ザ・シング"},
    "The Thing": {"ko": "더 씽", "ja": "ザ・シング"},
    "MOON KNIGHT": {"ko": "문나이트", "ja": "ムーンナイト"},
    "Moon Knight": {"ko": "문나이트", "ja": "ムーンナイト"},
    "PSYLOCKE": {"ko": "사일록", "ja": "サイロック"},
    "Psylocke": {"ko": "사일록", "ja": "サイロック"},
    "WOLVERINE": {"ko": "울버린", "ja": "ウルヴァリン"},
    "Wolverine": {"ko": "울버린", "ja": "ウルヴァリン"},
    "SQUIRREL GIRL": {"ko": "스쿼럴 걸", "ja": "スクイレル・ガール"},
    "Squirrel Girl": {"ko": "스쿼럴 걸", "ja": "スクイレル・ガール"},
    "BLADE": {"ko": "블레이드", "ja": "ブレイド"},
    "Blade": {"ko": "블레이드", "ja": "ブレイド"},
    "PHOENIX": {"ko": "피닉스", "ja": "フェニックス"},
    "Phoenix": {"ko": "피닉스", "ja": "フェニックス"},
    "EMMA FROST": {"ko": "엠마 프로스트", "ja": "エマ・フロスト"},
    "Emma Frost": {"ko": "엠마 프로스트", "ja": "エマ・フロスト"},
    "ROGUE": {"ko": "로그", "ja": "ローグ"},
    "Rogue": {"ko": "로그", "ja": "ローグ"},
    "GAMBIT": {"ko": "갬빗", "ja": "ガンビット"},
    "Gambit": {"ko": "갬빗", "ja": "ガンビット"},
    "ULTRON": {"ko": "울트론", "ja": "ウルトロン"},
    "Ultron": {"ko": "울트론", "ja": "ウルトロン"},
    "BLACK WIDOW": {"ko": "블랙 위도우", "ja": "ブラック・ウィドウ"},
    "Black Widow": {"ko": "블랙 위도우", "ja": "ブラック・ウィドウ"},
    "DEADPOOL": {"ko": "데드풀", "ja": "デッドプール"},
    "Deadpool": {"ko": "데드풀", "ja": "デッドプール"},
    "ANGELA": {"ko": "안젤라", "ja": "アンジェラ"},
    "Angela": {"ko": "안젤라", "ja": "アンジェラ"},
    "White Fox": {"ko": "화이트 폭스", "ja": "ホワイト・フォックス"},
    "WHITE FOX": {"ko": "화이트 폭스", "ja": "ホワイト・フォックス"},
    "Elsa Bloodstone": {"ko": "엘사 블러드스톤", "ja": "エルサ・ブラッドストーン"},
    "ELSA BLOODSTONE": {"ko": "엘사 블러드스톤", "ja": "エルサ・ブラッドストーン"},
    "Daredevil": {"ko": "데어데블", "ja": "デアデビル"},
    "DAREDEVIL": {"ko": "데어데블", "ja": "デアデビル"},
    "Gorr the God Butcher": {"ko": "고르", "ja": "ゴア"},
    "Gorr": {"ko": "고르", "ja": "ゴア"},
    "GORR": {"ko": "고르", "ja": "ゴア"}
}

ROLE_TRANSLATIONS = {
    "VANGUARD": {"en": "Vanguard", "ko": "뱅가드 (돌격)", "ja": "ヴァンガード (タンク)"},
    "DUELIST": {"en": "Duelist", "ko": "듀얼리스트 (공격)", "ja": "デュエリスト (DPS)"},
    "STRATEGIST": {"en": "Strategist", "ko": "전략가 (지원)", "ja": "ストラテジスト (サポート)"}
}

def resolve_hero_names(raw_name):
    """
    Resolve hero name into KO and JA.
    If new/unknown hero, safely fallback to English name for both KO and JA.
    """
    if not raw_name:
        return "", {"ko": "", "ja": ""}
    norm = raw_name.strip()
    # 1. Exact match
    if norm in HERO_NAMES:
        return norm, HERO_NAMES[norm]
    # 2. Case-insensitive match
    for k, v in HERO_NAMES.items():
        if k.lower() == norm.lower():
            return norm, v
    # 3. New hero fallback: use English name for KO and JA
    return norm, {"ko": norm, "ja": norm}

KEY_TRANSLATIONS = {
    "Left Click": {"ko": "마우스 좌클릭", "ja": "左クリック"},
    "Right Click": {"ko": "마우스 우클릭", "ja": "右クリック"},
    "Q": {"ko": "Q (궁극기)", "ja": "Q (アルティメット)"},
    "SHIFT": {"ko": "Shift", "ja": "Shift"},
    "Shift": {"ko": "Shift", "ja": "Shift"},
    "E": {"ko": "E", "ja": "E"},
    "F": {"ko": "F", "ja": "F"},
    "C": {"ko": "C", "ja": "C"},
    "SPACE": {"ko": "Space", "ja": "Space"},
    "Space": {"ko": "Space", "ja": "Space"},
    "Passive": {"ko": "패시브", "ja": "パッシブ"}
}


def normalize_stat_value(k, v):
    if not v:
        return ""
    v_str = str(v).replace('\xa0', ' ').strip()
    if k == "Movement Speed":
        m_num = re.match(r'^(\d+(?:\.\d+)?)$', v_str)
        if m_num:
            val = float(m_num.group(1))
            if val >= 100:
                val = val / 100.0
            return f"{val:g} m/s"
        m_ms = re.match(r'^(\d+(?:\.\d+)?)\s*m/s$', v_str, re.IGNORECASE)
        if m_ms:
            val = float(m_ms.group(1))
            return f"{val:g} m/s"
    return v_str


def extract_partner_name(desc):
    if not desc:
        return ""
    m = re.search(r"teaming up with ([A-Za-z\s&.\x27-]+?)(?:,|\.|\s+and|\s+grants|\s+heavily|\s+Armor|\s+releasing|\s+is|\s+or|\s+can|\s+to|\s+both|\s+attacks)", desc, re.IGNORECASE)
    if m:
        cand = m.group(1).strip()
        # Clean cand
        for h_key in HERO_NAMES:
            if h_key.lower() == cand.lower():
                return h_key
        return cand
    return ""


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


def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_hero_list():
    html = fetch_url(BASE_URL)
    pattern = r'<a\s+[^>]*data-url="([^"]+)"[^>]*data-id="([^"]+)"[^>]*data-tag="([^"]*)"[^>]*title="([^"]+)"[^>]*>(.*?)</a>'
    items = re.findall(pattern, html, re.DOTALL)

    heroes = []
    seen = set()
    for url, hid, tag, title, inner in items:
        title = title.strip()
        if hid in seen:
            continue
        seen.add(hid)
        
        imgs = re.findall(r'src=[\'"]([^\'"]+)[\'"]', inner)
        avatar = imgs[2] if len(imgs) >= 3 else (imgs[0] if imgs else "")
        full_img = imgs[0] if imgs else ""
        
        tag = tag.upper().strip()
        if not tag:
            tag = "DUELIST"

        roles_list = [r for r in tag.split() if r in ["VANGUARD", "DUELIST", "STRATEGIST"]]
        if not roles_list:
            roles_list = ["DUELIST"]
        primary_role = roles_list[0] if len(roles_list) == 1 else "ALL-ROUNDER"

        heroes.append({
            "id": hid,
            "title": title,
            "role": primary_role,
            "roles": roles_list,
            "url": url,
            "avatar": avatar,
            "full_img": full_img
        })

    return heroes


def parse_hero_page(hero):
    try:
        html = fetch_url(hero["url"])
    except Exception as e:
        print(f"Error fetching hero {hero['title']}: {e}")
        return None

    builder = TreeBuilder()
    builder.feed(html)

    tables = builder.root.find_all("table")
    if not tables:
        return None
    main_table = tables[0]

    top_trs = []
    for tr in main_table.find_all("tr", recursive=True):
        p = tr.parent
        if p == main_table or (p.tag == "tbody" and p.parent == main_table):
            top_trs.append(tr)

    c_partners = []
    teamup_raw = []
    normal_abilities = []
    type0_rows = []

    for tr in top_trs:
        tds = [c for c in tr.children if c.tag == "td"]
        if not tds:
            continue
        col0 = tds[0].get_text().strip()
        if not col0.isdigit():
            continue
        type_num = int(col0)

        # Base stats row: type == 0 (table is located in tds[3])
        if type_num == 0:
            name_txt = tds[1].get_text().strip() if len(tds) > 1 else ""
            imgs = tds[2].find_all("img") if len(tds) > 2 else []
            img_src = imgs[0].attrs.get("src", "") if imgs else ""
            sub_tables = []
            if len(tds) > 3:
                sub_tables = tds[3].find_all("table")
            if not sub_tables:
                for td in tds:
                    st = td.find_all("table")
                    if st:
                        sub_tables = st
                        break
            row_stats = {}
            if sub_tables:
                for sub_tr in sub_tables[0].find_all("tr"):
                    sub_tds = [c for c in sub_tr.children if c.tag == "td"]
                    if len(sub_tds) >= 2:
                        k = sub_tds[0].get_text().strip().replace('\xa0', ' ')
                        v = sub_tds[1].get_text().strip().replace('\xa0', ' ')
                        if k and k != "占位空格":
                            row_stats[k] = normalize_stat_value(k, v)
            if row_stats:
                type0_rows.append({"name": name_txt, "avatar": img_src, "stats": row_stats})
            continue

        # Partner avatars row: type == 4, 2 images, no sub-table
        if type_num == 4 and len(tds) >= 4:
            img2 = tds[2].find_all("img")
            img3 = tds[3].find_all("img")
            has_table = len(tds) > 4 and len(tds[4].find_all("table")) > 0
            if img2 and img3 and not has_table:
                c_partners = [img2[0].attrs.get("src", ""), img3[0].attrs.get("src", "")]
                continue

        name_txt = tds[1].get_text().strip() if len(tds) > 1 else ""
        imgs = tds[2].find_all("img") if len(tds) > 2 else []
        icon = imgs[0].attrs.get("src", "") if imgs else ""
        desc = tds[3].get_text().strip() if len(tds) > 3 else ""

        stats = {}
        if len(tds) > 4:
            sub_tables = tds[4].find_all("table")
            if sub_tables:
                for sub_tr in sub_tables[0].find_all("tr"):
                    sub_tds = [c for c in sub_tr.children if c.tag == "td"]
                    if len(sub_tds) >= 2:
                        k = sub_tds[0].get_text().strip().replace('\xa0', ' ')
                        v = sub_tds[1].get_text().strip().replace('\xa0', ' ')
                        if k and k != "占位空格":
                            stats[k] = normalize_stat_value(k, v)

        last_txt = tds[-1].get_text().strip() if tds else ""
        if type_num == 4:
            lxHero = int(last_txt) if last_txt.isdigit() else 0
            teamup_raw.append({
                "type": 4,
                "name": name_txt,
                "icon": icon,
                "desc": desc,
                "lxHero": lxHero,
                "stats": stats
            })
        else:
            form_idx = int(last_txt) if last_txt.isdigit() else 0
            key = stats.get("Key", "Passive")
            normal_abilities.append({
                "type": type_num,
                "form_index": form_idx,
                "key": key,
                "key_trans": KEY_TRANSLATIONS.get(key, {"ko": key, "ja": key}),
                "name": name_txt or f"Skill ({key})",
                "icon": icon,
                "description": desc,
                "stats": stats
            })

    # Pick primary base_stats:
    base_stats = {}
    h_title = hero["title"].upper()
    for r_item in type0_rows:
        n_txt = r_item["name"]
        r_stats = r_item["stats"]
        if n_txt.upper() in h_title or h_title in n_txt.upper():
            if r_stats.get("Health"):
                base_stats = r_stats
                break
    if not base_stats and type0_rows:
        base_stats = type0_rows[0]["stats"]

    if "Movement Mode" not in base_stats:
        if hero["title"].upper() in ["IRON MAN", "STORM", "HUMAN TORCH"]:
            base_stats["Movement Mode"] = "Flight"
        else:
            base_stats["Movement Mode"] = "Ground"

    # Group team-up skills by lxHero
    # In official game:
    # lxHero 0 -> Loadout 1, with c_partners[0]
    # lxHero 1 -> Loadout 2, with c_partners[1]
    u = {}
    structured_teamups = []
    for item in teamup_raw:
        lx = item["lxHero"]
        if lx not in u:
            u[lx] = 0
        lx_tier = u[lx]
        u[lx] += 1

        partner_avatar = c_partners[lx] if lx < len(c_partners) else ""
        partner_raw = extract_partner_name(item["desc"])
        partner_name_en, partner_info = resolve_hero_names(partner_raw)

        loadout_num = lx + 1
        tier_label = "base" if lx_tier == 0 else "enhanced"

        structured_teamups.append({
            "loadout_number": loadout_num,
            "loadout_name": item["name"] or f"Loadout {loadout_num}",
            "tier": tier_label,
            "name": item["name"],
            "icon": item["icon"],
            "description": item["desc"],
            "partner_avatar": partner_avatar,
            "partner_name": {
                "en": partner_name_en,
                "ko": partner_info.get("ko", partner_name_en),
                "ja": partner_info.get("ja", partner_name_en)
            },
            "key": item["stats"].get("Key", "Passive"),
            "stats": item["stats"]
        })

    KEY_ORDER = {
        "Left Click": 1,
        "Right Click": 2,
        "Q": 3,
        "SHIFT": 4,
        "Shift": 4,
        "E": 5,
        "F": 6,
        "C": 7,
        "Space": 8,
        "SPACE": 8,
        "V": 9,
        "X": 10,
        "Z": 11,
        "Passive": 20,
        "PASSIVE": 20,
    }
    normal_abilities.sort(key=lambda s: (s.get("form_index", 0), KEY_ORDER.get(s.get("key", ""), 15)))

    norm_name, names = resolve_hero_names(hero["title"])

    return {
        "id": hero["id"],
        "name": norm_name,
        "names": {
            "en": norm_name,
            "ko": names.get("ko", norm_name),
            "ja": names.get("ja", norm_name)
        },
        "role": hero["role"],
        "roles": hero.get("roles", [hero["role"]]),
        "role_name": ROLE_TRANSLATIONS.get(hero["role"], {"en": hero["role"], "ko": hero["role"], "ja": hero["role"]}),
        "avatar": hero["avatar"],
        "full_img": hero["full_img"],
        "base_stats": base_stats,
        "raw_forms": type0_rows,
        "skills": normal_abilities,
        "teamups": structured_teamups
    }


def main():
    print("Fetching Marvel Rivals official hero roster...")
    heroes = parse_hero_list()
    print(f"Discovered {len(heroes)} heroes. Extracting details...")

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(parse_hero_page, h): h for h in heroes}
        for future in as_completed(futures):
            h_info = future.result()
            if h_info:
                results.append(h_info)
                print(f" -> {h_info['name']} (Skills: {len(h_info['skills'])}, Team-Ups: {len(h_info['teamups'])})")

    results.sort(key=lambda x: x["name"])

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    heroes_file = os.path.join(data_dir, "heroes.json")
    with open(heroes_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Saved {len(results)} heroes into {heroes_file}")


if __name__ == "__main__":
    main()
