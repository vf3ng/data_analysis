# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import MySQLdb
from datetime import datetime, timedelta
from common import tk_log_client

class DBoperator(object):

    def __init__(self, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
        self.conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset='utf8')
        self.cur = self.conn.cursor()

    #tk_yufa使用
    def get_sql_data(self, sql):
        dataframe = pd.read_sql(sql, self.conn)
        return dataframe    

    def get_max_version_data(self, tk_yufa_dataframe, table_name, user_id):
        if tk_yufa_dataframe.shape[0] == 0:
            ids = "('nothing')"
        else :
            tk_yufa_dataframe['id'] = ['hualahuala_'+str(i) for i in tk_yufa_dataframe['create_by_id']]
            ids = str(tuple(tk_yufa_dataframe['id']))
        sql_version = '''
            select * from %s as t1
            join (select %s, max(version) as max_version
                from %s 
                where %s in %s
                group by %s) as t2
            on t1.%s = t2.%s and t1.version = t2.max_version;
                      ''' %(table_name, user_id, table_name, user_id, ids, user_id, user_id, user_id)
        dataframe = self.get_sql_data(sql_version)
        return dataframe
        
    def get_common_feature(self, date, tk_yufa_dataframe, data_type, table_name, feature_name, bins, user_id = 'user_id'):
        dataframe = self.get_max_version_data(tk_yufa_dataframe, table_name, user_id)
        data = dataframe[feature_name].replace(['',-1],np.nan).dropna()
        cut = pd.cut(data, bins, right = False).replace(np.nan, '[%s, inf)'%bins[-1])
        result = cut.value_counts()
        new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]
        final_result = result.reindex(new_index).fillna(0)
        #final_result = result[sorted(result.index, key = lambda x: int(x.split(',')[0][1:]))]
        print feature_name,'  ',data_type,':'
        print final_result,'\n'
        return (date, feature_name, data_type, final_result)

    def get_unused_time_feature(self, date, tk_yufa_dataframe, data_type, count_bins, time_bins):
        dataframe = self.get_max_version_data(tk_yufa_dataframe, 'blacklist', 'user_id')
        data = dataframe['unused_time'].replace('',np.nan).dropna()
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
        count_cut = pd.Series(pd.cut(unused_count, count_bins, right = False)).replace(np.nan, '[%s, inf)'%count_bins[-1])
        time_cut = pd.Series(pd.cut(unused_time, time_bins, right = False)).replace(np.nan, '[%s, inf)'%time_bins[-1])
        result_count = count_cut.value_counts()
        result_time = time_cut.value_counts()
        new_count_index = ['[%s, %s)'%(count_bins[i],count_bins[i+1]) if i!=len(count_bins)-1 else '[%s, inf)'%count_bins[i] for i in range(len(count_bins))]
        final_result_count = result_count.reindex(new_count_index).fillna(0)
        new_time_index = ['[%s, %s)'%(time_bins[i],time_bins[i+1]) if i!=len(time_bins)-1 else '[%s, inf)'%time_bins[i] for i in range(len(time_bins))]
        final_result_time = result_time.reindex(new_time_index).fillna(0)
        #final_result_count = result_count[sorted(result_count.index, key = lambda x: int(x.split(',')[0][1:]))] 
        #final_result_time = result_time[sorted(result_time.index, key = lambda x: int(x.split(',')[0][1:]))]
        print 'unused_count    %s : '%data_type
        print final_result_count,'\n'
        print 'unused_time    %s : '%data_type
        print final_result_time,'\n'
        return [(date, 'unused_count', data_type, final_result_count), (date, 'unused_time', data_type, final_result_time)]


    def get_day_average_call_count_feature(self, date, tk_yufa_dataframe, data_type, bins):
        dataframe = self.get_max_version_data(tk_yufa_dataframe, 'userinfoformine', 'user_id')
        data = dataframe[dataframe['sustained_days']!=0].copy()
        data.loc[:,'day_average_call_count'] = data['call_count']/data['sustained_days']
        data = data['day_average_call_count'].dropna()
        cut = pd.cut(data, bins, right =False).replace(np.nan, '[%s, inf)'%bins[-1])
        result = cut.value_counts()
        new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]
        final_result = result.reindex(new_index).fillna(0)
        #final_result = result[sorted(result.index, key = lambda x: int(x.split(',')[0][1:]))]
        print 'day_average_call_count    %s : '%data_type
        print final_result,'\n'
        return (date, 'day_average_call_count', data_type, final_result)

    def insert_into_table(self, feature_data):
        for i in range(len(feature_data[3])):
            self.cur.execute('insert into day_interval_feature values(%s,%s,%s,%s,%s)',(feature_data[0],feature_data[1],feature_data[2],feature_data[3].index[i],feature_data[3][i]))

    def commit_and_close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        

if __name__ =='__main__':
    
    import threading
    import time
    
    log = tk_log_client.TkLog()    

    date = datetime.now().strftime('%Y-%m-%d')
    date_time_start = datetime.now().strftime('%Y-%m-%d 00:00:00')
    date_time_end = (datetime.now()+timedelta(1)).strftime('%Y-%m-%d 00:00:00')    

    DB_HOST = 'rdsv0r421oul5inr17f5.mysql.rds.aliyuncs.com'
    DB_USER = 'tk_yufa'
    DB_PASSWORD = 'tkyufa'
    DB_NAME1 = 'tk_yufa'
    DB_NAME2 = 'data_online'
    
    tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
    data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
    
    #data_type
    sql_apply_id = '''
                    select create_by_id from apply
                    where create_at >= '%s' and create_at < '%s' and status != 'e';
                   '''%(date_time_start, date_time_end)
    
    sql_apply_pass_id = '''
                    select create_by_id from apply
                    where create_at >= '%s' and create_at < '%s' and status != 'n' and status != 'b' and status != 'e';
                        '''%(date_time_start, date_time_end)
    
    sql_m0_id = '''
                select create_by_id from apply
                where type = 'a';
                '''

    sql_m1_id = '''
                select create_by_id from apply
                where type = 'b';
                '''

    sql_m2_id = '''
                select create_by_id from apply
                where type = 'c';
                '''

    sql_m3_id = '''
                select create_by_id from apply
                where type = 'd';
                '''

    sql_m4_id = '''
                select create_by_id from apply
                where type = 'e';
                '''

    sql_list = [(sql_apply_id, 'apply'),(sql_apply_pass_id,'apply_pass'),(sql_m0_id,'m0'),(sql_m1_id,'m1'),(sql_m2_id,'m2'),(sql_m3_id,'m3'),(sql_m4_id,'m4')]

    #计算"关机时长和次数"分布特征
    def unused_feature():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                unused_feature = data_online.get_unused_time_feature(date, tk_dataframe, data_type, count_bins = range(0,13,2), time_bins = range(0,57,7))
                data_online.insert_into_table(unused_feature[0])
                data_online.insert_into_table(unused_feature[1])
            tk_yufa.commit_and_close()
            data_online.commit_and_close() 
        except Exception,e:
            print 'unused_feature  error\n' 
            log.error(str(e))
    #计算"平均日通话次数"分布特征
    def day_average_call_count():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_day_average_call_count_feature(date, tk_dataframe, data_type, bins = range(0,49,6))
                data_online.insert_into_table(feature)    
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'day_average_call_count  error\n'
            log.error(str(e))
    #计算"通话次数"分布特征
    def call_count():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'userinfoformine', 'call_count', bins = range(0,6501,500))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'call_count  error\n'    
            log.error(str(e))
    #计算"通话时间"分布特征
    def call_time():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'userinfoformine', 'call_time', bins = range(0,420001,30000))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'call_time  error\n'
            log.error(str(e))
    #计算"手机使用天数"分布特征
    def sustained_days():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'userinfoformine', 'sustained_days', bins = range(0,241,30))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'sustained_days  error\n'
            log.error(str(e))
    #计算"订单次数"分布特征
    def total_order_count():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'ebusiness_feature','total_order_count',bins = range(0,481,60))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'total_order_count  error\n'
            log.error(str(e))
    #计算"订单金额"分布特征
    def total_price():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'ebusiness_feature','total_price',bins = range(0,36001,3000))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'total_price  error\n'
            log.error(str(e))
    #计算"使用天数"分布特征
    def used_days():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'ebusiness_feature','used_days',bins = range(0,2601,200))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'used_days  error\n'
            log.error(str(e))
    #计算"日均消费金额"分布特征
    def price_per_day():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'ebusiness_feature','price_per_day',bins = range(0,81,8))
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'price_per_day  error\n'
            log.error(str(e))
    #计算"个推家庭地址距离"分布特征
    def home_offset():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'getuiresult', 'home_offset', bins = range(0,130001,10000), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'home_offset  error\n'
            log.error(str(e))
    #计算"个推工作地址距离"分布特征
    def work_offset():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'getuiresult', 'work_offset', bins = range(0,130001,10000), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'work_offset  error\n'
            log.error(str(e))
    #计算"百度家庭地址距离"分布特征
    def home_distance():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'baiducredit', 'home_distance', bins = range(0,72001,6000), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'home_distance  error\n'
            log.error(str(e))
    #计算"百度工作地址距离"分布特征
    def company_distance():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'baiducredit', 'company_distance', bins = range(0,72001,6000), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'company_distance  error\n'
            log.error(str(e))
    #计算"手机平台数"分布特征
    def phone_loan_platform_num():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'loginplatforms', 'phone_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'phone_loan_platform_num  error\n'
            log.error(str(e))
    #计算"手机贷款次数"分布特征
    def phone_loan_times():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'loginplatforms', 'phone_loan_times', bins = range(0,101,10), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'phone_loan_times  error\n'
            log.error(str(e))
    #计算"身份证平台数"分布特征
    def idcard_loan_platform_num():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'loginplatforms', 'idcard_loan_platform_num', bins = range(0,31,3), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'idcard_loan_platform_num  error\n'
            log.error(str(e))
    #计算"身份证贷款次数"分布特征
    def idcard_loan_times():
        tk_yufa = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME1)
        data_online = DBoperator(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME2)
        try:
            for sql, data_type in sql_list:
                tk_dataframe = tk_yufa.get_sql_data(sql)
                feature = data_online.get_common_feature(date, tk_dataframe, data_type, 'loginplatforms', 'idcard_loan_times', bins = range(0,101,10), user_id = 'owner_id')
                data_online.insert_into_table(feature)
            tk_yufa.commit_and_close()
            data_online.commit_and_close()
        except Exception,e:
            print 'idcard_loan_times  error\n'
            log.error(str(e))

    threads = []
    start = time.time()
    threads.append(threading.Thread(target = lambda : (unused_feature(),day_average_call_count(),call_count()), args = ()))
    threads.append(threading.Thread(target = lambda : (call_time(),sustained_days(),total_order_count()), args = ()))
    threads.append(threading.Thread(target = lambda : (total_price(),used_days(),price_per_day()), args = ()))
    threads.append(threading.Thread(target = lambda : (home_offset(),work_offset(),home_distance()), args = ()))
    threads.append(threading.Thread(target = lambda : (company_distance(),phone_loan_platform_num()), args = ()))
    threads.append(threading.Thread(target = lambda : (phone_loan_times(),idcard_loan_platform_num(),idcard_loan_times()), args = ()))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    print time.time()-start

