#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-10 09:19:06
Author  : hnawei (potaski@qq.com)
Describe: File Encrypt & Decrypt
Version : 1.0.0
-------------------- End --------------------
"""


def example():
    """ official document
    https://www.dlitz.net/software/pycrypto/api/2.6/
    """
    from Crypto.PublicKey import RSA
    from Crypto import Random
    # generate random RSA key
    passphrase = None
    key = RSA.generate(bits=4096)
    pri = key.exportKey(passphrase=passphrase, pkcs=8)
    pub = key.publickey().exportKey()
    with open('id_rsa', 'wb') as f:
        f.write(pri)
    with open('id_rsa.pub', 'wb') as f:
        f.write(pub)
    # encrypt file by pub
    data = open('data_file', 'rb').read()
    pub_key = RSA.importKey(
        externKey=open('id_rsa.pub').read(), passphrase=passphrase
    )
    encrypt_data = pub_key.encrypt(plaintext=data, K=Random.new())[0]
    with open('data_file.encrypt', 'wb') as f:
        f.write(encrypt_data)
    # decrypt file by pri
    pri_key = RSA.importKey(
        externKey=open('id_rsa').read(), passphrase=passphrase
    )
    encrypt_data = open('data_file.encrypt', 'rb').read()
    data = pri_key.decrypt(ciphertext=encrypt_data)
    with open('data_file.decrypt', 'wb') as f:
        f.write(data)
