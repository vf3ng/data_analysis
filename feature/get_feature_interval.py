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
             limit 5000;
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
        result.append(a[index]+0.1)
    result.append(a[-1]+0.1)
    return result

#以进单用户均等来划分区间
def get_interval(table_name, feature, num, user_id = 'user_id'):
    data = get_compute_data(table_name, user_id)
    data = data[feature].replace(['',-1],np.nan).dropna()
    bins = get_average_interval(data,num)
    cut = pd.cut(data, bins, right = False)
    #cut = pd.qcut(data,num)
    print feature,':'
    print cut.value_counts(),'\n'

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
    #count_cut = pd.qcut(unused_count, num_count)
    #time_cut = pd.qcut(unused_time, num_time)
    count_bins = get_average_interval(unused_count, num_count)
    time_bins = get_average_interval(unused_time, num_time)
    count_cut = pd.cut(unused_count, count_bins, right =False)
    time_cut = pd.cut(unused_time, time_bins, right = False)
    print 'unused_count : '
    print count_cut.value_counts(),'\n'
    print 'unused_time : '
    print time_cut.value_counts(),'\n'

if __name__ == '__main__':

    
    #通话特征
    get_interval('userinfoformine','call_count',10)
    get_interval('userinfoformine','call_time',10)
    get_interval('userinfoformine','sustained_days',6)
    #平均日通话次数
    data = get_compute_data('userinfoformine', 'user_id')
    data = data[data['sustained_days']!=0]
    data['day_average_call_count'] = data['call_count']/data['sustained_days']
    data = data['day_average_call_count'].dropna()
    bins = get_average_interval(data, 10)
    cut = pd.cut(data, bins, right =False)
    print 'day_average_call_count : '
    print cut.value_counts(),'\n'
    #关机时长
    get_unused_time_interval(3,6)
    #电商特征
    get_interval('ebusiness_feature','total_order_count',6)
    get_interval('ebusiness_feature','total_price',10)
    get_interval('ebusiness_feature','used_days',10)
    get_interval('ebusiness_feature','price_per_day',10)
    #地址特征
    get_interval('getuiresult','home_offset',10,'owner_id')
    get_interval('getuiresult','work_offset',10,'owner_id')
    get_interval('baiducredit','home_distance',10,'owner_id')
    get_interval('baiducredit','company_distance',10,'owner_id')
    #多平台贷款特征
    get_interval('loginplatforms','phone_loan_platform_num',2,'owner_id')
    get_interval('loginplatforms','phone_loan_times',2,'owner_id')
    get_interval('loginplatforms','idcard_loan_platform_num',2,'owner_id')
    get_interval('loginplatforms','idcard_loan_times',2,'owner_id')
    conn.close()
