with open('scratch/netease_index.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's format and print the block containing xt-wrap
idx = code.find("xt-wrap")
start = max(0, idx - 1000)
end = min(len(code), idx + 2000)
snippet = code[start:end]

print(snippet)
