#!/usr/bin/env python3
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
    # encrypt file by pub
    data = b'hello world!'
    print('origin \n', data)
    pub_key = RSA.importKey(
        externKey=pub.decode('utf-8'), passphrase=passphrase
    )
    encrypt_data = pub_key.encrypt(plaintext=data, K=Random.new())[0]
    # decrypt file by pri
    print('encrypt \n', encrypt_data)
    pri_key = RSA.importKey(
        externKey=pri.decode('utf-8'), passphrase=passphrase
    )
    data = pri_key.decrypt(ciphertext=encrypt_data)
    print('decrypt \n', data)


def example_2():
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA
    from Crypto import Random
    data = b'hello world!\n'
    print('origin \n', data)
    with open('test/data', 'wb') as f: f.write(data)
    h = SHA.new(data)
    # generate random RSA key
    passphrase = None
    key = RSA.generate(bits=2048)
    pri = key.exportKey()
    with open('test/pri.key', 'wb') as f: f.write(pri)
    pub = key.publickey().exportKey()
    with open('test/pub.key', 'wb') as f: f.write(pub)
    # encrypt file by pub
    pub_key = RSA.importKey(pub.decode('utf-8'))
    cipher = PKCS1_v1_5.new(pub_key)
    ciphertext = cipher.encrypt(data + h.digest())
    print('encrypt \n', ciphertext)
    with open('test/data.1', 'wb') as f: f.write(ciphertext)
    # decrypt
    pri_key = RSA.importKey(pri.decode('utf-8'))
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(pri_key)
    data = cipher.decrypt(ciphertext, sentinel)
    print('after decrypt \n', data)
    digest = SHA.new(data[:-dsize]).digest()
    print('method \n', data[:-dsize])
    

if __name__ == '__main__':
    # example()
    example_2()
