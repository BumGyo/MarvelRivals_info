import re

with open('scratch/hulk_page.html', 'r', encoding='utf-8') as f:
    hulk_html = f.read()

# Look for form names in hulk_page.html
scripts = re.findall(r'<script[^>]*src="([^"]+)"', hulk_html)
print("Scripts in Hulk page:", scripts)

# Look for text around type 0 in hulk page
matches = re.findall(r'<tr[^>]*>.*?</tr>', hulk_html, re.DOTALL)
print(f"Total trs in Hulk page: {len(matches)}")
for m in matches[:5]:
    txt = re.sub(r'<[^>]+>', ' ', m)
    txt = ' '.join(txt.split())
    print("TR:", txt)
