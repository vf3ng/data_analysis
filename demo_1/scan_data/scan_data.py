#encoding=utf8
import sys
from model.order_model import *
import json

def get_status_map(status):
    status_str = ''
    apply_status_t = {
        '0': u'等待审批',
        'i': u'审批中',
        'y': u'通过',
        'r': u'返回修改',
        'n': u'拒绝',

        '1': u'请款中',
        '2': u'打款成功',
        '3': u'打款失败',

        '4': u'm1',
        '5': u'm2',
        '6': u'm3',
        '7': u'委外',
        '8': u'催收完成',

        'a': u'机器审核', # 额度提升中的自动审核
        'b': u'机器拒绝', # 第一轮风控自动拒绝

        '9': u'扣款成功',
        'c': u'扣款失败',
        'd': u'部分成功',
        'e': u'取消订单', # 已注销用户
    }

    if status in apply_status_t:
        status_str = apply_status_t[status]

    return status_str

@db_session
def main(user_id):
    #for apply in select(p for p in Apply):
    apply = Apply.get(id = user_id)
    if apply is None:
        return
    apply_id = apply.id
    apply_type = apply.type

    if apply_type != '0':
        return

    apply_create_at = apply.create_at.strftime("%Y-%m-%d %H:%M:%S") if apply.create_at else ""
    apply_status = apply.status
    user_id = apply.create_by_id

    address_num = len(user_id.address_book)
    call_record_num = len(user_id.call_records)
    call_phone_num = len(set(a.phone_number for a in user_id.call_records))
    phone_call_num = len(user_id.phone_call)
    phone_number_num = len(set(a.other_cell_phone for a in user_id.phone_call))

    print "\t".join([str(apply_id),str(user_id.id),get_status_map(apply_status),apply_create_at,str(address_num),str(call_record_num),str(call_phone_num),str(phone_call_num),str(phone_number_num)]).encode('utf-8')


if __name__ == '__main__':
    #db.bind('mysql', host = 'rdsonyxdxtqbyl2e1a59y.mysql.rds.aliyuncs.com', user = 'tk_online', passwd = 'tkonline', db = 'tk_yufa')
    db.bind('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', user = 'tk_test', passwd = 'tktest', db = 'tk_test')
    db.generate_mapping(create_tables = True)
    for i in range(0,10300):
        try:
            main(i)
        except:
            pass