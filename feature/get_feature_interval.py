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
             limit 5000,5000;
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
    cut = pd.cut(data, bins, right = False)
    #cut = pd.qcut(data,num)
    print feature,':'
    print cut.value_counts().sort_index(),'\n'

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
    get_interval('userinfoformine','call_count',bins = [0,370,690,980,1300,1600,2000,2500,3100,4200,60000])
    get_interval('userinfoformine','call_time',bins = [0,33400,59400,82700,106600,135100,168400,208300,260200,363200,7522700])
    get_interval('userinfoformine','sustained_days',4)
    #平均日通话次数
    data = get_compute_data('userinfoformine', 'user_id')
    data = data[data['sustained_days']!=0]
    data['day_average_call_count'] = data['call_count']/data['sustained_days']
    data = data['day_average_call_count'].dropna()
    #bins = get_average_interval(data, 10)
    cut = pd.cut(data, [0,3,4,6,7,9,11,14,18,25,500], right =False)
    print 'day_average_call_count : '
    print cut.value_counts().sort_index(),'\n'
    #关机时长
    get_unused_time_interval(2,5)
    #电商特征
    get_interval('ebusiness_feature','total_order_count',6)
    get_interval('ebusiness_feature','total_price',bins = [0,70,415,1200,2300,4000,6300,9600,14900,27800,664000])
    get_interval('ebusiness_feature','used_days',bins = [0,35,105,190,300,410,550,690,980,1500,3600])
    get_interval('ebusiness_feature','price_per_day',bins = [0,1,3,5,7,9,13,18,25,43,1700])
    #地址特征
    get_interval('getuiresult','home_offset',user_id = 'owner_id',bins = [0,140,300,660,1600,3500,7200,16400,58200,315000,4000000])
    get_interval('getuiresult','work_offset',user_id = 'owner_id',bins = [0,230,780,1700,3300,5200,8200,14600,38100,269600,4000000])
    get_interval('baiducredit','home_distance',user_id = 'owner_id',bins = [0,230,780,1800,3700,7100,10900,18000,35000,360000,3100000])
    get_interval('baiducredit','company_distance',user_id = 'owner_id',bins = [0,410,1200,2500,4500,7300,11000,17800,38500,410000,3300000])
    #多平台贷款特征
    get_interval('loginplatforms','phone_loan_platform_num',2,'owner_id')
    get_interval('loginplatforms','phone_loan_times',2,'owner_id')
    get_interval('loginplatforms','idcard_loan_platform_num',2,'owner_id')
    get_interval('loginplatforms','idcard_loan_times',2,'owner_id')
    
    conn.close()
