#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
-------------------- Copyright --------------------
Date    : 2018-12-17 10:27:25
Author  : zhangwei (potaski@qq.com)
Describe: File Encrypt&Decrypt Base on Packeage: pycryptodome
Link1   : https://pycryptodome.readthedocs.io/
Detail  : python3.6.5 & pycryptodome3.7.0
-------------------- End --------------------
"""


def aes_eax_only():
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    data = b'Hello World!'
    key = get_random_bytes(16)
    header = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    cipher.update(header)
    encrypt, tag = cipher.encrypt_and_digest(data)
    with open('encrypt.bin', 'wb') as f:
        [f.write(x) for x in (cipher.nonce, header, key, tag, encrypt)]
    # decrypt
    bytes_split = (16, 16, 16, 16, -1)
    with open('encrypt.bin', 'rb') as f:
        nonce, header, key, tag, encrypt = [f.read(x) for x in bytes_split]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    cipher.update(header)
    plaintext = cipher.decrypt_and_verify(encrypt, tag)
    print(plaintext)  # == data


def rsa_only():
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
    # gen keys
    key = RSA.generate(2048)
    with open('my.pri', 'wb') as f:
        f.write(key.export_key())
    with open('my.pub', 'wb') as f:
        f.write(key.publickey().export_key())
    # encrypt by pub
    data = b'1111111111111111'
    pub = RSA.importKey(open('my.pub').read())
    cipher = PKCS1_OAEP.new(pub)
    ciphertext = cipher.encrypt(data)
    print(ciphertext)
    # decrypt by pri
    pri = RSA.importKey(open('my.pri').read())
    cipher = PKCS1_OAEP.new(pri)
    ciphertext = cipher.decrypt(ciphertext)
    print(ciphertext)  # == data


def aes_eax_with_rsa():
    """ AES/RSA混合加密
    AES加密数据本身(MODE_EAX)
    RSA加密AES密钥
    """
    from Crypto.Cipher import AES, PKCS1_OAEP
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
    data = b'Hello World!!!'
    # gen rsa key
    key = RSA.generate(2048)
    with open('my.pri', 'wb') as f:
        f.write(key.export_key())
    with open('my.pub', 'wb') as f:
        f.write(key.publickey().export_key())
    # gen aes key and encrypt by rsa(pub)
    key = get_random_bytes(24)
    pub = RSA.importKey(open('my.pub').read())
    rsa_cipher = PKCS1_OAEP.new(pub)
    encrypt_key = rsa_cipher.encrypt(key)
    header = get_random_bytes(16)
    aes_cipher = AES.new(key, AES.MODE_EAX)
    aes_cipher.update(header)
    encrypt_data, tag = aes_cipher.encrypt_and_digest(data)
    write_order = (aes_cipher.nonce, header, encrypt_key, tag, encrypt_data)
    with open('encrypt.bin', 'wb') as f:
        [f.write(x) for x in write_order]
    # decrypt
    read_order = (16, 16, 256, 16, -1)
    with open('encrypt.bin', 'rb') as f:
        nonce, header, key, tag, data = [f.read(x) for x in read_order]
    # decrypt aes key
    pri = RSA.importKey(open('my.pri').read())
    rsa_cipher = PKCS1_OAEP.new(pri)
    key = rsa_cipher.decrypt(key)
    aes_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    aes_cipher.update(header)
    data = aes_cipher.decrypt_and_verify(data, tag)
    print(data)  # == data


if __name__ == "__main__":
    aes_mode_eax()