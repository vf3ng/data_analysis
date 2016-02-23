# coding: utf-8
from M2Crypto.EVP import Cipher
import base64


class DesCrypter(object):
    def __init__(self, key):
        self.key = key
        self.iv = 16 * '\x00'

    def encrypt_3des(key, text):
        encryptor = Cipher(alg='des_ede3_ecb', key=key, op=1, iv='\0'*16)
        s = encryptor.update(text)
        return s+ encryptor.final()

    def decrypt_3des(key, text):
        decryptor = Cipher(alg='des_ede3_ecb', key=key, op=0, iv='\0'*16)
        s= decryptor.update(text)
        return s + decryptor.final()

