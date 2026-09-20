#!/usr/bin/env bash
set -euo pipefail
SRC="/workspace/vitaink-sprites-mari/world"
DST="/workspace/nuevo-internet/red-ciudadano-valladolid/web/vitaink/sprites/world"
mkdir -p "$DST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '_gen/' \
    --exclude 'COPY-TO-RCV.sh' \
    "$SRC/" "$DST/"
else
  mkdir -p "$DST"
  # copy biomes + meta (no _gen)
  for item in palette.json catalog.json inventory.json README.md \
              pradera bosque roca rio urbana cielo; do
    if [[ -e "$SRC/$item" ]]; then
      if [[ -d "$SRC/$item" ]]; then
        mkdir -p "$DST/$item"
        cp -a "$SRC/$item/." "$DST/$item/"
      else
        cp -f "$SRC/$item" "$DST/$item"
      fi
    fi
  done
fi
echo "Copied VitaInk world LOTE 1 → $DST"
echo -n "PNG count at destination: "
find "$DST" -name '*.png' | wc -l
