#coding=utf-8
from blacklist_test import *
test_url = 'https://qhzx-dcs.pingan.com.cn/do/dmz/query/loanee/v1/MSC8037'

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
              

      def make_data_many(self,user_list):
          data = {
              "batchNo":self.batch_num,
              "records":[]
          }
          for user in user_list:
              new_data = {
                  "idNo":user.id_card_num,
                  "idType":'0',
                  "name":user.name,
                  "entityAuthCode":user.id,
                  "entityAuthDate":datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S"),
                  "seqNo":user.id,
                  "busiDesc":"11"
              }
              data['records'].append(new_data)
          return data



if __name__ == '__main__':
    b = LoaneeCal("user_data")
    b.write_data(test_url,"blacklist_data_0")
