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
        if self.name.split('_')[0]=='blacklist':
            result = pd.DataFrame([],index = [u'命中',u'误伤',u'单独'],columns = [u'个数',u'覆盖率'])
            data = self.get_merged_data()
            data['new'] = data[2].replace([str(i) for i in range(-11,-1)],99)
            result.ix[0][0] = len(data[data['dataStatus']==u'1'])
            result.ix[1][0] = len(data[(data['dataStatus']==u'1')&(data[1]=='3')])
            result.ix[2][0] = len(data[(data['dataStatus']==u'1')&(data['new']!=99)])
            result[u'覆盖率']=result[u'个数']/200.0
            print result

    def show_address(self):
        if self.name.split('_')[0]=='address':
            data = self.get_merged_data()
            data.columns = [str(i) for i in data.columns]
            data['newprice'] = data['houseArodAvgPrice'].replace(['',u'0.0'],99).map(float)
            newdata = data[data['newprice']!=99.0]
            #newdata['pricefield'] = pd.cut(newdata['newprice'],6)
            #temp = newdata.pivot_table('0',index = 'pricefield',columns = '1',margins=True,aggfunc=[len,max]) 
            temp = newdata.groupby([pd.cut(newdata['newprice'],6),'1'])
            result = temp.apply(len).unstack().fillna(0)
            result['a'] = result['3']+result['5']
            del result['3']
            result.columns = [u'命中',u'总数']
            result[u'命中率'] = result[u'命中']/result[u'总数']
            result.index.name = u'价格区间'
            result.to_excel('address.xlsx')
            print result

    def show_credoo(self):
        if self.name.split('_')[0]=='credoo':
            b = self.get_data()
            a = pd.read_table('user_new',header = None)
            data = pd.merge(a,b,left_on=3,right_on='idNo')
            data.columns = [str(i) for i in data.columns]
            data['newscore'] = data['credooScore'].replace([''],99).map(float)
            newdata = data[data['newscore']!=99.0]
            temp = newdata.groupby([pd.cut(newdata['newscore'],6),'5'])
            result = temp.apply(len).unstack().fillna(0)
            result['a'] = result[3]+result[5]
            del result[3]
            result.columns = [u'命中',u'总数']
            result[u'命中率'] = result[u'命中']/result[u'总数']
            result.index.name = u'分数区间'
            result.to_excel('credoo.xlsx')
            print result


    def show_loanee(self):
        if self.name.split('_')[0]=='loanee':
            data = self.get_merged_data()
            data['amount_new']=data['amount'].replace([unicode(i) for i in range(8,15)],'8次以上')
            data['amount_new']=data['amount_new'].replace(['','None'],u'0')
            data.columns = [str(i) for i in data.columns]
            temp = data.pivot_table('0', index = 'amount_new', columns = '1', aggfunc = len, margins = True)
            del temp['3']
            temp[u'比率'] = temp['5']/temp['All']
            temp.columns = [u'黑名单命中数',u'数量',u'比率']
            temp.index.name = u'申请次数取值'
            temp = temp.drop('All',axis = 0)
            temp.to_excel('amount.xlsx')
            print temp 

if __name__=='__main__':
    #data_blacklist = Data('blacklist_data_0')
    #data_blacklist.show_blacklist()
    #data_address = Data('address_data')
    #data_address.show_address()
    data_credoo = Data('credoo_data')
    data_credoo.show_credoo()
    #data_loanee = Data('loanee_data')
    #data_loanee.show_loanee()
