#encoding=utf8
import sys
from model.order_model import *
import json
import traceback
import re

@db_session
def filter_latest_version_data(db_data):
    max_version = 0
    for data in db_data:
        if data.version > max_version:
            max_version = data.version

    data_list = list()
    for data in db_data:
        if data.version == max_version:
            data_list.append(data)


    return data_list


@db_session
def get_data(user_id):
    user = User.get(id = user_id)
    if user is None:
        return 

    if user.check_status.apply_status in [3,4,5]:
        phone_call_list = filter_latest_version_data(user.phone_call)
        for phone_call in phone_call_list:
            if re.match(r'1\d{10}$',phone_call.other_cell_phone) == None and phone_call.other_cell_phone not in tel_number_set:
                tel_number_set.add(phone_call.other_cell_phone)
                print 'corp_debug_'+str(user_id) ,phone_call.cell_phone, phone_call.other_cell_phone, phone_call.start_time, phone_call.use_time
        
tel_number_set = set()

if __name__ == '__main__':
    db.bind('mysql', host = 'rdsonyxdxtqbyl2e1a59y.mysql.rds.aliyuncs.com', user = 'tk_online', passwd = 'tkonline', db = 'tk_yufa')
    #db.bind('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', user = 'tk_test', passwd = 'tktest', db = 'tk_test')
    db.generate_mapping(create_tables = True)
    for i in range(29933,30050):
        try:
            get_data(i)
        except:
            traceback.print_exc()
            pass
