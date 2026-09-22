#!/bin/bash
# Let's Encrypt certificate for the bnetserver host name (RSA, 90 days). Needs port 80 free.
# Cron /etc/cron.d/asuracore-cert runs it twice a day; renews when <30 days left.
set -e
H=193-124-184-192.sslip.io
P=/opt/asuracore/cert-dns
BIN=/opt/asuracore/server/bin
lego run --accept-tos --path $P --domains $H --http --key-type rsa2048 --renew-days 30
if ! cmp -s $P/certificates/$H.crt $BIN/bnetserver.cert.pem; then
  cp $P/certificates/$H.crt $BIN/bnetserver.cert.pem
  cp $P/certificates/$H.key $BIN/bnetserver.key.pem
  systemctl restart asura-bnetserver
fi
echo CERT_OK
