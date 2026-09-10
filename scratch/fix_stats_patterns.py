patterns = [
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per round$",
        "ko": "$1 발당 데미지",
        "ja": "$1 発あたりのダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per tick$",
        "ko": "$1 틱당 데미지",
        "ja": "$1 1tickあたりのダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*damage per second$",
        "ko": "초당 $1 데미지",
        "ja": "秒間 $1 ダメージ"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*rounds per second$",
        "ko": "초당 $1발",
        "ja": "秒間 $1発"
    },
    {
        "regex": r"^Falloff begins at (\d+m), decreasing to (\d+%) at (\d+m)$",
        "ko": "$1부터 감쇠 시작, $3에서 $2로 감소",
        "ja": "$1から減衰開始、$3で$2に低下"
    },
    {
        "regex": r"^Falloff begins at (\d+m), decreasing to (\d+) at (\d+m)$",
        "ko": "$1부터 감쇠 시작, $3에서 $2로 감소",
        "ja": "$1から減衰開始、$3で$2に低下"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*spherical radius$",
        "ko": "반경 $1 구형 범위",
        "ja": "半径 $1 の球状範囲"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?m)\s*radius$",
        "ko": "반경 $1",
        "ja": "半径 $1"
    },
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s) to recharge$",
        "ko": "$1회 충전 (충전당 $2 소요)",
        "ja": "$1回チャージ (1チャージ $2)"
    },
    {
        "regex": r"^(\d+)\s*charges?, with each charge taking (\d+(?:\.\d+)?s)$",
        "ko": "$1회 충전 (충전당 $2 소요)",
        "ja": "$1回チャージ (1チャージ $2)"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*/\s*s$",
        "ko": "초당 $1",
        "ja": "毎秒 $1"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*s$",
        "ko": "$1초",
        "ja": "$1秒"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*m$",
        "ko": "$1m",
        "ja": "$1m"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*m/s$",
        "ko": "$1 m/s",
        "ja": "$1 m/s"
    },
    {
        "regex": r"^(\d+(?:\.\d+)?)\s*%$",
        "ko": "$1%",
        "ja": "$1%"
    }
]

import json

with open('data/translations/stats.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

stats['patterns'] = patterns

with open('data/translations/stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("Updated data/translations/stats.json cleanly with patterns!")
