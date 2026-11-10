import json, math, sys
G = sys.argv[1]
MW, H = 206, 218                      # map box (left part of 440x218 svg)
LON0, LON1 = 126.25, 127.20
LATC = 37.63; CO = math.cos(math.radians(LATC))
k = MW / ((LON1 - LON0) * CO)          # px per deg lat
LAT1 = LATC + (H / 2) / k
def P(lon, lat): return ((lon - LON0) * CO * k, (LAT1 - lat) * k)
def clamp(x, y): return (min(max(x, -4), MW + 4), min(max(y, -4), H + 4))
topo = json.load(open(f'{G}/package/land-10m.json'))
sc, tr = topo['transform']['scale'], topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)
def ring(r):
    pts = []
    for i in r:
        a = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts += a[1:] if pts else a
    return pts
def path(pts):
    out = []; last = None
    for lon, lat in pts:
        q = clamp(*P(lon, lat))
        if last and abs(q[0] - last[0]) < .6 and abs(q[1] - last[1]) < .6: continue
        out.append(q); last = q
    if len(out) < 3: return ''
    xs = [p[0] for p in out]; ys = [p[1] for p in out]
    if max(xs) < 0 or min(xs) > MW or max(ys) < 0 or min(ys) > H: return ''
    if max(xs) - min(xs) < 1.5 and max(ys) - min(ys) < 1.5: return ''
    return 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in out) + 'Z'
d = ''
for geo in topo['objects']['land']['geometries']:
    polys = geo['arcs'] if geo['type'] == 'MultiPolygon' else [geo['arcs']]
    for poly in polys:
        for r in poly: d += path(ring(r))
riv = json.load(open(f'{G}/rivers.json')); rd = ''
for f in riv['features']:
    if f['properties'].get('name') not in ('Han', 'Namhan'): continue
    g = f['geometry']; lines = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
    for l in lines:
        pts = [P(*p) for p in l]
        if not any(-10 < x < MW + 10 and -10 < y < H + 10 for x, y in pts): continue
        rd += 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
def lab(lon, lat, t, dx=6, dy=4, anchor='start', bold=False, dot=True):
    x, y = P(lon, lat)
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#5f5a53"/>' if dot else ''
    return s + f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}" font-size="12.5" font-weight="{700 if bold else 500}" fill="#5f5a53">{t}</text>'
ux, uy = P(126.683, 37.653)
items = [('10일 오전', '교육훈련 비행 중'), ('김포 운양동 공원', '훈련장 인근'), ('대대급 소형 무인기', '김포 육군 모 부대'), ('인명 피해 없음', '민간 피해도 없어')]
right = ''
for i, (t, s) in enumerate(items):
    y0 = 8 + i * 53
    right += (f'<circle cx="232" cy="{y0+11}" r="10.5" fill="var(--accent)"/><text x="232" y="{y0+15.5}" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{i+1}</text>'
              f'<text x="250" y="{y0+16.5}" font-family="var(--font-head)" font-size="17" font-weight="900" letter-spacing="-0.3" fill="var(--fg)">{t}</text>'
              f'<text x="250" y="{y0+35}" font-size="13" fill="var(--muted)">{s}</text>')
svg = f'''<svg viewBox="0 0 440 {H}" width="440" height="{H}" xmlns="http://www.w3.org/2000/svg" font-family="var(--font-body)">
<defs><clipPath id="mc"><rect width="{MW}" height="{H}"/></clipPath></defs>
<g clip-path="url(#mc)"><rect width="{MW}" height="{H}" fill="var(--sea)"/>
<path d="{d}" fill="var(--land)" stroke="var(--coast)" stroke-width=".8" stroke-linejoin="round"/>
<path d="{rd}" fill="none" stroke="var(--sea)" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="{rd}" fill="none" stroke="var(--coast)" stroke-width=".6" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>
{lab(126.978, 37.566, '서울', bold=True)}{lab(126.705, 37.456, '인천')}{lab(126.40, 37.83, '강화도', dot=False, dx=0, dy=0, anchor='middle')}
<text x="{P(126.86,37.60)[0]:.1f}" y="{P(126.86,37.60)[1]:.1f}" font-size="11" font-style="italic" fill="#8a847b" text-anchor="middle">한강</text>
<circle cx="{ux:.1f}" cy="{uy:.1f}" r="11" fill="var(--accent)" opacity=".18"/><circle cx="{ux:.1f}" cy="{uy:.1f}" r="4.6" fill="var(--accent)" stroke="#fff" stroke-width="1.4"/>
<text x="{ux+2:.1f}" y="{uy-13:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">김포 운양동</text>
<rect width="{MW}" height="{H}" fill="none" stroke="var(--line)"/></g>
{right}
</svg>'''
open(sys.argv[2], 'w').write(svg); print(len(svg), 'bytes', 'unyang', round(ux), round(uy))
