# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import MySQLdb
from datetime import datetime

DB_HOST = 'rdsv0r421oul5inr17f5.mysql.rds.aliyuncs.com'
DB_USER = 'tk_yufa'
DB_PASSWORD = 'tkyufa'
DB_NAME = 'data_online'

conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset='utf8')


def get_sql_data(sql, conn):
    dataframe = pd.read_sql(sql, conn)

    return dataframe

def get_compute_data(table_name, user_id):
    sql = '''
             select * from %s as t1
             join (select %s,max(version) as max_version
                   from %s 
                   group by %s) as t2
             on t1.%s = t2.%s and t1.version = t2.max_version
             limit 5000,30000;
          ''' %(table_name, user_id, table_name, user_id, user_id, user_id)
    data = get_sql_data(sql, conn)
    
    return data

#定义数据切割函数(以数量均匀切割)
def get_average_interval(series, cut_num):
    a = list(series)
    a.sort()
    num = len(a)//cut_num
    result = [a[0]]
    index = 0
    for i in range(cut_num-1):
        index += num
        result.append(a[index])
    result.append(a[-1]+1)
    result = [(i//100+1)*100 if i >= 1000 else i for i in result]
    return result

#以进单用户均等来划分区间
def get_interval(table_name, feature, num = 2, user_id = 'user_id',bins = None):
    data = get_compute_data(table_name, user_id)
    data = data[feature].replace(['',-1],np.nan).dropna()
    if bins == None:
        bins = get_average_interval(data,num)
    cut = pd.cut(data, bins, right = False).replace(np.nan, '[%s, inf)'%bins[-1])
    result = cut.value_counts()
    #cut = pd.qcut(data,num)
    print feature,':'
    print result[my_sort_index(result)],'\n'

def get_unused_time_interval(num_count, num_time):
    data = get_compute_data('blacklist', 'user_id')
    data = data['unused_time'].replace('',np.nan).dropna()
    temp = [i.split('/') for i in data]
    unused_count = [len(i) for i in temp]
    a = []
    for i in temp:
        if len(i[0])==70:
            a.append([i[0][-41:]]+i[1:])
        else:
            a.append([i[0][-23:]]+i[1:])

    unused_time = []
    for i in a:
        max_time = 0
        for j in i:
            if len(j)==23:
                time = (datetime.strptime(j[-10:],'%Y-%m-%d')-datetime.strptime(j[0:10],'%Y-%m-%d')).days
                if time > max_time:
                    max_time = time
            else:
                time = (datetime.strptime(j[-19:],'%Y-%m-%d %H:%M:%S')-datetime.strptime(j[0:19],'%Y-%m-%d %H:%M:%S')).days
                if time > max_time:
                    max_time = time
        unused_time.append(max_time)
    #count_bins = get_average_interval(unused_count, num_count)
    #time_bins = get_average_interval(unused_time, num_time)
    count_bins = range(0,13,2)
    count_cut = pd.Series(pd.cut(unused_count, count_bins, right = False)).replace(np.nan, '[%s, inf)'%count_bins[-1])
    time_bins = range(0,57,7)+[400]
    time_cut = pd.Series(pd.cut(unused_time, time_bins, right = False)).replace(np.nan, '[%s, inf)'%time_bins[-1])
    result_count = count_cut.value_counts()
    result_time = time_cut.value_counts()
    print 'unused_count : '
    print result_count[my_sort_index(result_count)],'\n'
    #count_cut = pd.qcut(unused_count, num_count)
    print 'unused_time : '
    print result_time[my_sort_index(result_time)],'\n'

def my_sort_index(series):
    return sorted(series.index, key = lambda x: int(x.split(',')[0][1:]))

if __name__ == '__main__':

    #通话特征
    get_interval('userinfoformine', 'call_count', bins = range(0,6501,500))
    get_interval('userinfoformine', 'call_time', bins = range(0,420001,30000))
    get_interval('userinfoformine', 'sustained_days', bins = range(0,241,30))
    #平均日通话次数
    data = get_compute_data('userinfoformine', 'user_id')
    data = data[data['sustained_days']!=0]
    data['day_average_call_count'] = data['call_count']/data['sustained_days']
    data = data['day_average_call_count'].dropna()
    #bins = get_average_interval(data, 10)
    bins = range(0,49,6)
    cut = pd.cut(data, bins, right =False).replace(np.nan, '[%s, inf)'%bins[-1])
    result = cut.value_counts()
    print 'day_average_call_count : '
    print result[my_sort_index(result)],'\n'
    #关机时长
    get_unused_time_interval(2,5)
    #电商特征
    get_interval('ebusiness_feature','total_order_count',bins = range(0,481,60))
    get_interval('ebusiness_feature','total_price',bins = range(0,36001,3000))
    get_interval('ebusiness_feature','used_days',bins = range(0,2601,200))
    get_interval('ebusiness_feature','price_per_day',bins = range(0,81,8))
    #地址特征
    get_interval('getuiresult','home_offset',user_id = 'owner_id',bins = range(0,130001,10000))
    get_interval('getuiresult','work_offset',user_id = 'owner_id',bins = range(0,130001,10000))
    get_interval('baiducredit','home_distance',user_id = 'owner_id',bins = range(0,72001,6000))
    get_interval('baiducredit','company_distance',user_id = 'owner_id',bins = range(0,72001,6000))
    #多平台贷款特征
    get_interval('loginplatforms','phone_loan_platform_num',user_id = 'owner_id',bins = range(0,31,3))
    get_interval('loginplatforms','phone_loan_times',user_id = 'owner_id',bins = range(0,101,10))
    get_interval('loginplatforms','idcard_loan_platform_num',user_id = 'owner_id',bins = range(0,31,3))
    get_interval('loginplatforms','idcard_loan_times',user_id = 'owner_id',bins = range(0,101,10))
    
    conn.close()
