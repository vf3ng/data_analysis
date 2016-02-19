#coding=utf-8
from data_user import *
db.generate_mapping(create_tables = True)

@db_session
def get_data(uid):
    uid = "hualahuala_"+uid
    user = DataUser.get(user_id=uid)
    return [user.name.encode("utf8"),user.id_card_num,user.phone_num,user.home_address.encode("utf8"),user.work_address.encode("utf8")]

if __name__ == '__main__':
    file1 = open("b2","r")
    lines = file1.readlines()
    file1.close()
    file2 = open("user_data","w")
    for i in lines:
        id,check_status,code = i.split()
        list1  = get_data(id)
        list2 = [id,check_status,code]+list1
        list2 = [str(i) for i in list2]
        str1 = ' '.join(list2)
        file2.write(str1+'\n')
    file2.close()
        
    
