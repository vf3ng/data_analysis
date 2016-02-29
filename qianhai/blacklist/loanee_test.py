#coding=utf-8
from blacklist_test import *
test_url = 'https://test-qhzx.pingan.com.cn:5443/do/dmz/query/loanee/v1/MSC8037'

class LoaneeCal(BlacklistCal):
      def make_data(self,user):  
          data = {
              "batchNo":self.batch_num,
              "records":[
                  {
                  "idNo":user.id_card_num,
                  "idType":'0',
                  "name":user.name,
                  "entityAuthCode":user.id,
                  "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
                  "seqNo":user.id,
                  "busiDesc":"11"
                  }
              ]
          }
          return data
              

if __name__ == '__main__':
    b = LoaneeCal("user_data")
    b.get_response(test_url,'loanee_result')
