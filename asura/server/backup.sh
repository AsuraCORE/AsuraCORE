#!/bin/bash
# Dumps auth/characters (+ world/hotfixes with "full") to /opt/asuracore/backups, keeps 14 days
set -e
DIR=/opt/asuracore/backups; mkdir -p $DIR; TS=$(date +%F_%H%M)
DBS="auth characters"; [ "$1" = full ] && DBS="$DBS world hotfixes"
for db in $DBS; do mysqldump --single-transaction --routines $db | gzip > $DIR/${db}_$TS.sql.gz; done
find $DIR -name "*.sql.gz" -mtime +14 -delete
echo BACKUP_OK $DIR
