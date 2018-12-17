#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-10 09:19:06
Author  : hnawei (potaski@qq.com)
Describe: File Encrypt & Decrypt Base On Package: pycrypto
Link    : https://www.dlitz.net/software/pycrypto/api/2.6/
Detail  : python3.6.5 & pycrypto2.6
-------------------- End --------------------
"""


def example_rsa_defautl():
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


def example_rsa_pkcs1_5():
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


def aes_only(filename):
    from Crypto.Cipher import AES
    from Crypto import Random
    from random import choice
    import string
    # system setting
    spec_chars = '!@#$%^&*()'
    allow_chars = string.ascii_letters + string.digits*3 + spec_chars*2
    # user setting
    key_length = 16  # 16, 24 or 32
    password = ''.join([choice(allow_chars) for i in range(key_length)])
    password = password.encode('utf-8')
    print(password, len(password))
    # encrypt file with aes
    data = open(filename, 'rb').read()
    print('origin \n', data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(password, AES.MODE_CFB, iv)
    encrypt_data = iv + cipher.encrypt(data)
    print('encrypt \n', encrypt_data[0:20])
    with open('encrypt_' + filename, 'wb') as f:
        f.write(encrypt_data)
    # decrypt file with aes
    cipher = AES.new(password, AES.MODE_CFB, Random.new().read(AES.block_size))
    decrypt_data = cipher.decrypt(encrypt_data)
    print('decrypt \n', decrypt_data)
    with open('decrypt_' + filename, 'wb') as f:
        f.write(decrypt_data[16:])
    print('origin \n', decrypt_data[16:])


def aes_and_rsa(filename):
    """ aes/rsa 混合加密
    """
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES
    from Crypto import Random
    # gen password start
    from random import choice
    import string
    spec_chars = '!@#$%^&*()'
    allow_chars = string.ascii_letters + string.digits*3 + spec_chars*2
    key_length = 32  # 16, 24 or 32
    password = ''.join([choice(allow_chars) for i in range(key_length)])
    password = password.encode('utf-8')
    # gen password end
    # gen random 32bit key from Random object or Custom String
    passwd = Random.new().read(32)
    passwd = password
    # print('passwd \n', passwd)
    # (rsa) encrypt passwd by public key, encrypt key length 256bit
    pub_cipher = RSA.importKey(open('zhang-w6.pub.pem').read())
    encrypt_key = pub_cipher.encrypt(plaintext=passwd, K=Random.new())[0]
    # (aes) encrypt data by passwd
    data = open(filename, 'rb').read()
    iv = Random.new().read(16)
    aes_cipher = AES.new(passwd, AES.MODE_CFB, iv)
    encrypt_data = encrypt_key + iv + aes_cipher.encrypt(data)
    with open('encrypt_' + filename, 'wb') as f:
        f.write(encrypt_data)
    # (aes) decrypt passwd by private key
    encrypt_key = encrypt_data[:256]
    pri_cipher = RSA.importKey(open('zhang-w6.pem').read())
    decrypt_passwd = pri_cipher.decrypt(ciphertext=encrypt_key)
    # print('passwd \n', decrypt_passwd)
    iv = Random.new().read(16)
    aes_cipher = AES.new(decrypt_passwd, AES.MODE_CFB, iv)
    decrypt_data = aes_cipher.decrypt(encrypt_data[256:])
    # print('decrypt data \n', decrypt_data[16:])
    with open('decrypt_' + filename, 'wb') as f:
        f.write(decrypt_data[16:])
    

if __name__ == '__main__':
    # example()
    aes_and_rsa('data.txt')
