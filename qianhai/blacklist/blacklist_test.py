#coding=utf-8
import urllib2,json,urllib
import base64,hashlib
from DesCrypter import DesCrypter
#from data_user import *
import time,datetime
import requests
import random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk
from Crypto.Hash import SHA
#db.generate_mapping(create_tables = True)

userName = 'V_PA025_QHCS_DCS'
userPassword = 'weblogic1'
key = 'SK803@!QLF-D25WEDA5E52DA'

privatekey=RSA.importKey(open('private.pem.key','r').read())
test_url = 'https://test-qhzx.pingan.com.cn:5443/do/dmz/query/blacklist/v1/MSC8004'

class TempUser(object):
      def __init__(self,id,status,code,name,id_card_num,phone,home_addr,work_addr):
          self.id = id
          self.status = status
          self.code = code
          self.name = name
          self.id_card_num = id_card_num
          self.phone = phone
          self.home_addr = home_addr
          self.work_addr = work_addr

class BlacklistCal(object):
      def __init__(self,file):
          f = open(file,"r")
          self.lines = f.readlines()
          f.close()
          self.user_list = []
          self.init_user()
          random.seed(time.time())
          self.batch_num = random.randint(10000,99999)
      def get_header(self):
          random.seed(time.time())
          transNo = random.randint(10000,99999)
          now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
          transDate = now
          authDate = now
          header = {
             "orgCode":"10000000",
             "chnlId":"qhcs-dcs",
             "transNo":"",
             "transDate":"",
             "authCode":"CRT001A2",
             "authDate":"",
          }
          header["transNo"] = transNo
          header["transDate"] = transDate
          header["authDate"] = authDate
          return header

      def get_sign(self,data):
          temp = []
          keys=data.keys()
          keys.sort()
          for v in keys:
              temp.append(str(data[v]))
          str1=''.join(temp)
          h=SHA.new(str1)
          signer = pk.new(privatekey)
          signn=signer.sign(h)
          signn=base64.b64encode(signn)
          return signn
          
      def make_security_info(self,sign):
          password = hashlib.sha1(userPassword).hexdigest()
          securityInfo = {
              "signatureValue":sign,
              "userName":userName,
              "userPassword":password,
          }
          return securityInfo
      #need to overwrite
      def make_data(self,user):  
          data = {
              "batchNo":self.batch_num,
              "idNo":user.id_card_num,
              "idType":'0',
              "reasonNo":'01',
              "name":user.name,
              "entityAuthCode":user.id,
              "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
              "seqNo":user.id
          }
          return data
              
      def init_user(self):
          for i in self.lines:
              s = len(i.split())
              if s == 6:
                  id,check_status,code,name,id_card_num,phone = i.split()
                  self.user_list.append(TempUser(str(id),str(check_status),str(code),str(name),str(id_card_num),str(phone),'',''))
              else:
                  list1 = i.split()[0:8]
                  id,check_status,code,name,id_card_num,phone,home_addr,work_addr = list1
                  self.user_list.append(TempUser(str(id),str(check_status),str(code),str(name),str(id_card_num),str(phone),str(home_addr),str(work_addr)))

      def get_response(self,url):
          a = open("result","w")
          for user in self.user_list:
              header = self.get_header()
              data = self.make_data(user)
              sign = self.get_sign(data)
              securityInfo = self.make_security_info(sign)
              d = DesCrypter()
              encrypt_data = d.encrypt_3des(json.dumps(data,ensure_ascii=False))
              json_data = {
                  "header":header,
                  "busiData":encrypt_data,
                  "securityInfo":securityInfo,
              }
              str_data = json.dumps(json_data,ensure_ascii=False)
              print str_data
              http_headers = {'content-type': 'application/json;charset=utf-8','content-length':len(str_data)}
              res = requests.post(url, data=str_data, headers=http_headers ,cert='credoo_ssl.crt',verify=True)
              res = d.decrypt_3des(res)
              a.write(user.id+' '+res+'\n')
              time.sleep(0.1)
              break
          a.close()

b = BlacklistCal("user_data")
print b.get_response(test_url)
'''
if __name__ == '__main__':
    data = {"app_id":app_key,"secret":secret,"idNumber":"511181199306050015","phone":"15608071193","name":"leon"}
    s = sorted(data.items(), key=lambda d:d[0])
    print s
    str1 = ''
    for i in s:
        str1+= i[0]+'='+i[1]
    str1 += md5_key
    m = hashlib.md5()
    m.update(str1)
    token = m.hexdigest()
    data.setdefault("token",token)
    str_data = json.dumps(data)
    print str_data
    aes = AesCrypter(secret)
    b64 = aes.encrypt(str_data)
    print b64
    #mode=AES.MODE_CBC
    #iv = 16 * '\x00'
    #encryptor=AES.new(secret)
    #padding = '\0'
    #pad_it = lambda s: s+(16 - len(s)%16)*padding
    #data2 = encryptor.encrypt(pad_it(str(str_data)))
    #print data2,type(data2)
    #b64 = base64.b64encode(data2)
    #print b64,"-----------------base64"
    res = json_http_post(url_1, b64)
    #res = 'AaOG8V7mLs08J7TmQ/xKqy3WhnLaG2dyH3PtnYzCUoE4oDsiWwBlgfXJn9Xeqh2YLzCvtCHM/DB3u7Zke+EiFpOryS67qDMRWV/cJjefXjAaQ+p7JfO6lbsP99UWta4iqNw74P2qO4ATSNaGvLoe3oPqt+9eOwADOuQDKwiJetc='
    print res,"-----------------response"
    #res = base64.b64decode(res)
    #decryptor = AES.new(secret,mode,iv)
    #r = decryptor.decrypt(res)
    #print r,'==================='
    #unpad = lambda s : s[0:-ord(s[-1])]
    #s = unpad(r)
    s = aes.decrypt(res)
    print s'''
