#encoding=utf8
import sys
from model.order_model import *
import json

user_info_count = dict()

@db_session
def get_check_status(user_id, user_info_count):
    check_status = CheckStatus.get(id = user_id)
    if check_status is None:
        return

    user_info_count['user_count'] += 1

    profile_status = check_status.profile_status
    real_id_verify_status = check_status.real_id_verify_status

    for i in range(0,2):
        data = 1 << (i * 2)
        if real_id_verify_status & data == data:
            user_info_count[i+1] += 1

    for i in range(0,9):
        data = 1 << (i * 2)
        if profile_status & data == data:
            user_info_count[i+3] += 1



if __name__ == '__main__':
    db.bind('mysql', host = 'rdsonyxdxtqbyl2e1a59y.mysql.rds.aliyuncs.com', user = 'tk_online', passwd = 'tkonline', db = 'tk_yufa')
    #db.bind('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', user = 'tk_test', passwd = 'tktest', db = 'tk_test')
    db.generate_mapping(create_tables = True)

    user_info_count['user_count'] = 0
    for i in range(1,12):
        user_info_count[i] = 0

    #begin_id = 14167
    #end_id = 25676

    begin_id = 352126
    end_id = 378362
    for i in range(begin_id,end_id):
        get_check_status(i, user_info_count)

    schema_dict = {
        1 : u'姓名/身份证',
        5 : u'学信网',
        4: u'联系人信息',
        6: u'身份证正面',
        7: u'身份证背面',
        8: u'手持身份证',
        9: u'通话详单',
        10: u'工作信息',
        11: u'电商信息'
    }
    temp_str = str(user_info_count['user_count'])
    rate_dict = dict()
    for key in schema_dict:
        rate_dict[schema_dict[key]] = user_info_count[key]

    print  "\t".join([temp_str,json.dumps(rate_dict,ensure_ascii=False)]).encode('utf-8')


