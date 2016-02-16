#encoding=utf8
import sys
from model.data_model import *
import json
import traceback

@db_session
def save_data(user_id,name,phone_no,id_no,home_address,home_tel_num,work_address,work_tel_num,bank_card_num,imei,id_card_url):
    try:
        old_user = DataUser.get(user_id=user_id)
        if old_user is not None:
            old_user.org_account = 'hualahuala'
            old_user.name = name
            old_user.id_card_num = id_no
            old_user.phone_num = phone_no
            old_user.home_address = home_address
            old_user.home_tel_num = home_tel_num
            old_user.work_address = work_address
            old_user.work_tel_num = work_tel_num
            old_user.bank_card_num = bank_card_num
            old_user.imei = imei
            old_user.idcard_image_url = id_card_url
        else:
            new_user = DataUser(user_id=user_id, org_account='hualahuala', name=name, id_card_num=id_no,
                phone_num=phone_no,home_address=home_address,home_tel_num=home_tel_num,
                work_address=work_address,work_tel_num=work_tel_num,bank_card_num=bank_card_num,
                imei=imei,idcard_image_url=id_card_url)
    except Exception,e:
        traceback.print_exc()
        return -1

    return 0

if __name__ == '__main__':

    #db.bind('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', user = 'tk_yufa', passwd = 'tkyufa', db = 'data_yufa')
    db.bind('mysql', host = 'rds4mtr354eazs228252.mysql.rds.aliyuncs.com', user = 'tk_online', passwd = 'tkonline', db = 'data_online')
    db.generate_mapping(create_tables = True)

    for line in sys.stdin:
        line = line.strip().decode('utf-8')
        line_parts = line.split('\t')
        user_id = "hualahuala_%s" % line_parts[0]
        name = line_parts[1]
        phone_no = line_parts[2]
        id_no = line_parts[3]
        home_address = line_parts[4]
        home_tel_num = line_parts[5]
        work_address = line_parts[6]
        work_tel_num = line_parts[7]
        bank_card_num = line_parts[8]
        imei = line_parts[9]
        id_card_url = line_parts[10]

        save_data(user_id,name,phone_no,id_no,home_address,home_tel_num,work_address,work_tel_num,bank_card_num,imei,id_card_url)

