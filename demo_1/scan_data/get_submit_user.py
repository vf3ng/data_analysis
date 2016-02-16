#encoding=utf8
import sys
from model.order_model import *
import json
import traceback

@db_session
def get_data(user_id):
    user = User.get(id = user_id)
    if user is None:
        return 

    if user.check_status.apply_status in [5]:
        #home_address = user.profile.family_address if user.profile is not None else ''
        #home_tel_num = ''
        #work_address = user.profile.work_address if user.profile is not None else ''
        #work_tel_num = user.profile.company_phone if user.profile is not None else ''
        #job = user.profile.job
        #bank_card_num = ''
        #imei = user.imei
        #id_card_url = "http://tk-pic.oss-cn-hangzhou.aliyuncs.com/%s" % user.id_card_info.id_pic_front if user.id_card_info is not None else ''

        #education = []
        #for chsi in user.chsi_info:
        #    education.append(chsi.education)

        #parent_phone_list = []
        #for contact in user.contact:
        #    if contact.relationship in [1,2]:
        #        parent_phone_list.append(contact.phone_no)
        print str(user_id)
        #print "\t".join([str(user_id), user.name, user.phone_no, user.id_no,",".join(education), ",".join(parent_phone_list),str(imei),home_address,work_address,str(job),str(user.check_status.apply_status),str(user.check_status.auto_check_status)]).encode('utf-8')

        #print "\t".join([str(user_id), user.name, user.phone_no, user.id_no,home_address,home_tel_num,work_address,work_tel_num,bank_card_num,imei,id_card_url]).encode('utf-8')


if __name__ == '__main__':
    db.bind('mysql', host = 'rdsonyxdxtqbyl2e1a59y.mysql.rds.aliyuncs.com', user = 'tk_online', passwd = 'tkonline', db = 'tk_yufa')
    #db.bind('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', user = 'tk_test', passwd = 'tktest', db = 'tk_test')
    db.generate_mapping(create_tables = True)
    file1 = open("reject","w")
    for i in range(371616,381994):
        try:
            get_data(i)
        except:
            traceback.print_exc()
            pass
