#! /usr/bin/python3

import OpenSSL
import os

if __name__ == '__main__':
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 1024)
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(0)
    
    subj = cert.get_subject()
    # Common Name: /CN
    subj.C = "MX"
    subj.ST = "MexicoCity"
    subj.L =  "MexicoCity"
    subj.O = "pulsarcloud"
    subj.OU = "pulsarcloud-cluster"
    subj.CN = "pulsarcloud-machine"
    
    # El emisor es el mismo que el solicitante
    cert.set_issuer(subj)
    cert.gmtime_adj_notBefore(0)
    # Validez por 10 anios
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_pubkey(key)
    cert.sign(key, 'md5')
    # Write con permisos
    # with open("certificate.cer", 'wb') as fh:
    with os.fdopen(os.open('certificate.cer', os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as fh:
        fh.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
    # with open("private_key.pem", 'wb') as fh:
    with os.fdopen(os.open('private_key.pem', os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as fh:
        fh.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))

    with os.fdopen(os.open('public_key.pub', os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as fh:
        fh.write(OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, key))

    # Generamos el
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)

    # with open("container.pfx", 'wb') as fh:
    with os.fdopen(os.open('container.pfx', os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as fh:
        fh.write(p12.export())
