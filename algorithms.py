def naive_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            return i
    return -1

def kmp_search(text: str, pattern: str) -> int:
    if pattern == '':
        return 0

    def build_lps(p: str):
        lps = [0] * len(p)
        length = 0
        for i in range(1, len(p)):
            while length and p[i] != p[length]:
                length = lps[length - 1]
            if p[i] == p[length]:
                length += 1
                lps[i] = length
        return lps

    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return -1

def boyer_moore_search(text: str, pattern: str) -> int:
    def build_bad_char(p: str):
        table = {c: -1 for c in set(p)}
        for i, c in enumerate(p):
            table[c] = i
        return table

    n, m = len(text), len(pattern)
    bad_char = build_bad_char(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        skip = max(1, j - bad_char.get(text[s + j], -1))
        s += skip
    return -1

def rabin_karp_search(text: str, pattern: str) -> int:
    p, mod = 31, 1_000_000_009
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    def mod_inv(a, mod):
        return pow(a, mod - 2, mod)

    pattern_hash = text_hash = 0
    p_pow = 1
    for i in range(m):
        pattern_hash = (pattern_hash + (ord(pattern[i]) - ord('a') + 1) * p_pow) % mod
        text_hash = (text_hash + (ord(text[i]) - ord('a') + 1) * p_pow) % mod
        if i != m - 1:
            p_pow = (p_pow * p) % mod

    if pattern_hash == text_hash and text[:m] == pattern:
        return 0

    p_inv = mod_inv(p, mod)
    for i in range(m, n):
        text_hash = (text_hash - (ord(text[i - m]) - ord('a') + 1) + mod) % mod
        text_hash = (text_hash * p_inv) % mod
        text_hash = (text_hash + (ord(text[i]) - ord('a') + 1) * p_pow) % mod
        if pattern_hash == text_hash and text[i - m + 1:i + 1] == pattern:
            return i - m + 1
    return -1

