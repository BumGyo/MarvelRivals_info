with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find("xt-wrap")
start = max(0, idx - 800)
end = min(len(code), idx + 2500)
snippet = code[start:end]

with open('scratch/xt_snippet_utf8.txt', 'w', encoding='utf-8') as f:
    f.write(snippet)

print("Saved xt_snippet_utf8.txt")
