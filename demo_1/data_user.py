#encoding=utf-8
from datetime import datetime
from datetime import date
from pony.orm import *
DB_HOST = 'rds4mtr354eazs228252.mysql.rds.aliyuncs.com'
DB_USER = 'tk_online'
DB_PASSWORD = 'tkonline'
DB_NAME = 'data_online'


db = Database()
db.bind('mysql', host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
#db.generate_mapping(create_tables = True)
class DataUser(db.Entity):
        user_id = PrimaryKey(str, 255)
        org_account = Optional(str, 128)
        name = Optional(str, 64)
        id_card_num = Optional(str, 20)
        phone_num = Optional(str, 20)
        home_address = Optional(str)
        home_tel_num = Optional(str, 20)
        work_address = Optional(str)
        work_tel_num = Optional(str, 20)
        bank_card_num = Optional(str, 20)
        imei = Optional(str, 128)

