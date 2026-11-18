#!/usr/bin/env python3
"""
Marvel Rivals Official Hero Skill & Team-Up Data Sync Script
Faithfully replicates official NetEase frontend parser & __HERO_DATA__ schema.
Accurately extracts:
 - Hero roles (from data-tag and __HERO_DATA__.jobs)
 - Hero base stats & multi-form raw_forms (Health, Movement Speed normalized to 'X m/s', Movement Mode)
 - Normal Abilities (types 1 & 2 only; excludes deprecated type 3 / 'unused' legacy team-ups)
 - Ordered stat entries [[key, value], ...] preserving sub-section headers and duplicate keys across phases
 - Team-Up Loadouts 1 & 2 with partner hero avatar, partner hero name (KO/JA/EN), Base & Enhanced stats
"""

import os
import re
import json
import time
import urllib.request
from urllib.parse import urljoin
from html import unescape
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.marvelrivals.com/heroes/index.html?heroId=0"

HERO_NAMES = {
    "NIGHTCRAWLER": {"ko": "나이트크롤러", "ja": "ナイトクローラー"},
    "Nightcrawler": {"ko": "나이트크롤러", "ja": "ナイトクローラー"},
    "The Hood": {"ko": "더 후드", "ja": "ザ・フッド"},
    "THE HOOD": {"ko": "더 후드", "ja": "ザ・フッド"},
    "Jubilation Lee": {"ko": "쥬빌리", "ja": "ジュビリー"},
    "Jubilee": {"ko": "쥬빌리", "ja": "ジュビリー"},
    "JUBILEE": {"ko": "쥬빌리", "ja": "ジュビリー"},
    "Cyclops": {"ko": "사이클롭스", "ja": "サイクロップス"},
    "CYCLOPS": {"ko": "사이클롭스", "ja": "サイクロップス"},
    "DEVIL DINOSAUR": {"ko": "데빌 다이노소어", "ja": "デビル・ダイナソー"},
    "Devil Dinosaur": {"ko": "데빌 다이노소어", "ja": "デビル・ダイナソー"},
    "BLACK CAT": {"ko": "블랙 캣", "ja": "ブラックキャット"},
    "Black Cat": {"ko": "블랙 캣", "ja": "ブラックキャット"},
    "IRON MAN": {"ko": "아이언맨", "ja": "アイアンマン"},
    "Iron Man": {"ko": "아이언맨", "ja": "아이언맨"},
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
    "Jean Grey": {"ko": "피닉스", "ja": "フェニックス"},
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
    "GORR THE GOD BUTCHER": {"ko": "고르", "ja": "ゴア"},
    "Gorr": {"ko": "고르", "ja": "ゴア"},
    "GORR": {"ko": "고르", "ja": "ゴア"}
}
# Fix typo if any
HERO_NAMES["Iron Man"] = {"ko": "아이언맨", "ja": "アイアンマン"}

ROLE_TRANSLATIONS = {
    "VANGUARD": {"en": "Vanguard", "ko": "뱅가드 (돌격)", "ja": "ヴァンガード (タンク)"},
    "DUELIST": {"en": "Duelist", "ko": "듀얼리스트 (공격)", "ja": "デュエリスト (DPS)"},
    "STRATEGIST": {"en": "Strategist", "ko": "전략가 (지원)", "ja": "ストラテジスト (サポート)"}
}

KNOWN_HERO_ROLES = {
    "ADAM WARLOCK": "STRATEGIST",
    "NIGHTCRAWLER": "STRATEGIST",
}

KEY_NORMALIZE_MAP = {
    "mouse-left": "Left Click",
    "left click": "Left Click",
    "mouse-right": "Right Click",
    "right click": "Right Click",
    "q": "Q",
    "shift": "Shift",
    "e": "E",
    "f": "F",
    "c": "C",
    "space": "Space",
    "v": "V",
    "x": "X",
    "z": "Z",
    "passive": "Passive",
    "none": "Passive",
    "": "Passive",
}

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
    "V": {"ko": "V", "ja": "V"},
    "X": {"ko": "X", "ja": "X"},
    "Z": {"ko": "Z", "ja": "Z"},
    "Passive": {"ko": "패시브", "ja": "パッシブ"},
    "PASSIVE": {"ko": "패시브", "ja": "パッシブ"},
}

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

LOWER_WORDS = {"of", "to", "in", "on", "at", "by", "for", "with", "and", "or", "per", "the", "a", "an", "from"}
UPPER_ACRONYMS = {"CD": "CD", "HP": "HP", "DPS": "DPS", "AOE": "AoE", "KO": "KO"}


def normalize_key(raw_key):
    if not raw_key:
        return "Passive"
    cleaned = str(raw_key).strip()
    return KEY_NORMALIZE_MAP.get(cleaned.lower(), cleaned)


def smart_label_case(label):
    cleaned = unescape(str(label)).replace("\xa0", " ").strip()
    if not cleaned:
        return ""
    if cleaned != cleaned.upper():
        return cleaned
    words = cleaned.split(" ")
    out = []
    for idx, w in enumerate(words):
        if "/" in w:
            parts = [UPPER_ACRONYMS.get(p, p.capitalize()) for p in w.split("/")]
            out.append("/".join(parts))
        elif w in UPPER_ACRONYMS:
            out.append(UPPER_ACRONYMS[w])
        elif idx > 0 and w.lower() in LOWER_WORDS:
            out.append(w.lower())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def resolve_hero_names(raw_name):
    if not raw_name:
        return "", {"ko": "", "ja": ""}
    norm = unescape(raw_name).replace("\xa0", " ").strip()
    if norm.upper() in ["CLOAK&DAGGER", "CLOAK & DAGGER"]:
        return "CLOAK & DAGGER", HERO_NAMES["CLOAK & DAGGER"]
    if norm in HERO_NAMES:
        return norm, HERO_NAMES[norm]
    for k, v in HERO_NAMES.items():
        if k.lower() == norm.lower():
            return norm, v
    return norm, {"ko": norm, "ja": norm}


def normalize_stat_value(k, v):
    if v is None:
        return ""
    v_str = unescape(str(v)).replace("\xa0", " ").strip()
    if not v_str:
        return ""
    if k.lower() == "movement speed":
        m_num = re.match(r"^(\d+(?:\.\d+)?)$", v_str)
        if m_num:
            val = float(m_num.group(1))
            if val >= 100:
                val = val / 100.0
            return f"{val:g} m/s"
        m_ms = re.match(r"^(\d+(?:\.\d+)?)\s*m/s$", v_str, re.IGNORECASE)
        if m_ms:
            val = float(m_ms.group(1))
            return f"{val:g} m/s"
    return v_str


def trim_trailing_headers(stat_entries):
    """Remove trailing section header rows ([label, '']) that have no stat values beneath them."""
    cleaned = list(stat_entries)
    while cleaned and cleaned[-1][1] == "":
        cleaned.pop()
    result = []
    for i, (k, v) in enumerate(cleaned):
        if v == "":
            # Only keep section header if next entry has a non-empty value
            if i + 1 < len(cleaned) and cleaned[i + 1][1] != "":
                result.append([k, ""])
        else:
            result.append([k, v])
    return result


def extract_partner_name(desc, self_name=""):
    if not desc:
        return ""
    clean_desc = unescape(desc).replace("\xa0", " ")
    # Isolate Enhanced Effect clause when present so we don't match self/other heroes in Base Effect
    enh_part = clean_desc
    if "Enhanced Effect:" in clean_desc:
        enh_part = clean_desc.split("Enhanced Effect:", 1)[1]

    m = re.search(
        r"teaming up with ([A-Za-z\s&.\x27-]+?)(?:,|\.|\s+and|\s+grants|\s+heavily|\s+Armor|\s+releasing|\s+is|\s+or|\s+can|\s+to|\s+both|\s+attacks)",
        enh_part,
        re.IGNORECASE,
    )
    if m:
        cand = m.group(1).strip()
        for h_key in HERO_NAMES:
            if h_key.lower() == cand.lower():
                return h_key
        return cand

    # Fallback: scan Enhanced Effect text for any known hero name (longest first, excluding self)
    self_upper = (self_name or "").upper()
    sorted_candidates = sorted(set(HERO_NAMES.keys()), key=len, reverse=True)
    for h_key in sorted_candidates:
        if h_key.upper() == self_upper:
            continue
        if self_upper == "PHOENIX" and h_key.upper() == "JEAN GREY":
            continue
        pattern = r"(?<![A-Za-z])" + re.escape(h_key) + r"(?![A-Za-z])"
        if re.search(pattern, enh_part, re.IGNORECASE):
            return "Phoenix" if h_key.lower() == "jean grey" else h_key
    return ""


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []
        self.items = []  # Preserves interleaved text strings and child Nodes in exact DOM order

    def get_text(self):
        parts = []
        for item in self.items:
            if isinstance(item, str):
                parts.append(item)
            elif item.tag == "br":
                parts.append("\n")
            else:
                parts.append(item.get_text())
        raw = unescape("".join(parts)).replace("\xa0", " ")
        lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
        return "\n".join(ln for ln in lines if ln).strip()

    def find_all(self, tag, recursive=True):
        res = []
        for c in self.children:
            if c.tag == tag:
                res.append(c)
            if recursive:
                res.extend(c.find_all(tag, recursive=True))
        return res


class TreeBuilder(HTMLParser):
    VOID_TAGS = {"img", "br", "hr", "meta", "link", "input", "area", "base", "col", "embed", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        self.current.items.append(node)
        if tag not in self.VOID_TAGS:
            self.current = node

    def handle_endtag(self, tag):
        curr = self.current
        while curr and curr.parent:
            if curr.tag == tag:
                self.current = curr.parent
                return
            curr = curr.parent

    def handle_data(self, data):
        self.current.items.append(data)


def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (OSError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def parse_hero_list():
    html = fetch_url(BASE_URL)
    static_match = re.search(r'https://www\.marvelrivals\.com/pc/gw/[^/"\s]+/img/heroes/', html)
    if not static_match:
        raise RuntimeError("[ABORT] Official hero image base URL not found.")
    image_base = static_match.group(0).split("/img/heroes/")[0] + "/heroes/"
    builder = TreeBuilder()
    builder.feed(html)
    items = builder.root.find_all("a")

    by_id = {}
    order = []
    for item in items:
        hid = item.attrs.get("data-id", "").strip()
        title = unescape(item.attrs.get("title", "")).strip()
        if not hid or not title:
            continue

        raw_url = item.attrs.get("data-url", "").strip()
        raw_tag = item.attrs.get("data-tag", "").upper().strip()
        imgs = [urljoin(image_base, img.attrs.get("src", "")) for img in item.find_all("img") if img.attrs.get("src")]
        card_img = next((img for img in imgs if "/card-image" in img), "")
        avatar_img = next((img for img in imgs if "/avatar" in img), "")
        fallback_img = imgs[0] if imgs else ""

        if hid not in by_id:
            order.append(hid)
            by_id[hid] = {
                "id": hid,
                "title": title,
                "raw_url": raw_url,
                "raw_tag": raw_tag,
                "card_img": card_img,
                "avatar_img": avatar_img,
                "fallback_img": fallback_img,
            }
        else:
            entry = by_id[hid]
            if not entry["raw_url"] and raw_url:
                entry["raw_url"] = raw_url
            if not entry["raw_tag"] and raw_tag:
                entry["raw_tag"] = raw_tag
            if not entry["card_img"] and card_img:
                entry["card_img"] = card_img
            if not entry["avatar_img"] and avatar_img:
                entry["avatar_img"] = avatar_img
            if not entry["fallback_img"] and fallback_img:
                entry["fallback_img"] = fallback_img

    heroes = []
    seen_titles = set()
    for hid in order:
        entry = by_id[hid]
        title = entry["title"]
        if title.upper() in seen_titles:
            continue
        seen_titles.add(title.upper())

        url = urljoin(BASE_URL, entry["raw_url"]) if entry["raw_url"] else urljoin(BASE_URL, f"/heroes/{hid}/")
        avatar = entry["card_img"] or entry["fallback_img"] or entry["avatar_img"]
        full_img = entry["avatar_img"] or avatar

        tag = entry["raw_tag"]
        roles_list = [r for r in tag.split() if r in ("VANGUARD", "DUELIST", "STRATEGIST")]
        has_explicit_role = bool(roles_list)
        if not roles_list:
            known = KNOWN_HERO_ROLES.get(title.upper())
            roles_list = [known] if known else ["DUELIST"]
        primary_role = roles_list[0] if len(roles_list) == 1 else "ALL-ROUNDER"

        heroes.append({
            "id": hid,
            "title": title,
            "role": primary_role,
            "roles": roles_list,
            "has_explicit_role": has_explicit_role,
            "url": url,
            "avatar": avatar,
            "full_img": full_img,
        })

    if len(heroes) < 50:
        raise RuntimeError(f"[ABORT] Failed to discover enough heroes ({len(heroes)} < 50). Preserving current database.")

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
        return parse_static_hero(hero, html)
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

        # Base stats row: type == 0
        if type_num == 0:
            name_txt = tds[1].get_text().strip() if len(tds) > 1 else ""
            imgs = tds[2].find_all("img") if len(tds) > 2 else []
            img_src = imgs[0].attrs.get("src", "") if imgs else ""
            sub_tables = tds[3].find_all("table") if len(tds) > 3 else []
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
                        k = sub_tds[0].get_text().strip()
                        v = sub_tds[1].get_text().strip()
                        if k and k != "占位空格":
                            row_stats[k] = normalize_stat_value(k, v)
            if row_stats:
                type0_rows.append({"name": name_txt, "avatar": img_src, "stats": row_stats})
            continue

        # Skip deprecated pre-Season-9 legacy team-up rows (hidden by official NetEase frontend)
        if type_num == 3:
            continue

        # Only accept normal attacks (1), abilities (2), and current team-up loadouts (4)
        if type_num not in (1, 2, 4):
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

        stat_entries = []
        raw_key = "Passive"
        if len(tds) > 4:
            sub_tables = tds[4].find_all("table")
            if sub_tables:
                for sub_tr in sub_tables[0].find_all("tr"):
                    sub_tds = [c for c in sub_tr.children if c.tag == "td"]
                    if len(sub_tds) >= 2:
                        k = sub_tds[0].get_text().strip()
                        v = sub_tds[1].get_text().strip()
                        if not k or k == "占位空格":
                            continue
                        if k.lower() == "key":
                            raw_key = v or "Passive"
                        else:
                            stat_entries.append([k, normalize_stat_value(k, v)])

        stat_entries = trim_trailing_headers(stat_entries)
        norm_key = normalize_key(raw_key)

        last_txt = tds[-1].get_text().strip() if tds else ""
        if type_num == 4:
            lx_hero = int(last_txt) if last_txt.isdigit() else 0
            teamup_raw.append({
                "type": 4,
                "name": name_txt,
                "icon": icon,
                "desc": desc,
                "lxHero": lx_hero,
                "key": norm_key,
                "stats": stat_entries,
            })
        else:
            form_idx = int(last_txt) if last_txt.isdigit() else 0
            # Fix NetEase CMS typo on Adam Warlock's F flight skill if parsed via article table
            if hero["title"].upper() == "ADAM WARLOCK" and norm_key == "F" and "Take to the skies" in desc:
                name_txt = "SOARING SURGE"
            normal_abilities.append({
                "type": type_num,
                "form_index": form_idx,
                "key": norm_key,
                "key_trans": KEY_TRANSLATIONS.get(norm_key, {"ko": norm_key, "ja": norm_key}),
                "name": name_txt or f"Skill ({norm_key})",
                "icon": icon,
                "description": desc,
                "stats": stat_entries,
            })

    # Pick primary base_stats
    base_stats = {}
    h_title = hero["title"].upper()
    for r_item in type0_rows:
        n_txt = r_item["name"]
        r_stats = r_item["stats"]
        if n_txt and (n_txt.upper() in h_title or h_title in n_txt.upper()) and r_stats.get("Health"):
            base_stats = dict(r_stats)
            break
    if not base_stats and type0_rows:
        base_stats = dict(type0_rows[0]["stats"])

    if "Movement Mode" not in base_stats:
        base_stats["Movement Mode"] = "Flight" if h_title in ("IRON MAN", "STORM", "HUMAN TORCH", "ULTRON") else "Ground"

    norm_name, names = resolve_hero_names(hero["title"])

    # Group team-up skills by lxHero
    u = {}
    structured_teamups = []
    for item in teamup_raw:
        lx = item["lxHero"]
        lx_tier = u.get(lx, 0)
        u[lx] = lx_tier + 1

        partner_avatar = c_partners[lx] if lx < len(c_partners) else ""
        partner_raw = extract_partner_name(item["desc"], self_name=norm_name)
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
                "ja": partner_info.get("ja", partner_name_en),
            },
            "key": item["key"],
            "key_trans": KEY_TRANSLATIONS.get(item["key"], {"ko": item["key"], "ja": item["key"]}),
            "stats": item["stats"],
        })

    normal_abilities.sort(key=lambda s: (s.get("form_index", 0), KEY_ORDER.get(s.get("key", ""), 15)))

    return {
        "id": hero["id"],
        "name": norm_name,
        "names": {
            "en": norm_name,
            "ko": names.get("ko", norm_name),
            "ja": names.get("ja", norm_name),
        },
        "role": hero["role"],
        "roles": hero.get("roles", [hero["role"]]),
        "role_name": ROLE_TRANSLATIONS.get(hero["role"], {"en": hero["role"], "ko": hero["role"], "ja": hero["role"]}),
        "avatar": hero["avatar"],
        "full_img": hero["full_img"],
        "base_stats": base_stats,
        "raw_forms": type0_rows,
        "skills": normal_abilities,
        "teamups": structured_teamups,
    }


def parse_static_hero(hero, html):
    match = re.search(r"window\.__HERO_DATA__\s*=\s*", html)
    if not match:
        return None
    data, _ = json.JSONDecoder().raw_decode(html[match.end():])
    if data.get("id") != hero["id"] or not data.get("skills"):
        return None

    # Resolve accurate role from __HERO_DATA__.jobs when index link lacked data-tag
    jobs = [str(j).upper().strip() for j in (data.get("jobs") or []) if str(j).upper().strip() in ROLE_TRANSLATIONS]
    roles = jobs if jobs else hero["roles"]
    primary_role = roles[0] if len(roles) == 1 else ("ALL-ROUNDER" if len(roles) > 1 else hero["role"])

    def build_stat_entries(items):
        entries = []
        for s in items or []:
            raw_label = s.get("label", "")
            if not raw_label or raw_label.lower() == "key":
                continue
            label = smart_label_case(raw_label)
            val = s.get("value", "")
            unit = s.get("unit", "")
            if val and unit and not str(val).endswith(str(unit)):
                val = f"{val}{unit}"
            entries.append([label, normalize_stat_value(label, val)])
        return trim_trailing_headers(entries)

    def build_base_stats_dict(items):
        d = {}
        for k, v in build_stat_entries(items):
            if v != "":
                d[k] = v
        return d

    name, names = resolve_hero_names(hero["title"])

    skills = []
    for skill in data["skills"]:
        if skill.get("type") == "unused":
            continue
        norm_key = normalize_key(skill.get("key", "Passive"))
        s_name = unescape(skill.get("name", "")).replace("\xa0", " ").strip()
        s_desc = unescape(skill.get("description", "")).replace("\xa0", " ").strip()
        if name.upper() == "ADAM WARLOCK" and norm_key == "F" and "Take to the skies" in s_desc:
            s_name = "SOARING SURGE"
        s_type = 1 if skill.get("type") == "normal" else 2
        skills.append({
            "type": s_type,
            "form_index": skill.get("variantIndex", 0),
            "key": norm_key,
            "key_trans": KEY_TRANSLATIONS.get(norm_key, {"ko": norm_key, "ja": norm_key}),
            "name": s_name,
            "icon": skill.get("icon", ""),
            "description": s_desc,
            "stats": build_stat_entries(skill.get("stats", [])),
        })

    skills.sort(key=lambda s: (s.get("form_index", 0), KEY_ORDER.get(s.get("key", ""), 15)))

    teamups = []
    for number, teamup in enumerate(data.get("teamups", []), 1):
        for tier in teamup.get("tiers", []):
            t_desc = unescape(tier.get("description", "")).replace("\xa0", " ").strip()
            t_name = unescape(tier.get("name", "")).replace("\xa0", " ").strip()
            partner = extract_partner_name(t_desc, self_name=name)
            partner_en, partner_local = resolve_hero_names(partner)
            t_key = normalize_key(tier.get("key", "Passive"))
            teamups.append({
                "loadout_number": number,
                "loadout_name": t_name or f"Loadout {number}",
                "tier": tier.get("tier", "base"),
                "name": t_name,
                "icon": tier.get("icon", ""),
                "description": t_desc,
                "partner_avatar": teamup.get("avatar", ""),
                "partner_name": {
                    "en": partner_en,
                    "ko": partner_local.get("ko", partner_en),
                    "ja": partner_local.get("ja", partner_en),
                },
                "key": t_key,
                "key_trans": KEY_TRANSLATIONS.get(t_key, {"ko": t_key, "ja": t_key}),
                "stats": build_stat_entries(tier.get("stats", [])),
            })

    variants = data.get("variants", [])
    raw_forms = []
    for v in variants:
        v_stats = build_base_stats_dict(v.get("stats", []))
        if v_stats:
            raw_forms.append({
                "name": unescape(v.get("name", "")).strip(),
                "avatar": v.get("avatar", ""),
                "stats": v_stats,
            })

    base_stats = dict(raw_forms[0]["stats"]) if raw_forms else {}
    base_stats.setdefault("Movement Mode", "Flight" if name.upper() in ("IRON MAN", "STORM", "HUMAN TORCH", "ULTRON") else "Ground")

    return {
        "id": hero["id"],
        "name": name,
        "names": {"en": name, **names},
        "role": primary_role,
        "roles": roles,
        "role_name": ROLE_TRANSLATIONS.get(primary_role, {"en": primary_role, "ko": primary_role, "ja": primary_role}),
        "avatar": hero["avatar"],
        "full_img": hero["full_img"],
        "base_stats": base_stats,
        "raw_forms": raw_forms,
        "skills": skills,
        "teamups": teamups,
    }


def main():
    print("Fetching Marvel Rivals official hero roster...")
    heroes = parse_hero_list()
    print(f"Discovered {len(heroes)} heroes. Extracting details...")

    results = []
    failed = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(parse_hero_page, h): h for h in heroes}
        for future in as_completed(futures):
            h_info = future.result()
            if h_info:
                results.append(h_info)
                print(f" -> {h_info['name']} [{h_info['role']}] (Skills: {len(h_info['skills'])}, Team-Ups: {len(h_info['teamups'])})")
            else:
                failed.append(futures[future]["title"])

    results.sort(key=lambda x: x["name"])

    if failed or len(results) != len(heroes):
        raise RuntimeError(f"[ABORT] Failed to extract: {', '.join(failed)}. Preserving current heroes.json.")
    invalid = [h["name"] for h in results if not h["skills"] or not h["base_stats"].get("Health")]
    if invalid:
        raise RuntimeError(f"[ABORT] Missing skills or health: {', '.join(invalid)}. Preserving current heroes.json.")
    untranslated = [h["name"] for h in results if h["names"]["ko"] == h["name"] or h["names"]["ja"] == h["name"]]
    if untranslated:
        print(f"[WARNING] Korean and Japanese names need translation: {', '.join(untranslated)}. English names will be used.")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    heroes_file = os.path.join(data_dir, "heroes.json")
    if os.path.exists(heroes_file):
        with open(heroes_file, encoding="utf-8") as f:
            previous = json.load(f)
        previous_ids = {h["id"] for h in previous if not h["id"].startswith("deadpool-")}
        if any(h["id"].startswith("deadpool-") for h in previous) and not any(h["name"].upper() == "DEADPOOL" for h in results):
            raise RuntimeError("[ABORT] Previously published Deadpool is missing.")
        current_ids = {h["id"] for h in results}
        missing = previous_ids - current_ids
        if missing:
            raise RuntimeError(f"[ABORT] Previously published hero IDs missing: {sorted(missing)}. Preserving current heroes.json.")
    with open(heroes_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Saved {len(results)} heroes into {heroes_file}")


if __name__ == "__main__":
    main()
