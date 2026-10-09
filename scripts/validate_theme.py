#!/usr/bin/env python3
"""Statische Prüfung des HACS-Theme-Repos (Struktur, YAML, Farbwerte, card-mod)."""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COLOR_RE = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|\d{1,3}, \d{1,3}, \d{1,3})$")


def main() -> int:
    errors = []
    manifest = json.loads((ROOT / "hacs.json").read_text())
    theme_file = ROOT / "themes" / manifest["filename"]
    if not theme_file.is_file():
        errors.append(f"hacs.json filename zeigt auf fehlende Datei: {theme_file}")
        return report(errors)

    data = yaml.safe_load(theme_file.read_text())
    if not isinstance(data, dict) or len(data) != 1:
        errors.append("Theme-Datei muss genau ein Theme auf oberster Ebene enthalten")
        return report(errors)

    name, theme = next(iter(data.items()))
    modes = theme.get("modes", {})
    if "dark" not in modes:
        errors.append("modes.dark fehlt")
    for mode, palette in modes.items():
        for key, value in palette.items():
            if key.endswith("-color") and not COLOR_RE.match(str(value)):
                errors.append(f"{mode}.{key}: ungültiger Farbwert {value!r}")
    if theme.get("card-mod-theme") not in (None, name):
        errors.append(f"card-mod-theme muss '{name}' sein")
    return report(errors)


def report(errors) -> int:
    for e in errors:
        print(f"FEHLER: {e}")
    print("OK" if not errors else f"{len(errors)} Fehler")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
