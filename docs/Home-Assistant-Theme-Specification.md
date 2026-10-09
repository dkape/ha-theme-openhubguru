# Home Assistant Custom Theme: OpenHubGuru Design-Abstraktion & HACS-Spezifikation

Dieses Dokument bildet das Ergebnis von **Teilaufgabe 1/3 (Karte `c-6e41d4`)** ab:
Recherche der CSS- & YAML-Strukturen für HACS-Themes und Definition der Design-Abstraktionsschicht aus OpenHubGuru für Home Assistant.

---

## 1. HACS Custom Theme Repository- & Dateianforderungen

Damit ein Home Assistant Theme sauber über **HACS (Home Assistant Community Store)** als Custom Repository (Default oder Custom Repository URL aus Gitea) eingebunden und geladen werden kann, müssen folgende Spezifikationen strikt eingehalten werden:

### 1.1 Verzeichnis- & Dateistruktur des Theme-Repositories
HACS erwartet für die Kategorie `theme` eine feste Konvention:

```text
ha-theme-openhubguru/
├── .git/
├── .gitea/
│   └── workflows/                # CI/CD: Linting & Release Automation
│       └── release.yaml
├── themes/
│   └── openhubguru.yaml          # Das eigentliche Home Assistant Theme
├── hacs.json                     # HACS Manifest Metadaten
├── README.md                     # Doku mit Screenshots & Einbindung
└── LICENSE                       # Lizenz (z.B. MIT)
```

> **Wichtig für HACS:**
> 1. Die Themendatei **muss** im Unterordner `themes/` liegen (z.B. `themes/openhubguru.yaml`).
> 2. Pro Theme-Repository sollte genau eine Theme-Datei oder ein eindeutiges Theme-Verzeichnis vorliegen. HACS lädt den Inhalt von `themes/` in den HA-Ordner `/config/themes/`.

### 1.2 HACS Manifest (`hacs.json`)
Im Root-Verzeichnis des Theme-Repositories:
```json
{
  "name": "OpenHubGuru Dark Theme",
  "filename": "openhubguru.yaml",
  "render_readme": true,
  "homeassistant": "2024.1.0"
}
```

### 1.3 Einbindung in Home Assistant (`configuration.yaml`)
Damit Home Assistant Themes lädt:
```yaml
frontend:
  themes: !include_dir_merge_named themes/
```
In HA kann das Theme dann nach Neuladen der Themes via Entwicklerwerkzeuge oder Dienst `frontend.reload_themes` im Benutzerprofil ausgewählt werden.

---

## 2. OpenHubGuru Design-Abstraktionsschicht

Die visuelle Identität von OpenHubGuru basiert auf einem immersiven **OLED High-Tech Darkmode** mit Cyan/Sky-Akzentfarben, semantischen Status-Farben (Pulse/Mesh) und dezenten Glassmorphism-Effekten.

### 2.1 Farbpalette (Color Palette)

| Semantische Rolle | Hex / RGBA | OpenHubGuru CSS / Token | Home Assistant Variable Mapping |
| :--- | :--- | :--- | :--- |
| **Hintergrund (OLED Base)** | `#05070c` | `--oled-bg` / `bg-oled-bg` | `primary-background-color`, `lovelace-background` |
| **Oberfläche (Surface / Header)** | `#0d131f` (90% Alpha) | `--oled-surface` | `app-header-background-color`, `sidebar-background-color` |
| **Karten (Card Background)** | `#121a2b` | `--oled-card` | `card-background-color`, `ha-card-background` |
| **Rahmen & Divider (Borders)** | `#1e293b` | `--oled-border` | `divider-color`, `ha-card-border-color` |
| **Primärakzent (Brand / Cyan)** | `#38bdf8` | `--brand: #38BDF8` | `primary-color`, `accent-color`, `state-active-color` |
| **Primärakzent Hover** | `#0ea5e9` | `--brand-hover` | `state-hover-color` |
| **Primärakzent Glow / Subtil**| `rgba(56, 189, 248, 0.15)` | `--brand-glow` | `ha-card-box-shadow` (Glow), Sub-Badges |
| **Text Hauptfarbe (Primary)** | `#f8fafc` / `#ffffff` | `text-slate-100` / `text-white` | `primary-text-color` |
| **Text Sekundärfarbe (Muted)** | `#94a3b8` | `text-slate-400` | `secondary-text-color` |
| **Text Disabled / Faint** | `#64748b` | `text-slate-500` | `disabled-text-color` |

#### Status- & Pulse-Farben (OpenHubGuru Phase 10 / 11)
Diese Farben werden für Entity-Status, Alarme und Badges verwendet:
- **Status OK / Healthy:** `#34d399` (`rgba(52, 211, 153, 0.12)`) -> `state-on-color`, `success-color`
- **Status Idle / Info:** `#38bdf8` (`rgba(56, 189, 248, 0.10)`) -> `info-color`
- **Status Warning:** `#fbbf24` (`rgba(251, 191, 36, 0.12)`) -> `warning-color`, `state-alert-color`
- **Status Error / Critical:** `#fb7185` (`rgba(251, 113, 133, 0.14)`) -> `error-color`, `state-problem-color`
- **Status Neutral / Standby:** `#64748b` -> `state-unavailable-color`

### 2.2 Typografie (Typography)
- **Primary Font Family:** System Sans-Serif (`system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`)
- **Code / Monospace Font Family:** `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace`
- **Font Weights:** Regular `400`, Medium `500`, Semi-Bold `600`, Bold `700`
- **Text-Transform:** Sub-Labels, KPIs und Metriken verwenden `letter-spacing: 0.04em` bis `0.08em` in Großbuchstaben / Monospace.

### 2.3 Layout-, Card- und Form-Prinzipien
1. **Card Radius:** `border-radius: 12px` (`0.75rem`), subtilere Pills und Badges mit `border-radius: 9999px` oder `6px`.
2. **Borders & Outlines:** Schlanke Borders (`1px solid #1e293b`).
3. **Card Mod & Box-Shadows:**
   - Standard: `box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5)`
   - Subtle Accent Glow: `box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.02) inset, 0 0 20px -10px rgba(56, 189, 248, 0.25)`
4. **Glassmorphism:**
   - `backdrop-filter: blur(12px);`
   - `background: rgba(18, 26, 43, 0.75);`
5. **Scrollbars:** Schlank (`6px`), Thumb `#1e293b` (Hover: `#38bdf8`), Track `rgba(5, 7, 12, 0.6)`.

---

## 3. Entwurf der Home Assistant Theme YAML-Struktur (`openhubguru.yaml`)

Home Assistant unterstützt sowohl statische Root-Variablen als auch `modes: { dark: ... }` sowie Integration von `card-mod`.
Hier ist die für Teilaufgabe 2 vorbereitete Kern-Spezifikation:

```yaml
openhubguru:
  # Base Setup
  modes:
    dark:
      # Backgrounds
      primary-background-color: "#05070c"
      card-background-color: "#121a2b"
      secondary-background-color: "#0d131f"
      app-header-background-color: "#0d131f"
      sidebar-background-color: "#0d131f"
      lovelace-background: "#05070c"

      # Accent & Brand Colors
      primary-color: "#38bdf8"
      accent-color: "#38bdf8"
      light-primary-color: "#7dd3fc"
      dark-primary-color: "#0284c7"

      # Text Colors
      primary-text-color: "#f8fafc"
      secondary-text-color: "#94a3b8"
      text-primary-color: "#f8fafc"
      disabled-text-color: "#64748b"

      # Borders & Dividers
      divider-color: "#1e293b"
      ha-card-border-color: "#1e293b"
      ha-card-border-width: "1px"
      ha-card-border-radius: "12px"
      ha-card-box-shadow: "0 4px 20px -2px rgba(0, 0, 0, 0.5)"

      # States & Badges
      state-active-color: "#38bdf8"
      state-icon-color: "#94a3b8"
      state-icon-active-color: "#38bdf8"
      state-on-color: "#34d399"
      state-alarm-triggered-color: "#fb7185"

      # Feedback / Semantic Colors
      success-color: "#34d399"
      warning-color: "#fbbf24"
      error-color: "#fb7185"
      info-color: "#38bdf8"

      # Navigation & Sliders
      sidebar-selected-text-color: "#38bdf8"
      sidebar-selected-icon-color: "#38bdf8"
      switch-checked-button-color: "#38bdf8"
      switch-checked-track-color: "rgba(56, 189, 248, 0.3)"
      slider-color: "#38bdf8"
      slider-bar-color: "#1e293b"

  # Card-Mod Integration (Optional / Advanced Styling)
  card-mod-theme: "openhubguru"
  card-mod-root: |
    app-toolbar {
      border-bottom: 1px solid #1e293b !important;
    }
  card-mod-card: |
    ha-card {
      backdrop-filter: blur(12px);
      transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    ha-card:hover {
      border-color: rgba(56, 189, 248, 0.4) !important;
    }
```

---

## 4. Bereitstellungsstrategie für Homelab & Gitea

1. **Gitea Repository:** Neues Repository `ha-theme-openhubguru` unter Organisation/Benutzer `kapeplus.de` (analog zu den anderen Homelab-Repos).
2. **HACS Custom Repository Integration:**
   - In Home Assistant unter HACS -> Drei Punkte (Menü oben rechts) -> "Benutzerdefinierte Repositories" (Custom repositories).
   - URL: `https://code.kapeplus.de/kapeplus.de/ha-theme-openhubguru` (oder lokaler K3s/LAN Git URL).
   - Kategorie: `Theme`.
3. **Automatisierung:** Bei Git Tags / Releases aktualisiert HACS das Theme direkt auf HA.

---

## 5. Nächste Schritte (Teilaufgabe 2 & 3 Vorschau)
- **Teilaufgabe 2/3:** Erstellung des dedizierten Git-Repositories `ha-theme-openhubguru` (in Gitea), Ausarbeiten der vollständigen `openhubguru.yaml` inklusive aller HA Lovelace Element-Mappings und `hacs.json`.
- **Teilaufgabe 3/3:** Bereitstellung / Release-Vorbereitung, Test-Verifikation in HA und Dokumentation im Homelab-Wiki / Knowledge Graph.
