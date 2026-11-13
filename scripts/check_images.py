#!/usr/bin/env python3
"""Check image URLs referenced by the published hero data."""
import concurrent.futures
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE_KEYS = {"avatar", "full_img", "icon", "partner_avatar"}


def collect(value, urls):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in IMAGE_KEYS and isinstance(item, str) and item:
                urls.add(item)
            else:
                collect(item, urls)
    elif isinstance(value, list):
        for item in value:
            collect(item, urls)


def check(url):
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            content_type = response.headers.get_content_type()
            response.read(16)
        if not content_type.startswith("image/"):
            return url, f"Unexpected content type: {content_type}"
    except Exception as exc:
        return url, str(exc)
    return None


def main():
    with (ROOT / "data/heroes.json").open(encoding="utf-8") as file:
        heroes = json.load(file)
    urls = set()
    collect(heroes, urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        failures = [result for result in executor.map(check, sorted(urls)) if result]
    print(f"Checked {len(urls)} image URLs: {len(failures)} failed")
    for url, error in failures:
        print(f"{url}: {error}")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
