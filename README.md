# OpenHubGuru Theme für Home Assistant

OLED-High-Tech-Darkmode mit Cyan/Sky-Akzent – die Designsprache von
[OpenHubGuru](https://code.kapeplus.de/kapeplus.de/open-hub-guru) als Home-Assistant-Theme.

| Rolle | Farbe |
| :--- | :--- |
| Hintergrund (OLED) | `#05070c` |
| Surface / Header / Sidebar | `#0d131f` |
| Karten | `#121a2b` |
| Rahmen | `#1e293b` |
| Brand / Akzent | `#38bdf8` (Hover `#0ea5e9`, Dark `#0369a1`) |
| OK / Info / Warnung / Fehler | `#34d399` / `#38bdf8` / `#fbbf24` / `#fb7185` |

## Installation über HACS

> **Hinweis:** HACS (auch 2.x) lädt Custom Repositories ausschließlich von **GitHub**.
> Ein reines Gitea-Repo lässt sich dort nicht hinzufügen – dafür wird ein GitHub-Spiegel
> des Gitea-Repos benötigt (Gitea *Push-Mirror*). Die URL unten ist dann die des Spiegels.

1. HACS → ⋮ → *Benutzerdefinierte Repositories*
2. URL des GitHub-Spiegels von `code.kapeplus.de/kapeplus.de/ha-theme-openhubguru`, Kategorie **Theme**
3. Theme installieren, dann sicherstellen, dass `configuration.yaml` Themes lädt:

   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
   ```

4. Dienst `frontend.reload_themes` ausführen und im Benutzerprofil **openhubguru** wählen.

Das Theme ist bewusst dark-only: dieselbe Palette gilt für `modes.dark` und `modes.light`.

## Optional: card-mod

Mit installiertem [card-mod](https://github.com/thomasloven/lovelace-card-mod) kommen
Glassmorphism-Karten (`backdrop-filter: blur(12px)`), ein Cyan-Glow beim Hover und schlanke
Scrollbars dazu. Ohne card-mod werden diese Schlüssel ignoriert.

## Entwicklung

```bash
pip install pyyaml
python3 scripts/validate_theme.py   # prüft Struktur, hacs.json, Farbwerte, card-mod-Name
scripts/simulate_hacs_install.sh    # HACS-Install in Wegwerf-Config + echtes HA check_config (Docker)
```

`simulate_hacs_install.sh` kopiert `themes/*` wie HACS nach `/config/themes/<repo>/`, legt eine
minimale `configuration.yaml` mit `!include_dir_merge_named themes` an und lässt Home Assistant
(`HA_VERSION`, Standard `2026.10.0`) die Konfiguration validieren. Schlägt bei ungültigen
Theme-Schlüsseln (z. B. unbekannter Modus) fehl.

Design-Herleitung: `docs/Home-Assistant-Theme-Specification.md` im OpenHubGuru-Repo.
