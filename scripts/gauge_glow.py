"""Rundskalen-Glow (ha-theme-openhubguru): card_mod-Objekt-Styles für Gauge-,
Modern-Circular-Gauge- und Thermostat-Karten. Objekt-Styles brauchen keinen
YAML-Parser in card-mod (der hängt unter HA 2026.10)."""
import json, sys
MARK = "/* OpenHubGuru-Glow Rundskala (ha-theme-openhubguru) */\n"
def glow(sel, var):
    return f"{MARK}{sel} {{\n  filter: drop-shadow(0 0 4px var({var})) drop-shadow(0 0 10px var({var}));\n}}\n"
STYLES = {
    "gauge": {"ha-gauge$": glow(".value", "--gauge-color")},
    "custom:modern-circular-gauge": {"modern-circular-gauge-element$": glow("g > path.arc.current", "--gauge-color")},
    "thermostat": {"ha-state-control-climate-temperature$ ha-control-circular-slider$":
                   glow("path.arc-active, path.target-border", "--control-circular-slider-color")},
}
n = 0
def walk(o):
    global n
    if isinstance(o, dict):
        if o.get("type") in STYLES:
            cm = o.setdefault("card_mod", {})
            st = cm.get("style", {})
            if isinstance(st, str):
                st = {".": st}
            st.update(STYLES[o["type"]]); cm["style"] = st; n += 1
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
cfg = json.load(open(sys.argv[1])); walk(cfg)
json.dump(cfg, open(sys.argv[2], "w"), ensure_ascii=False)
print(n, "Rundskalen")
