#!/usr/bin/env bash

set -e
#set -v

CERT_NAME=service_certificate

# creates private key
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout $CERT_NAME.pem -out $CERT_NAME.pem <<EOF
MX
Mexico
Mexico
PulsarCloud
RDU
lenovo
fernando.aguilar@pulsarcloud.ml
EOF

echo

# creates certificate file (public key) in DER
openssl x509 -inform pem -in $CERT_NAME.pem -outform der -out $CERT_NAME.cer

echo

# https://www.lisenet.com/2014/convert-p7b-to-pfx-with-openssl/
#openssl req -new -x509 -days 365 -sha256 -nodes -out cert.cer -keyout cert.key
#openssl pkcs12 -export -in cert.cer -inkey cert.key -out cert.pfx
