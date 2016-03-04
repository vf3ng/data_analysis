#coding=utf-8
test_url = 'https://qhzx-dcs.pingan.com.cn/do/dmz/query/credoo/v1/MSC8005'

from blacklist_test import *

class CredooCal(BlacklistCal):
      def make_data(self,user):  
          data = {
              "batchNo":self.batch_num,
              "records":[
                  {
                  "idNo":user.id_card_num,
                  "idType":'0',
                  "reasonNo":'01',
                  "name":user.name,
                  "entityAuthCode":user.id,
                  "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
                  "seqNo":user.id,
	              "mobileNo":'1358629551',
	              "cardNo":'111111222222',
	              "email":'421833098@qq.com',
	              "weiboNo":'421222833@qq.com',
	              "qqNo":'421833098',
	              "weixinNo":'412933098',
	              "taobaoNo":'123123123',
	              "jdNo":'42183330',
	              "amazonNo":'asdasd',
	              "yhdNo":'asdasd'
                  }
              ]
          }
          return data


      def make_data_many(self,user_list):
          data = {
              "batchNo":self.batch_num,
              "records":[]
          }
          for user in user_list:
              new_data ={
                  "idNo":user.id_card_num,
                  "idType":'0',
                  "reasonNo":'01',
                  "name":user.name,
                  "entityAuthCode":user.id,
                  "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
                  "seqNo":user.id,
                  "mobileNo":'1358629551',
                  "cardNo":'111111222222',
                  "email":'421833098@qq.com',
                  "weiboNo":'421222833@qq.com',
                  "qqNo":'421833098',
                  "weixinNo":'412933098',
                  "taobaoNo":'123123123',
                  "jdNo":'42183330',
                  "amazonNo":'asdasd',
                  "yhdNo":'asdasd'
              }
              data['records'].append(new_data)
          return data
              

if __name__ == '__main__':
    b = CredooCal("user_data")
    b.write_data(test_url,"blacklist_data_0")
