#-*- coding: utf-8 -*-

import math
import time

import pandas as pd
import numpy as np
import MySQLdb
from datetime import datetime, timedelta

from common import tk_log_client


#用来执行插入或者更新的标识   
insert_or_not = 0
update_or_not = 0

date = datetime.now().strftime('%Y-%m-%d')
date_time_start = datetime.now().strftime('%Y-%m-%d 00:00:00')
date_time_end = (datetime.now()+timedelta(1)).strftime('%Y-%m-%d 00:00:00')

DB_HOST = 'rdsv0r421oul5inr17f5.mysql.rds.aliyuncs.com'
DB_USER = 'tk_yufa'
DB_PASSWORD = 'tkyufa'
DB_NAME1 = 'tk_yufa'
DB_NAME2 = 'data_online'

sql_apply_id = '''
                select distinct create_by_id from apply
                where create_at >= '%s' and create_at < '%s' and status != 'e'
                '''%(date_time_start, date_time_end)
                #%('2015-11-11 00:00:00','2015-11-12 00:00:00')

sql_apply_pass_id = '''
                select distinct create_by_id from apply
                where create_at >= '%s' and create_at < '%s' and (status = 'a' or status = 'y')
                    '''%(date_time_start, date_time_end)
                #%('2015-11-11 00:00:00','2015-11-12 00:00:00')

sql_m0_id = '''
            select distinct create_by_id from apply
            where type = 'a' and status != '8'
            '''

sql_m1_id = '''
            select distinct create_by_id from apply
            where type = 'b' and status != '8'
            '''

sql_m2_id = '''
            select distinct create_by_id from apply
            where type = 'c' and status != '8'
            '''

sql_m3_id = '''
            select distinct create_by_id from apply
            where type = 'd' and status != '8'
            '''

sql_m4_id = '''
            select distinct create_by_id from apply
            where type = 'e' and status != '8'
            '''

#计算逾期IV值的语句
sql_apply_pass_id_iv = '''
                        select distinct create_by_id from apply
                        where create_at >= '%s' and create_at < '%s' and (status = 'a' or status = 'y')
                       '''%('2015-11-01 00:00:00', '2015-11-30 00:00:00')

sql_apply_deny_id_iv = '''
                        select distinct create_by_id from apply
                        where create_at >= '%s' and create_at < '%s' and status != 'e' and create_by_id not in (%s)
                       '''%('2015-11-01 00:00:00', '2015-11-30 00:00:00', sql_apply_pass_id)

sql_not_m_id_iv = '''
                  select distinct user_id from repaymentinfo
                  where user_id not in
                  (select distinct create_by_id from apply
                  where type in ('a','b','c','d','e'))
                  '''

sql_m_id_iv = '''
               select distinct create_by_id from apply
               where type in ('a','b','c','d','e')
              '''


sql_list = [(sql_apply_id, 'apply'),(sql_apply_pass_id,'apply_pass'),(sql_m0_id,'m0'),(sql_m1_id,'m1'),(sql_m2_id,'m2'),(sql_m3_id,'m3'),(sql_m4_id,'m4')]

IV_sql_list = [(sql_apply_pass_id_iv, sql_apply_deny_id_iv, 'pass_deny'),(sql_not_m_id_iv, sql_m_id_iv, 'm_not_m')]


class DBoperator(object):

    def __init__(self, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
        self.conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset='utf8')
        self.cur = self.conn.cursor()

    #tk_yufa使用
    def get_id_list(self, sql):
        num = self.cur.execute(sql) #获取数据的条数（长整型）
        data = self.cur.fetchmany(num)
        return ['hualahuala_'+str(i[0]) for i in data]

    def get_max_version_data(self, id_list, table_name, feature_name, user_id):
        if isinstance(feature_name, list):
            feature_name = ','.join(feature_name)
        if len(id_list) == 0:
            ids = "('nothing')"
        else:
            ids = str(tuple(id_list))
        sql_version ='''
            select %s from %s as t1 
            join (select %s, max(version) as max_version 
            from %s where %s in %s group by %s) as t2 
            on t1.%s = t2.%s and t1.version = t2.max_version;
                     ''' %(feature_name, table_name, user_id, table_name, user_id, ids, user_id, user_id, user_id)

        num = self.cur.execute(sql_version)
        data = self.cur.fetchmany(num)
        array = np.array(data).T 
        return array  #此处为二维数组（通常为1*n）
        
    def get_common_feature(self, date, id_list, data_type, table_name, feature_name, bins, user_id = 'user_id'):
        array = self.get_max_version_data(id_list, table_name, feature_name, user_id)
        if len(array) != 0:
            array = array[0]
            array = array[array != -1]
            cut = pd.cut(array, bins, right = False)
            cut = ['[%s, inf)'%bins[-1] if i!=i else i for i in cut] 
            #cut = np.array(pd.cut(array, bins, right = False))
            #cut[np.array([i != i for i  in cut])] = '[%s, inf)'%bins[-1]
        else:
            cut = pd.cut(array, bins, right = False)
        result = pd.value_counts(cut)
        new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]
        final_result = result.reindex(new_index).fillna(0)
        #print feature_name,'  ',data_type,':'
        #print final_result,'\n'
        return (date, feature_name, data_type, final_result)

    def get_unused_time_feature(self, date, id_list, data_type, count_bins, time_bins):
        array = self.get_max_version_data(id_list, 'blacklist', 'unused_time', 'user_id')
        if len(array) != 0:
            array = array[0]
            array = array[array != u'']
            temp = [i.split('/') for i in array]
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
            count_cut = pd.cut(unused_count, count_bins, right = False)
            count_cut = ['[%s, inf)'%count_bins[-1] if i!=i else i for i in count_cut]
            time_cut = pd.cut(unused_count, time_bins, right = False)
            time_cut = ['[%s, inf)'%time_bins[-1] if i!=i else i for i in time_cut]
            #count_cut = np.array(pd.cut(unused_count, count_bins, right = False))
            #count_cut[np.array([i != i for i in count_cut])] = '[%s, inf)'%count_bins[-1]
            #time_cut = np.array(pd.cut(unused_time, time_bins, right = False))
            #time_cut[np.array([i != i for i in time_cut])] = '[%s, inf)'%time_bins[-1]
        else:
            count_cut = pd.cut(array, count_bins, right = False)
            time_cut = pd.cut(array, time_bins, right = False)

        result_count = pd.value_counts(count_cut)
        result_time = pd.value_counts(time_cut)
        new_count_index = ['[%s, %s)'%(count_bins[i],count_bins[i+1]) if i!=len(count_bins)-1 else '[%s, inf)'%count_bins[i] for i in range(len(count_bins))]
        final_result_count = result_count.reindex(new_count_index).fillna(0)
        new_time_index = ['[%s, %s)'%(time_bins[i],time_bins[i+1]) if i!=len(time_bins)-1 else '[%s, inf)'%time_bins[i] for i in range(len(time_bins))]
        final_result_time = result_time.reindex(new_time_index).fillna(0)
        #print 'unused_count    %s : '%data_type
        #print final_result_count,'\n'
        #print 'unused_time    %s : '%data_type
        #print final_result_time,'\n'
        return [(date, 'unused_count', data_type, final_result_count), (date, 'unused_time', data_type, final_result_time)]


    def get_day_average_call_count_feature(self, date, id_list, data_type, bins):
        array = self.get_max_version_data(id_list, 'userinfoformine', ['call_count', 'sustained_days'], 'user_id') #此处为2*n的数组
        if len(array) != 0:
            new_array = array.T[array[1] != 0].astype(np.float).copy('F')
            result_array = new_array[:,0]/new_array[:,1]
            cut = np.array(pd.cut(result_array, bins, right =False))
            cut[np.array([i!=i for i in cut])] = '[%s, inf)'%bins[-1]
        else:
            cut = pd.cut(array, bins, right = False)
        result = pd.value_counts(cut)
        new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]
        final_result = result.reindex(new_index).fillna(0)
        #final_result = result[sorted(result.index, key = lambda x: int(x.split(',')[0][1:]))]
        #print 'day_average_call_count    %s : '%data_type
        #print final_result,'\n'
        return (date, 'day_average_call_count', data_type, final_result)

    def insert_into_table(self, feature_data):
        for i in range(len(feature_data[3])):
            self.cur.execute('insert into day_interval_feature values(%s,%s,%s,%s,%s)',(feature_data[0],feature_data[1],feature_data[2],feature_data[3].index[i],feature_data[3][i]))

    def compute_IV(self, feature_name, relation_type, series_1, series_0):
        total_1 = series_1.sum()
        total_0 = series_0.sum()
        IV = 0
        sign = 0
        for i in range(len(series_1)):
            if series_1[i] == 0 or series_0[i] == 0:
                continue
            IV = (series_1[i]*1.0/total_1-series_0[i]*1.0/total_0)*math.log((series_1[i]*1.0/total_1)/(series_0[i]*1.0/total_0)) + IV
            sign = 1
        if sign == 0:
            IV = 9.9
        global insert_or_not, update_or_not
        if insert_or_not == 1: 
            self.cur.execute('insert into feature_iv values(%s,%s,%s)',(feature_name, relation_type, IV))
        else:
            if update_or_not == 1:
                self.cur.execute('update feature_iv set iv = %s where feature_name = %s and relation_type = %s',(IV, feature_name, relation_type))
            else:
                if self.cur.execute('select * from feature_iv where feature_name = %s and relation_type = %s',(feature_name, relation_type)) == 0:
                    self.cur.execute('insert into feature_iv values(%s,%s,%s)',(feature_name, relation_type, IV))
                    insert_or_not = 1
                else:
                    self.cur.execute('update feature_iv set iv = %s where feature_name = %s and relation_type = %s',(IV, feature_name, relation_type))
                    update_or_not = 1
        print 'series_1 :'
        print series_1
        print 'series_0 :'
        print series_0
        print feature_name,'  ',relation_type,':',IV 
        

    def commit_and_close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

if __name__ =='__main__':
    
    log = tk_log_client.TkLog()
    start = time.time()

    tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
    data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
    
    #计算"关机时长和次数"分布特征
    try:
        for sql, data_type in sql_list:
            id_list = tk_yufa.get_id_list(sql)
            unused_feature = data_online.get_unused_time_feature(date, id_list, data_type, count_bins = range(0,13,2), time_bins = range(0,57,7))
            data_online.insert_into_table(unused_feature[0])
            data_online.insert_into_table(unused_feature[1]) 
    except Exception,e:
        log.error(str(e))
        print 'unused_feature  error\n'
    #计算"平均日通话次数"分布特征
    try:
        for sql, data_type in sql_list:
            id_list = tk_yufa.get_id_list(sql)
            feature = data_online.get_day_average_call_count_feature(date, id_list, data_type, bins = range(0,49,6))
            data_online.insert_into_table(feature)    
    except Exception,e:
        log.error(str(e))
        print 'day_average_call_count  error\n'
    #定义特征通用计算函数
    def common_feature(table_name, feature_name, bins, user_id = 'user_id'):
        try:
            for sql, data_type in sql_list:
                id_list = tk_yufa.get_id_list(sql)
                feature = data_online.get_common_feature(date, id_list, data_type, table_name, feature_name, bins = bins, user_id = user_id)
                data_online.insert_into_table(feature)
        except Exception,e:
            log.error(str(e))
            print '%s  error\n'%feature_name

    #计算"通话次数"分布特征
    common_feature('userinfoformine', 'call_count', bins = range(0,6501,500))
    #计算"通话时间"分布特征
    common_feature('userinfoformine', 'call_time', bins = range(0,420001,30000))
    #计算"手机使用天数"分布特征
    common_feature('userinfoformine', 'sustained_days', bins = range(0,241,30))
    #计算"订单次数"分布特征
    common_feature('ebusiness_feature', 'total_order_count', bins = range(0,481,60))
    #计算"订单金额"分布特征
    common_feature('ebusiness_feature', 'total_price', bins = range(0,36001,3000))
    #计算"使用天数"分布特征
    common_feature('ebusiness_feature', 'used_days',bins = range(0,2601,200))
    #计算"日均消费金额"分布特征
    common_feature('ebusiness_feature', 'price_per_day',bins = range(0,81,8))
    #计算"个推家庭地址距离"分布特征
    common_feature('getuiresult', 'home_offset', bins = range(0,130001,10000), user_id = 'owner_id')
    #计算"个推工作地址距离"分布特征
    common_feature('getuiresult', 'work_offset', bins = range(0,130001,10000), user_id = 'owner_id')
    #计算"百度家庭地址距离"分布特征
    common_feature('baiducredit', 'home_distance', bins = range(0,72001,6000), user_id = 'owner_id')
    #计算"百度工作地址距离"分布特征
    common_feature('baiducredit', 'company_distance', bins = range(0,72001,6000), user_id = 'owner_id')
    #计算"手机平台数"分布特征
    common_feature('loginplatforms', 'phone_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
    #计算"手机贷款次数"分布特征
    common_feature('loginplatforms', 'phone_loan_times', bins = range(0,101,10), user_id = 'owner_id')
    #计算"身份证平台数"分布特征
    common_feature('loginplatforms', 'idcard_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
    #计算"身份证贷款次数"分布特征
    common_feature('loginplatforms', 'idcard_loan_times', bins = range(0,101,10), user_id = 'owner_id')

    
    #计算"关机时长和次数"IV
    try:
        for sql_1, sql_0, relation_type in IV_sql_list:
            id_list_1 = tk_yufa.get_id_list(sql_1)
            id_list_0 = tk_yufa.get_id_list(sql_0)
            unused_feature_1 = data_online.get_unused_time_feature(date, id_list_1, 'nothing', count_bins = range(0,13,2), time_bins = range(0,57,7))
            unused_feature_0 = data_online.get_unused_time_feature(date, id_list_0, 'nothing', count_bins = range(0,13,2), time_bins = range(0,57,7))
            data_online.compute_IV(unused_feature_1[0][1], relation_type, unused_feature_1[0][3], unused_feature_0[0][3])
            data_online.compute_IV(unused_feature_1[1][1], relation_type, unused_feature_1[1][3], unused_feature_0[1][3])
    except Exception,e:
        log.error(str(e))
        print 'unused_feature_IV  error\n'

    #计算"平均日通话次数"IV
    try:
        for sql_1, sql_0, relation_type in IV_sql_list:
            id_list_1 = tk_yufa.get_id_list(sql_1)
            id_list_0 = tk_yufa.get_id_list(sql_0)
            feature_1 = data_online.get_day_average_call_count_feature(date, id_list_1, 'nothing', bins = range(0,49,6))
            feature_0 = data_online.get_day_average_call_count_feature(date, id_list_0, 'nothing', bins = range(0,49,6))
            data_online.compute_IV(feature_1[1], relation_type, feature_1[3], feature_0[3])
    except Exception,e:
        log.error(str(e))
        print 'day_average_call_count_IV  error\n'

    #定义特征IV通用计算函数
    def common_feature_iv(table_name, feature_name, bins, user_id = 'user_id'):
        try:
            for sql_1, sql_0, relation_type in IV_sql_list:
                id_list_1 = tk_yufa.get_id_list(sql_1)
                id_list_0 = tk_yufa.get_id_list(sql_0)
                feature_1 = data_online.get_common_feature(date, id_list_1, 'nothing', table_name, feature_name, bins = bins, user_id = user_id)
                feature_0 = data_online.get_common_feature(date, id_list_0, 'nothing', table_name, feature_name, bins = bins, user_id = user_id)
                data_online.compute_IV(feature_1[1], relation_type, feature_1[3], feature_0[3])
        except Exception,e:
            log.error(str(e))
            print '%s_IV  error\n'%feature_name
    
    #计算"通话次数"分布特征
    common_feature_iv('userinfoformine', 'call_count', bins = range(0,6501,500))
    #计算"通话时间"分布特征
    common_feature_iv('userinfoformine', 'call_time', bins = range(0,420001,30000))
    #计算"手机使用天数"分布特征
    common_feature_iv('userinfoformine', 'sustained_days', bins = range(0,241,30))
    #计算"订单次数"分布特征
    common_feature_iv('ebusiness_feature', 'total_order_count', bins = range(0,481,60))
    #计算"订单金额"分布特征
    common_feature_iv('ebusiness_feature', 'total_price', bins = range(0,36001,3000))
    #计算"使用天数"分布特征
    common_feature_iv('ebusiness_feature', 'used_days',bins = range(0,2601,200))
    #计算"日均消费金额"分布特征
    common_feature_iv('ebusiness_feature', 'price_per_day',bins = range(0,81,8))
    #计算"个推家庭地址距离"分布特征
    common_feature_iv('getuiresult', 'home_offset', bins = range(0,130001,10000), user_id = 'owner_id')
    #计算"个推工作地址距离"分布特征
    common_feature_iv('getuiresult', 'work_offset', bins = range(0,130001,10000), user_id = 'owner_id')
    #计算"百度家庭地址距离"分布特征
    common_feature_iv('baiducredit', 'home_distance', bins = range(0,72001,6000), user_id = 'owner_id')
    #计算"百度工作地址距离"分布特征
    common_feature_iv('baiducredit', 'company_distance', bins = range(0,72001,6000), user_id = 'owner_id')
    #计算"手机平台数"分布特征
    common_feature_iv('loginplatforms', 'phone_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
    #计算"手机贷款次数"分布特征
    common_feature_iv('loginplatforms', 'phone_loan_times', bins = range(0,101,10), user_id = 'owner_id')
    #计算"身份证平台数"分布特征
    common_feature_iv('loginplatforms', 'idcard_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
    #计算"身份证贷款次数"分布特征
    common_feature_iv('loginplatforms', 'idcard_loan_times', bins = range(0,101,10), user_id = 'owner_id')
    
    tk_yufa.commit_and_close()
    data_online.commit_and_close()
    print time.time()-start
