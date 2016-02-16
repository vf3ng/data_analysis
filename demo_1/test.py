#coding=utf-8
import urllib2,json,urllib
from Crypto.Cipher import AES
import base64,hashlib
from AesCrypter import AesCrypter
from data_user import *
import time

#secret = 'cf3221f2a63c800a'
md5_key = '0415143ee7edbb4de5cbd1126a38e809'
#app_key='offline_test'
#url_1 = ['http://111.204.113.194:8094/websearch/blacklist']

secret = '7f5611fd3d559592'
app_key = 'taikang'
#url_1 = 'http://tianji.rong360.com/websearch/blacklist'
url_list = [
            #'http://111.204.113.194:8094/websearch/blacklist',
            'http://tianji.rong360.com/websearch/blacklist',
            'http://tianji.rong360.com/ZhongZhiCheng/blacklist',
            'http://tianji.rong360.com/Fahai/LoanBlacklist',
            'http://tianji.rong360.com/rong360/Blacklist',
            'http://tianji.rong360.com/huifa/LoanBlacklist',
            'http://tianji.rong360.com/agentb/blacklist'
           ]
db.generate_mapping(create_tables = True)
#def pkcs7unpadding(data):
#    lengt = len(data)
#    unpadding = ord(data[lengt - 1])
#    return data[0:lengt-unpadding]

def json_http_post(url, data, retry=3, timeout=200):
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            req = urllib2.Request(url=url, headers=headers)
            #打开url读取内容并返回结果
            para_dict = {}
            para_dict["app_id"] = app_key
            para_dict["data"] = data
            post_data = urllib.urlencode(para_dict)
            #print post_data,"********************************post_data"
            rsp = urllib2.urlopen(req,post_data)
            page = rsp.read()
            return page
class BlacklistCal(object):
      def __init__(self,file):
          f = open(file,"r")
          self.lines = f.readlines()
          f.close()
          self.user_dict = {}
          self.init_dict()
          self.total = len(self.user_dict)
          self.hit_count = 0
          self.temp_count = 0
          self.hit_only = 0
          self.temp_only = 0
          self.hit_good = 0
          self.temp_good = 0
          self.response = []
          self.hit_dict = {}
      def init_dict(self):
          for i in self.lines:
              id,check_status,code = i.split()
              self.user_dict.setdefault("hualahuala_"+id,[check_status,code])
      def count(self,res,key):
          try:
              json_data = json.loads(res)
              if json_data["status"]==200 and json_data["content"]:
                  self.temp_count += 1
                  if self.user_dict[key][0] == '3':
                      self.temp_good += 1
                  if self.user_dict[key][1] not in [str(-i) for i in range(2,11)]:
                      self.temp_only += 1

                  if not self.hit_dict.get(key):
                      self.hit_dict.setdefault(key,res)
                      self.hit_count+=1
                      if self.user_dict[key][0] == '3':
                          self.hit_good += 1
                      if self.user_dict[key][1] not in [str(-i) for i in range(2,11)]:
                          self.hit_only += 1
              
          except Exception,e:
              print e
      @db_session
      def get_response(self):
          a = open("result","w")
          for url in url_list:
              print url
              for key,val in self.user_dict.items():
                  user = DataUser.get(user_id=key)
                  data = {"app_id":app_key,"secret":secret,"idNumber":user.id_card_num.encode("utf-8"),"phone":user.phone_num.encode("utf-8"),"name":user.name.encode("utf-8")}
                  s = sorted(data.items(), key=lambda d:d[0])
                  str1=''
                  for i in s:
                      str1+= i[0]+'='+i[1]
                  str1 += md5_key
                  m = hashlib.md5()
                  m.update(str1)
                  token = m.hexdigest()
                  data.setdefault("token",token)
                  str_data = json.dumps(data)
                  aes = AesCrypter(secret)
                  b64 = aes.encrypt(str_data)
                  res = json_http_post(url, b64)
                  s = aes.decrypt(res)
                  self.count(s,key)
                  self.response.append(s)
                  a.write(key+' '+s+' '+ url+'\n')
                  time.sleep(0.5)
              print self.temp_good,self.temp_only,self.temp_count,url
              self.temp_good = 0
              self.temp_only = 0
              self.temp_count = 0
          print self.total,self.hit_good,self.hit_only,self.hit_count
          a.close()
          return self.hit_dict

b = BlacklistCal("b3")
print b.get_response()
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
