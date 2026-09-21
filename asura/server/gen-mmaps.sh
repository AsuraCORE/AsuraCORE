#!/bin/bash
# Generates mmaps (pathfinding) from /opt/asuracore/data/{maps,vmaps,dbc}. Takes 1-3 h.
set -e
cd /opt/asuracore/data
mkdir -p mmaps
/opt/asuracore/server/bin/mmaps_generator --threads 15
echo MMAPS_OK
