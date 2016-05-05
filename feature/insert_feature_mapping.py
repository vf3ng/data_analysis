#-*- coding: utf-8 -*-

import MySQLdb

DB_HOST = 'rdsv0r421oul5inr17f5.mysql.rds.aliyuncs.com'
DB_USER = 'tk_yufa'
DB_PASSWORD = 'tkyufa'
DB_NAME = 'data_online'

conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, charset='utf8')
cur = conn.cursor()

def get_feature_index(bins):
    new_index = ['[%s, %s)'%(bins[i],bins[i+1]) if i!=len(bins)-1 else '[%s, inf)'%bins[i] for i in range(len(bins))]
    return new_index

def insert_into_table(feature_class, feature_name, feature_desc, feature_list):
    for i in feature_list:
        cur.execute('insert into feature_desc values(%s,%s,%s,%s)',(feature_class, feature_name, i, feature_desc))

def close():
    cur.close()
    conn.commit()
    conn.close()   

if __name__=='__main__':

    #通话特征
    feature_index = get_feature_index(range(0,13,2))
    insert_into_table(u'通话特征', 'unused_count', u'关机次数', feature_index)

    feature_index = get_feature_index(range(0,8,1))
    insert_into_table(u'通话特征', 'unused_time', u'关机时长', feature_index)
    
    feature_index = get_feature_index(range(0,49,6))
    insert_into_table(u'通话特征', 'day_average_call_count', u'平均日通话次数', feature_index)

    feature_index = get_feature_index(range(0,6501,500))
    insert_into_table(u'通话特征', 'call_count', u'通话次数', feature_index)

    feature_index = get_feature_index(range(0,420001,30000))
    insert_into_table(u'通话特征', 'call_time', u'通话时间', feature_index)

    feature_index = get_feature_index(range(0,241,30))
    insert_into_table(u'通话特征', 'sustained_days', u'手机使用天数', feature_index)

    #电商特征
    feature_index = get_feature_index(range(0,481,60))
    insert_into_table(u'电商特征', 'total_order_count', u'订单次数', feature_index)

    feature_index = get_feature_index(range(0,36001,3000))
    insert_into_table(u'电商特征', 'total_price', u'订单金额', feature_index)

    feature_index = get_feature_index(range(0,2601,200))
    insert_into_table(u'电商特征', 'used_days', u'使用天数', feature_index)

    feature_index = get_feature_index(range(0,81,8))
    insert_into_table(u'电商特征', 'price_per_day', u'日均消费金额', feature_index)

    #地址特征
    feature_index = get_feature_index(range(0,130001,10000))
    insert_into_table(u'地址特征', 'home_offset', u'个推家庭地址距离', feature_index)

    feature_index = get_feature_index(range(0,130001,10000))
    insert_into_table(u'地址特征', 'work_offset', u'个推工作地址距离', feature_index)

    feature_index = get_feature_index(range(0,72001,6000))
    insert_into_table(u'地址特征', 'home_distance', u'百度家庭地址距离', feature_index)

    feature_index = get_feature_index(range(0,72001,6000))
    insert_into_table(u'地址特征', 'company_distance', u'百度工作地址距离', feature_index)

    #多平台贷款特征
    feature_index = get_feature_index(range(0,31,3))
    insert_into_table(u'多平台贷款特征', 'phone_loan_platform_num', u'手机平台数', feature_index)

    feature_index = get_feature_index(range(0,101,10))
    insert_into_table(u'多平台贷款特征', 'phone_loan_times', u'手机贷款次数', feature_index)

    feature_index = get_feature_index(range(0,31,3))
    insert_into_table(u'多平台贷款特征', 'idcard_loan_platform_num', u'身份证平台数', feature_index)

    feature_index = get_feature_index(range(0,101,10))
    insert_into_table(u'多平台贷款特征', 'idcard_loan_times', u'身份证贷款次数', feature_index)

    close()





    

