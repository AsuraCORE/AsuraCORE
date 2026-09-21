#!/bin/bash
# git pull + build + install + restart
set -e
cd /opt/asuracore/src && git pull --ff-only
/opt/asuracore/build.sh 2>&1 | tee /opt/asuracore/build.log | grep -E "error|BUILD_OK|FAILED" || true
grep -q BUILD_OK /opt/asuracore/build.log || { echo "BUILD FAILED, see /opt/asuracore/build.log"; exit 1; }
systemctl restart asura-bnetserver asura-worldserver
echo UPDATE_OK
