#!/bin/bash
# Let's Encrypt IP certificate (shortlived profile, ~6 days) for bnetserver.
# Needs port 80 free. Cron /etc/cron.d/asuracore-cert runs it twice a day; renews when <3 days left.
set -e
IP=193.124.184.192
P=/opt/asuracore/cert
BIN=/opt/asuracore/server/bin
lego run --accept-tos --path $P --domains $IP --http --profile shortlived --renew-days 3
if ! cmp -s $P/certificates/$IP.crt $BIN/bnetserver.cert.pem; then
  cp $P/certificates/$IP.crt $BIN/bnetserver.cert.pem
  cp $P/certificates/$IP.key $BIN/bnetserver.key.pem
  systemctl restart asura-bnetserver
fi
echo CERT_OK
