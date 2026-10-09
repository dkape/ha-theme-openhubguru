#!/usr/bin/env bash
# Simuliert eine HACS-Theme-Installation in eine Wegwerf-HA-Konfiguration und
# validiert sie mit dem echten `check_config` von Home Assistant (Docker).
#   HA_VERSION=2026.10.0 scripts/simulate_hacs_install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HA_VERSION="${HA_VERSION:-2026.10.0}"
CONFIG="$(mktemp -d)"
trap 'rm -rf "$CONFIG"' EXIT

echo "== 1/3 Statische Repo-Prüfung"
python3 "$ROOT/scripts/validate_theme.py"

echo "== 2/3 HACS-Install emulieren (themes/* -> /config/themes/<repo>/)"
REPO="$(basename "$ROOT")"
mkdir -p "$CONFIG/themes/$REPO"
cp "$ROOT"/themes/*.yaml "$CONFIG/themes/$REPO/"
cat > "$CONFIG/configuration.yaml" <<'YAML'
homeassistant:
  name: theme-test
frontend:
  themes: !include_dir_merge_named themes
YAML
find "$CONFIG/themes" -type f

echo "== 3/3 Home Assistant $HA_VERSION check_config"
OUT="$(docker run --rm -v "$CONFIG:/config" \
  "ghcr.io/home-assistant/home-assistant:$HA_VERSION" \
  python -m homeassistant --script check_config -c /config --info frontend 2>&1)" || {
  echo "$OUT"; echo "FEHLER: check_config fehlgeschlagen"; exit 1; }
echo "$OUT" | tail -n 20
if echo "$OUT" | grep -qiE "invalid config|Failed config"; then
  echo "FEHLER: Theme-Konfiguration ungültig"; exit 1
fi
echo "$OUT" | grep -q "openhubguru" || { echo "FEHLER: Theme nicht geladen"; exit 1; }
echo "OK: Theme wird von HA $HA_VERSION geladen"
