#!/usr/bin/env python3
# 이브리프 장표 페이지 → 세로 18:9 쇼츠 (세로 스크롤 전환).  python3 shorts.py --gaps | [스틸 초 ...]
import re, sys, json, pathlib, subprocess, shutil, os
import numpy as np
from playwright.sync_api import sync_playwright
from align import align, mark_time
base = pathlib.Path('.').resolve(); CARDS = base / 'cards'
FPS, SCROLL, WIPE = 30, 1.1, 0.45
CARD_TOP = 430; SUB_TOP = CARD_TOP + 1080 + 44
TITLE1, TITLE2 = "日 '핵잠 검토' 추진", '韓 핵잠은 제자리'
OUT = pathlib.Path('/home/user/ebrief/japan_nuclear_sub_20261111/eBrief_일본핵잠_쇼츠_나레이션.mp4')
_pp = json.load(open('ppe.json')); P, PE = _pp['P'], _pp['PE']
SUBS_TXT = json.load(open('subs.json'))
SPOKEN = json.load(open('spoken.json'))

# ---- fonts ----
F = base / 'fonts'
if not (F / 'BlackHanSans-Regular.ttf').exists():
    F.mkdir(exist_ok=True)
    for pkg in ['@fontsource/noto-serif-kr', '@fontsource/noto-sans-kr', 'pretendard']:
        tgz = subprocess.run(['npm', 'pack', pkg, '--silent'], cwd=F, capture_output=True, text=True).stdout.strip().splitlines()[-1]
        d = F / pkg.split('/')[-1]; d.mkdir(exist_ok=True); subprocess.run(['tar', 'xzf', tgz, '-C', str(d)], cwd=F, check=True)
    subprocess.run(['curl', '-sSfL', '-o', str(F / 'BlackHanSans-Regular.ttf'), 'https://raw.githubusercontent.com/google/fonts/main/ofl/blackhansans/BlackHanSans-Regular.ttf'], check=True)
links = ''.join(f'<link rel="stylesheet" href="file://{F}/{fam}/package/{w}.css">' for fam, ws in [('noto-serif-kr', [400, 700, 900]), ('noto-sans-kr', [400, 500, 700, 900])] for w in ws)
PW = F / 'pretendard/package/dist/web/static/woff2'

# ---- audio ----
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(base / 'narr.wav'), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; n = len(x) // 160
db = 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-6)
low = db < -45; GAPS = []; i = 0
while i < n:
    if low[i]:
        j = i
        while j < n and low[j]: j += 1
        if j - i >= 5: GAPS.append((i / 100, j / 100))
        i = j
    else: i += 1
if sys.argv[1:2] == ['--gaps']:
    print('length', len(x) / 16000); print([(a, b, round(b - a, 2)) for a, b in GAPS if b - a >= 0.1]); sys.exit()
N = len(SUBS_TXT); AUDIO_END = PE[-1]; TOTAL = round(AUDIO_END + 1.0, 2)
SUBS = align(SUBS_TXT, json.load(open(base / 'tokens.json')), SPOKEN, P, PE)
for s in SUBS: print(s)
STARTS = [0] + [p - 0.55 for p in P[1:]]

# ---- page ----
src = (CARDS / 'index.html').read_text()
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
css = re.sub(r'\nbody \{.*?\}\n', '\n', css, flags=re.S); css = re.sub(r'\n\.slot \{[^}]*\}', '\n', css)
cards = [re.sub(r'src="([^":/]+)"', lambda m: f'src="file://{CARDS}/{m.group(1)}"', c) for c in re.findall(r'(<section class="card[^"]*".*?</section>)', src, re.S)]
assert len(cards) == N, (len(cards), N)
slots = ''.join(f'<div class="slot" data-i="{i}"><div class="scale">{c}</div></div>' for i, c in enumerate(cards))
caps = ''.join(f'<div class="cap"><span>{t}</span></div>' for s, e, t, _, _ in SUBS)
html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">{links}<style>
@font-face{{font-family:'Pretendard';font-weight:700;src:url('file://{PW}/Pretendard-Bold.woff2') format('woff2')}}
@font-face{{font-family:'BHS';font-weight:100 900;src:url('file://{F}/BlackHanSans-Regular.ttf')}}
{css}
html,body{{margin:0;background:#000}}
#stage{{position:relative;width:1080px;height:2160px;background:#000;overflow:hidden}}
#title{{position:absolute;left:0;top:0;width:1080px;height:{CARD_TOP}px;box-sizing:border-box;padding:0 30px 40px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:4px;font-family:'BHS','Noto Sans KR';font-weight:900;font-size:102px;line-height:1.1;letter-spacing:-3px;text-align:center;white-space:nowrap}}
#vp{{position:absolute;left:0;top:{CARD_TOP}px;width:1080px;height:1080px;overflow:hidden}}
.slot{{position:absolute;left:0;top:0;width:1080px;height:1080px;overflow:hidden;transform-origin:50% 50%}}
.scale{{position:absolute;left:0;top:0;width:480px;height:480px;transform:scale(2.25);transform-origin:0 0}}
.card{{box-shadow:none!important}}
mark{{background-repeat:no-repeat!important;background-size:var(--w,0%) 100%!important;-webkit-box-decoration-break:slice;box-decoration-break:slice}}
.cap{{position:absolute;left:40px;width:1000px;top:{SUB_TOP}px;display:none;text-align:center}}
.cap span{{display:inline-block;background:#000;color:#FFF;font-family:'Pretendard';font-weight:700;font-size:60px;line-height:1.3;letter-spacing:-1px;padding:8px 26px 10px;word-break:keep-all}}
</style></head><body><div id="stage"><div id="title"><div style="color:#FFFFFF">{TITLE1}</div><div style="color:#E3242B">{TITLE2}</div></div><div id="vp">{slots}</div>{caps}</div></body></html>"""
work = base / 'video_work'; shutil.rmtree(work, ignore_errors=True); (work / 'frames').mkdir(parents=True)
(work / 'shorts.html').write_text(html, encoding='utf-8')

def bigrams(t): t = re.sub(r'\s', '', t); return {t[i:i + 2] for i in range(len(t) - 1)}
ease_out = lambda t: 1 - (1 - t) ** 3
def bez(p1x, p1y, p2x, p2y):   # 이브리프 브리핑과 같은 모던 스프링 스크롤 곡선
    bx = lambda t: 3 * p1x * t * (1 - t) ** 2 + 3 * p2x * t * t * (1 - t) + t ** 3
    by = lambda t: 3 * p1y * t * (1 - t) ** 2 + 3 * p2y * t * t * (1 - t) + t ** 3
    def f(v):
        if v <= 0: return 0.0
        if v >= 1: return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2; lo, hi = (mid, hi) if bx(mid) < v else (lo, mid)
        return by((lo + hi) / 2)
    return f
SCR = bez(.2, 1.0, .32, 1)
JS = """(st) => {
  document.querySelectorAll('.slot').forEach(s => { const i = +s.dataset.i; const [y, op, sc] = st.slots[i];
    s.style.transform = 'translateY(' + y + 'px) scale(' + sc + ')'; s.style.opacity = op; s.style.visibility = Math.abs(y) >= 1080 ? 'hidden' : 'visible';
    s.querySelectorAll('mark').forEach((m, j) => m.style.setProperty('--w', (st.marks[i][j] * 100) + '%')); });
  document.querySelectorAll('.cap').forEach((d, k) => d.style.display = k === st.sub ? 'block' : 'none'); }"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium'); pg = b.new_page(viewport={'width': 1080, 'height': 2160})
    pg.goto(f'file://{work}/shorts.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1500)
    marks = pg.evaluate("() => [...document.querySelectorAll('.slot')].map(s => [...s.querySelectorAll('mark')].map(m => m.textContent))")
    MARK_T = []
    for ci, ms in enumerate(marks):
        row = []
        for mt in ms:
            cand = [c for c in SUBS if c[3] == ci]
            best = max(cand, key=lambda c: len(bigrams(mt) & bigrams(c[2])))
            mt_t = max(best[0], mark_time((best[3], best[4]), best[2], mt, SPOKEN))
            row.append(max(mt_t, STARTS[ci] + 0.6 if ci else 0.6)); print(f'장{ci+1} 하이라이트 "{mt}" → "{best[2]}" {row[-1]:.2f}s')
        MARK_T.append(row)
    two = pg.evaluate("() => { const r=[]; document.querySelectorAll('.cap').forEach(d=>{d.style.display='block'; if (d.getBoundingClientRect().height>100) r.push(d.textContent); d.style.display='none';}); return r; }")
    print('2줄 자막(줄일 것):', two)
    tw = pg.evaluate("() => [...document.querySelectorAll('#title div')].map(d => d.scrollWidth)"); print('제목 폭:', tw)
    def state(t):
        # 현재 몇 번째 스크롤 구간인지: 페이지 전체가 위로 1080px씩 이어 올라감
        k = max([0] + [i for i in range(1, N) if t >= STARTS[i]])
        pos = (k - 1) + SCR(min(1, (t - STARTS[k]) / SCROLL)) if k > 0 else 0.0
        st = {'slots': [], 'marks': [], 'sub': -1}
        for i in range(N):
            y = i * 1080 - round(pos * 1080); op, sc = 1.0, 1.0
            if i == 0: p = min(1, t / 0.5); op = ease_out(p); sc = 0.92 + 0.08 * ease_out(p)
            st['slots'].append((y, round(op, 3), round(sc, 4)))
            st['marks'].append([1.0 for m in MARK_T[i]])   # 하이라이트는 처음부터 칠해진 상태
        for kk, (s, e, *_r) in enumerate(SUBS):
            if s <= t < e: st['sub'] = kk
        return st
    if sys.argv[1:]:
        for s in sys.argv[1:]: pg.evaluate(JS, state(float(s))); pg.screenshot(path=str(base / f'still_{s}.jpg'), type='jpeg', quality=85)
        b.close(); sys.exit()
    prev = None
    for f in range(int(round(TOTAL * FPS))):
        st = state(f / FPS); key = json.dumps(st); dst = work / 'frames' / f'{f:05d}.jpg'
        if key == prev: os.link(work / 'frames' / f'{f-1:05d}.jpg', dst); continue
        pg.evaluate(JS, st); pg.screenshot(path=str(dst), type='jpeg', quality=92); prev = key
    b.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(base / 'narr.wav'), '-af', 'apad=pad_dur=1.2', '-t', str(TOTAL), '-ar', '48000', str(work / 'audio.wav')], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(work / 'frames/%05d.jpg'), '-i', str(work / 'audio.wav'), '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(OUT)], check=True)
print('DONE', OUT)
