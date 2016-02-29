#coding=utf-8
test_url = 'https://test-qhzx.pingan.com.cn:5443/do/dmz/query/credoo/v1/MSC8005'

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
              

if __name__ == '__main__':
    b = CredooCal("user_data")
    b.get_response(test_url,'credoo_result')
