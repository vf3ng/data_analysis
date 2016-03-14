#coding=utf-8

import pandas as pd, numpy as np

class Data(object):
   
    def __init__(self, filename):
        self.name = filename
     
    def get_excel_data(self):
        data_deny = pd.read_excel(self.name, sheetname = u'拒绝用户')
        data_pass = pd.read_excel(self.name, sheetname = u'通过用户')
        return data_deny, data_pass

    #data_type = ['pass','deny'],  interval_value = [X,X,X,...]
    def data_process(self, data, indexname, interval = False, interval_value = None):
        if interval and interval_value:
            cut_interval = pd.cut(data[indexname], interval_value)
            result = pd.DataFrame(data.groupby(cut_interval).apply(len))
            result.to_excel('%s.xlsx'%indexname)
            print result
        elif interval == False:
            result = pd.DataFrame(data.groupby(indexname).apply(len))
            result.to_excel('%s.xlsx'%indexname)
            print result
        else:
            pass

if __name__ == '__main__':
    a = Data('银联智策测试数据（泰康金融）.xlsx')
    data_deny, data_pass = a.get_excel_data()
    index = data_deny.columns[5:]
    print index
    a.data_process(data_deny,u'套现模型得分',interval = True,interval_value = [0,200,400,600,800,1000])
    a.data_process(data_deny,u'卡状态得分表')
