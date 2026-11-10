import json, re, difflib
def norm(t, rep):
    for k, v in rep.items(): t = t.replace(k, v)
    return re.sub(r'[^0-9A-Za-z가-힣]', '', t).lower()
def char_times(tokens):
    toks = [(re.sub(r'[^0-9A-Za-z가-힣]', '', t.replace('▁', '')).lower(), ts) for t, ts in tokens]
    toks = [(t, ts) for t, ts in toks if t]
    chars, times = [], []
    for k, (t, ts) in enumerate(toks):
        nxt = toks[k + 1][1] if k + 1 < len(toks) else ts + 0.15
        step = min(nxt - ts, 0.12 * len(t)) / len(t)
        for j, c in enumerate(t): chars.append(c); times.append(ts + j * step)
    return ''.join(chars), times
def align(subs_txt, tokens, rep, P, PE, lead=0.12):
    hyp, times = char_times(tokens)
    ref = ''.join(norm(c, rep) for caps in subs_txt for c in caps)
    m = {}
    for a, b, size in difflib.SequenceMatcher(None, ref, hyp, autojunk=False).get_matching_blocks():
        for i in range(size): m[a + i] = times[b + i]
    def t_at(i):  # 매칭 안 된 글자는 앞뒤 매칭 글자 사이 보간
        if i in m: return m[i]
        lo = max([x for x in m if x < i], default=None); hi = min([x for x in m if x > i], default=None)
        if lo is None: return m[hi]
        if hi is None: return m[lo]
        return m[lo] + (m[hi] - m[lo]) * (i - lo) / (hi - lo)
    global CHAR_T
    CHAR_T, starts, pos = {}, {}, 0
    for k, caps in enumerate(subs_txt):
        for j, c in enumerate(caps):
            L = len(norm(c, rep)); CHAR_T[(k, j)] = [t_at(pos + i) for i in range(L)]; starts[(k, j)] = CHAR_T[(k, j)][0]; pos += L
    SUBS = []
    for k, caps in enumerate(subs_txt):
        for j, c in enumerate(caps):
            s = P[k] if j == 0 else max(P[k], starts[(k, j)] - lead)   # 말보다 0.12초 먼저 뜬다
            end = (starts[(k, j + 1)] - lead) if j + 1 < len(caps) else (P[k + 1] if k + 1 < len(subs_txt) else PE[-1] + 0.6)
            SUBS.append((round(s, 3), round(end, 3), c, k, j))
    return SUBS
def mark_time(chunk_key, chunk_txt, mark_txt, rep):   # 하이라이트 구절의 첫 글자들을 말하는 시각 − 0.1초
    import align as A
    nc, nm = norm(chunk_txt, rep), norm(mark_txt, rep)
    for L in (4, 3, 2):
        i = nc.find(nm[:L])
        if i >= 0: return A.CHAR_T[chunk_key][i] - 0.1
    return A.CHAR_T[chunk_key][0]
