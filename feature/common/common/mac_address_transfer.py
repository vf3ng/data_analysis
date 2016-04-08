#encoding=utf-8
import hashlib

def mac2int(mac):
    mac = mac.replace(':', '')
    try:
        return int(mac, 16)
    except:
        return abs(hash(mac))

def int2mac(imac):
    mac = hex(imac)
    mac = mac.replace('0x', '')
    mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
    return mac

if __name__ == '__main__':
    imac = mac2int('64:76:ba:8b:9c:4e')
    print imac
    mac = int2mac(imac)
    print mac

