#!/usr/bin/env bash
# Copy VitaInk HUD package (lote 3 / v3.1 pintura aventura) into game + RCV trees.
# Excludes .venv
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
GAME_DEST="/workspace/nuevo-internet/vitaink-juego/public/assets/hud"
RCV_ROOT="/workspace/nuevo-internet/red-ciudadano-valladolid"
RCV_DEST="${RCV_ROOT}/web/vitaink/sprites/hud"

sync_one() {
  local DEST="$1"
  mkdir -p "${DEST}/svg" "${DEST}/png/128" "${DEST}/png/256" "${DEST}/png/512"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude '.venv' --exclude '_gen' --exclude 'masters' \
      "${SRC}/svg/" "${DEST}/svg/"
    rsync -a --delete "${SRC}/png/128/" "${DEST}/png/128/"
    rsync -a --delete "${SRC}/png/256/" "${DEST}/png/256/"
    rsync -a --delete "${SRC}/png/512/" "${DEST}/png/512/"
  else
    rm -rf "${DEST}/svg" "${DEST}/png/128" "${DEST}/png/256" "${DEST}/png/512"
    mkdir -p "${DEST}/svg" "${DEST}/png/128" "${DEST}/png/256" "${DEST}/png/512"
    cp -a "${SRC}/svg/." "${DEST}/svg/"
    cp -a "${SRC}/png/128/." "${DEST}/png/128/"
    cp -a "${SRC}/png/256/." "${DEST}/png/256/"
    cp -a "${SRC}/png/512/." "${DEST}/png/512/"
  fi
  cp -f "${SRC}/catalog.json" "${SRC}/inventory.json" "${SRC}/manifest.json" "${SRC}/README.md" "${DEST}/"
  echo "Synced VitaInk HUD v3.1 → ${DEST}"
  find "${DEST}" -type f | wc -l
}

sync_one "${GAME_DEST}"
if [[ -d "${RCV_ROOT}/web/vitaink" ]] || [[ -d "${RCV_DEST}" ]] || mkdir -p "${RCV_DEST}" 2>/dev/null; then
  sync_one "${RCV_DEST}"
fi
