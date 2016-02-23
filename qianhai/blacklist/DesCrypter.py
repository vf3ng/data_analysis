# coding: utf-8
from M2Crypto.EVP import Cipher
import base64

key = 'SK803@!QLF-D25WEDA5E52DA'

class DesCrypter(object):
    def __init__(self):
        self.key = key
        self.iv = 16 * '\x00'

    def encrypt_3des(self,text):
        encryptor = Cipher(alg='des_ede3_ecb', key=self.key, op=1, iv=self.iv)
        s = encryptor.update(text)
        return base64.b64encode(s+ encryptor.final())

    def decrypt_3des(self,text):
        data = base64.b64decode(text)
        decryptor = Cipher(alg='des_ede3_ecb', key=key, op=0, iv=self.iv)
        s= decryptor.update(data)
        return s + decryptor.final()

if __name__ == "__main__":
    d = DesCrypter()
    text = 'value'
    encrypt_text =d.encrypt_3des(text)
    print encrypt_text
    print  d.decrypt_3des(encrypt_text)
    

