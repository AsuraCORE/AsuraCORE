#!/bin/bash
# Extracts dbc/maps/vmaps/mmaps from the WoW client uploaded to /opt/asuracore/client
# (the folder that contains .build.info and Data/). Output -> /opt/asuracore/data
set -e
BIN=/opt/asuracore/server/bin
CLIENT=/opt/asuracore/client
OUT=/opt/asuracore/data
[ -f "$CLIENT/.build.info" ] || { echo "No client in $CLIENT (need .build.info + Data/)"; exit 1; }
cd "$CLIENT"
"$BIN/mapextractor"
"$BIN/vmap4extractor"
mkdir -p vmaps && "$BIN/vmap4assembler" Buildings vmaps
mkdir -p mmaps && "$BIN/mmaps_generator" --threads 14
mkdir -p "$OUT"
for d in dbc maps vmaps mmaps gt cameras; do [ -d "$d" ] && rm -rf "$OUT/$d" && mv "$d" "$OUT/"; done
rm -rf Buildings
echo EXTRACT_OK
