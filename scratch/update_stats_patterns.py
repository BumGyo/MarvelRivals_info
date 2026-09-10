import re

with open('scripts/translations_stats.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace r"\1" -> "$1", r"\2" -> "$2", r"\3" -> "$3"
content = re.sub(r'r"\\([1-9])', r'"$\1', content)
content = content.replace(r'r"^(\d+(?:\.\d+)?)/s$"', r'r"^(\d+(?:\.\d+)?)\s*/\s*s$"')

with open('scripts/translations_stats.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated translations_stats.py")
