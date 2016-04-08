#encoding=utf-8
import hashlib
import time
import os

def gen_session(nbytes):
    return ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(nbytes)))

if __name__ == '__main__':
    print gen_md5_with_time('test')
