#coding=utf-8

import pandas as pd
import json

class Data(object):

    def __init__(self,file):
        self.data = []
        self.name = file
        f = open(file,'r')
        json_data = f.readlines()
        for line in json_data:
            value = json.loads(line)
            self.data.append(eval(value)['records'][0])
        f.close() 

    def get_data(self):
        data = pd.DataFrame(self.data)
        return data    
    
    def get_merged_data(self):
        prefix = self.name.split('_')[0]
        dataframe = self.get_data()
        data_basic = self.read('user_data')
        final_data = pd.merge(data_basic,dataframe,left_on=4,right_on='idNo')
        return final_data
        '''   
        try:
            sub_dataframe = dataframe[dataframe['dataStatus']!='']
            print dataframe
            pct = len(sub_dataframe)*1.0/len(dataframe)
            print "%d,%d"%(len(sub_dataframe),len(dataframe))
            print "%s : %.2f%%"%(prefix,pct*100)
        except:
            print "%s length:%d" %(prefix,len(self.data))
            print prefix,":",dataframe
        '''
    def read(self,file):
        temp_data = pd.read_table(file,header=None)
        data = pd.DataFrame(i.split(' ') for i in temp_data[0])
        return data

    def show_blacklist(self):
        result = pd.DataFrame([],index = [u'命中',u'误伤',u'单独'],columns = [u'个数',u'覆盖率'])
        data = self.get_merged_data()
        data['new'] = data[2].replace([str(i) for i in range(-11,-1)],99)
        result.ix[0][0] = len(data[data['dataStatus']==u'1'])
        result.ix[1][0] = len(data[(data['dataStatus']==u'1')&(data[1]=='3')])
        result.ix[2][0] = len(data[(data['dataStatus']==u'1')&(data['new']!=99)])
        result[u'覆盖率']=result[u'个数']/200.0
        print result

    def show_address(self):
        pass

    def show_credoo(self):
        pass

    def show_loanee(self):
        data = self.get_merged_data()
        data['amount_new']=data['amount'].replace([unicode(i) for i in range(8,15)],99)
        a = pd.DataFrame([],index=[u'%s次'%i for i in range(0,8)]+[u'8次以上'],columns=[u'数量',u'黑名单命中数',u'比率'])
        for i in range(0,8):
            temp = data[data['amount']==unicode(i)]
            if len(temp)!=0:
                a.ix[i][0] = len(temp)
                a.ix[i][1] = len(temp[temp[1]==u'5'])
        temp = data[data['amount_new']==99]
        a.ix[u'8次以上'][0] = len(temp)
        a.ix[u'8次以上'][1] = len(temp[temp[1]==u'5'])
        a[u'比率'] = a[u'黑名单命中数']*1.0/a[u'数量']
        a.to_csv('amount_test.csv',encoding = 'gb2312')
        print a 

if __name__=='__main__':
    #data_blacklist = Data('blacklist_data_0')
    #data_blacklist.show_blacklist()
    #data_address = Data('address_data')
    #data_address.show()
    #data_credoo = Data('credoo_data')
    #data_credoo.show()
    data_loanee = Data('loanee_data')
    data_loanee.show_loanee()
