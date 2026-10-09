"""Fügt card_mod-Glow je Serie in ApexCharts-/Plotly-/Trend-Karten ein. Schreibt *.new.json."""
import json, re, sys

def rgba(c, a):
    c = c.strip()
    m = re.match(r'rgba?\(([^)]+)\)', c)
    if m:
        r, g, b = [x.strip() for x in m.group(1).split(',')[:3]]
    else:
        c = c.lstrip('#'); r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {a})'

def glow(c, bar=False):
    if c == NEUTRAL:
        return f'filter: drop-shadow(0 0 3px {rgba(c, 0.45)}) drop-shadow(0 0 8px {rgba(c, 0.2)});'
    if bar:
        return f'filter: drop-shadow(0 0 6px {rgba(c, 0.45)});'
    return f'filter: drop-shadow(0 0 3px {rgba(c, 0.8)}) drop-shadow(0 0 8px {rgba(c, 0.35)});'

NEUTRAL = '#f8fafc'  # Serien mit color_threshold (Gradient) -> heller, neutraler Glow
APEX_DEFAULT = ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0']
PLOTLY_DEFAULT = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
HEAD = '/* OpenHubGuru-Glow je Serie (ha-theme-openhubguru) */\n'

def apex(card):
    rules = []
    bar = (card.get('apex_config') or {}).get('chart', {}).get('type') == 'bar'
    for i, s in enumerate(card.get('series', [])):
        c = NEUTRAL if s.get('color_threshold') else (s.get('color') or APEX_DEFAULT[i % 5])
        rules.append(f'.apexcharts-series[data\\:realIndex="{i}"] path {{ {glow(c, bar or s.get("type") == "column")} }}')
    return rules

def plotly(card):
    rules = []
    for i, e in enumerate(card.get('entities', []), start=1):
        if not isinstance(e, dict): e = {}
        if e.get('type') == 'bar':
            c = (e.get('marker') or {}).get('color') or PLOTLY_DEFAULT[(i - 1) % 5]
            rules.append(f'.barlayer .trace:nth-of-type({i}) path {{ {glow(c, True)} }}')
        else:
            c = (e.get('line') or {}).get('color') or PLOTLY_DEFAULT[(i - 1) % 5]
            rules.append(f'.scatterlayer .trace:nth-of-type({i}) path.js-line {{ {glow(c)} }}')
    return rules

changed = []
def walk(o, path, name):
    if isinstance(o, dict):
        t = o.get('type'); rules = None
        if t == 'custom:apexcharts-card': rules = apex(o)
        elif t == 'custom:plotly-graph': rules = plotly(o)
        elif t == 'tile' and any(f.get('type') == 'trend-graph' for f in o.get('features', [])):
            rules = ['hui-card-features { filter: drop-shadow(0 0 3px var(--tile-color)) drop-shadow(0 0 8px var(--tile-color)); }']
        if rules:
            if 'card_mod' in o: print('SKIP (card_mod vorhanden)', name, path); 
            else:
                o['card_mod'] = {'style': HEAD + '\n'.join(rules) + '\n'}; changed.append((name, path, t, len(rules)))
        for k, v in o.items(): walk(v, f'{path}/{k}', name)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f'{path}[{i}]', name)

for name in sys.argv[1:]:
    c = json.load(open(f'./dash/{name}.json'))
    walk(c, '', name)
    json.dump(c, open(f'./dash/{name}.new.json', 'w'), ensure_ascii=False)
for x in changed: print(*x)
