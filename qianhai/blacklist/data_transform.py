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
    
    def show(self):
        prefix = self.name.split('_')[0]
        try:
            dataframe = self.get_data()
            sub_dataframe = dataframe[dataframe['dataStatus']!='']
            pct = len(sub_dataframe)*1.0/len(dataframe)
            print "%d,%d"%(len(sub_dataframe),len(dataframe))
            print "%s : %.2f%%"%(prefix,pct*100)
        except:
            print "%s length:%d" %(prefix,len(self.data))


if __name__=='__main__':
    data_blacklist = Data('blacklist_data_0')
    data_blacklist.show()
    data_address = Data('address_data')
    data_address.show()
    data_credoo = Data('credoo_data')
    data_credoo.show()
    data_loanee = Data('loanee_data')
    data_loanee.show()
