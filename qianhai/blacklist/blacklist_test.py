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
import ssl

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv3)
#db.generate_mapping(create_tables = True)

userName = 'V_PA025_QHCS_DCS'
userPassword = 'weblogic1'
key = 'SK803@!QLF-D25WEDA5E52DA'

privatekey=RSA.importKey(open('private.pem.key','r').read())
publickey=RSA.importKey(open('publickey','r').read())

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
          #temp = []
          #keys=data.keys()
          #keys.sort()
          #for v in keys:
          #    temp.append(str(data[v]))
          #str1=''.join(temp)
          h=SHA.new(data)
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
              "records":[
              {
                 "idNo":user.id_card_num,
                 "idType":'0',
                 "reasonCode":'01',
                 "name":user.name,
                 "entityAuthCode":user.id,
                 "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
                 "seqNo":user.id
              },
            ]
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

      def verify_sign(self,busi_data,sign):
          print publickey,privatekey
          signn=base64.b64decode(sign)
          h=SHA.new(busi_data)
          verifier = pk.new(publickey)
          if verifier.verify(SHA.new(busi_data), sign):
              print "verify data ok"
              return True
          else:
              print "verify data failed"
              return False

      def get_response(self,url,output):
          a = open(output,"w")
          s = requests.Session()
          for user in self.user_list:
              print user.id
              header = self.get_header()
              data = self.make_data(user)
              #sign = self.get_sign(data)
              #securityInfo = self.make_security_info(sign)
              d = DesCrypter()
              encrypt_data = d.encrypt_3des(json.dumps(data,ensure_ascii=False))
              print d.decrypt_3des(encrypt_data)
              sign = self.get_sign(encrypt_data)
              securityInfo = self.make_security_info(sign)
              json_data = {
                  "header":header,
                  "busiData":encrypt_data,
                  "securityInfo":securityInfo,
              }
              str_data = json.dumps(json_data,ensure_ascii=False)
              print str_data
              http_headers = {'content-type': 'application/json;charset=utf-8','content-length':len(str_data)}
              s.mount('https://',Ssl3HttpAdapter())
              res = s.post(url, data=str_data, headers=http_headers ,verify=False)
              print res.content,"____________________all"
              res_data = json.loads(res.content)
              res = d.decrypt_3des(res_data["busiData"])
              print self.verify_sign(res_data["busiData"],res_data["securityInfo"]["signatureValue"])
              print res
              a.write(user.id+' '+res+'\n')
              #time.sleep(0.1)
              break
          a.close()

if __name__ == '__main__':
    b = BlacklistCal("user_data")
    b.get_response(test_url,"result1")
