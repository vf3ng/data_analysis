# coding: utf-8
import hashlib
from Crypto.Cipher import AES
import base64

class AesCrypter(object):

    def __init__(self, key):
        #self.key = hashlib.sha256(key).digest()
        self.key = key
        self.iv = 16 * '\x00'

    def encrypt(self, data):
        data = self.pkcs7padding(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted)

    def decrypt(self, data):
        data = base64.b64decode(data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(data)
        decrypted = self.pkcs7unpadding(decrypted)
        return decrypted

    def pkcs7padding(self, data):
        bs = AES.block_size
        padding = bs - len(data) % bs
        padding_text = chr(padding) * padding
        return data + padding_text

    def pkcs7unpadding(self, data):
        lengt = len(data)
        unpadding = ord(data[lengt - 1])
        return data[0:lengt-unpadding]

if __name__ == '__main__':
    aes = AesCrypter('cf3221f2a63c800a')
    a=aes.encrypt('{"idNumber": "511181199209080013", "phone": "15650131975", "secret": "cf3221f2a63c800a", "app_id": "offline_test", "token": "9780631ed4a4981f445b67a4c05ecdf6"}')
    print a
    #print aes.decrypt("ckwXp0viGKmjzhQ0/ENv1KW1/kXumVimtypzFC7xbSaFGNANfTeu6AmG09aLIJguv4s+Tb7/baVlxUJBNCvBZvdX+K0z6d5oN+4CO5tUm2rv4k8rZkV/i2sGZ//0Ncp7yPQwwHXEW2mGzd7T7TcZT19yQPsDL5EXnrGLtCwThquq1+7o/tsKAT/hegf6noPV3OYK0U4XyWQsgU5YPwhJbw==")
