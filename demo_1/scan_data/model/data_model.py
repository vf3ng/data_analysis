#encoding=utf-8
from pony.orm import *
from datetime import datetime
from datetime import date

from model import db

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
    idcard_image_url = Optional(str,255)