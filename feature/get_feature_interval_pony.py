# -*- coding: utf-8 -*-

from model.data_model import *
import pandas as pd

@db_session
def get_unique_value(instance_set):
    max_version = 0
    value = 0
    for i in instance_set:
        if i.version > max_version:
            max_version = i.version
            value = i.call_count
    #if max_version == 0:
    #    value = list(instance_set)[0].call_count
    
    return value

@db_session
def get_per_value(user_id):
    instance_set = DataUser.get(user_id = user_id).user_info_mine
    value = get_unique_value(instance_set)

    return value


def get_value_list(user_id_list, table_name, column_name):
    result = []
    for i in user_id_list:
        result.append(get_per_value(i))
    
    return result

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

def get_interval(user_id_list, table_name, column_name, num):
    data = get_value_list(user_id_list, table_name, column_name)
    bins = get_average_interval(data,num)
    cut = pd.cut(data, bins, right = False)
    #cut = pd.qcut(data,num)
    print column_name,':'
    print cut.value_counts(),'\n'

@db_session
def get_user_id_list():
    prefix = 'hualahuala%'
    user_id_list = db.select('user_id from datauser where user_id like $prefix limit 5000;')

    return user_id_list

if  __name__ =='__main__':
    DB_HOST = 'rdsv0r421oul5inr17f5.mysql.rds.aliyuncs.com'
    DB_USER = 'tk_yufa'
    DB_PASSWORD = 'tkyufa'
    DB_NAME = 'data_online'
    db.bind('mysql', host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
    db.generate_mapping(create_tables = True)
    user_id_list = get_user_id_list()
    get_interval(user_id_list, 'user_info_mine', 'call_count', 2)
