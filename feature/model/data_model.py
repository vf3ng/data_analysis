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

    
    user_info_mine = Set('UserInfoForMine')
    contact_info_mine = Set('ContactInfoForMine')
    contact_info = Set('DataContactInfo')
    blacklist = Set('BlackList')
    minedIntimateContactInfo = Set('MinedIntimateContactInfo')
    minedCorpContactInfo = Set('MinedCorpContactInfo')
    getui_info = Set('GeTuiResult')
    dishonest_login = Set('DishonestLogin')
    login_platforms = Set('LoginPlatforms')
    szr_result = Set('SzrResult')
    phone_call_list = Set('PhoneCall')
    location_info = Set('LocationInfo')
    ebusiness_basic = Set('Ebusiness_Basic')
    deliver_address = Set('Deliver_Address')
    report_data_source = Set('Data_Source')
    baiducredit = Set('Baiducredit')
    ebusiness_feature = Set('Ebusiness_feature')
    
class DataContactInfo(db.Entity):
    user_id = Required(DataUser)
    org_account = Optional(str, 128)
    name = Required(str, 64)
    phone_num = Required(str, 20)
    relationship = Required(int)


class BlackList(db.Entity):
    user_id = Required(DataUser)
    is_in_blacklist = Optional(bool)
    unused_time = Optional(str)
    version = Optional(int)
    update_time = Optional(datetime)

class UserInfoForMine(db.Entity):
    user_id = Required(DataUser)
    phonenum = Optional(str)
    name = Optional(str)
    is_real_name = Optional(str)
    id_num = Optional(str)
    reg_time = Optional(datetime)
    version = Optional(int)
    update_time = Optional(datetime)
    call_count = Optional(int)

class ContactInfoForMine(db.Entity):
    user_id = Required(DataUser)
    contact_phonenum = Required(str)
    call_count = Optional(int)
    call_passive_count = Optional(int)
    call_count_norm = Optional(float)
    call_time = Optional(int)
    call_passive_time = Optional(int)
    call_time_norm = Optional(float)
    call_first_date = Optional(datetime)
    call_last_date = Optional(datetime)
    call_period = Optional(int)
    call_period_norm = Optional(float)
    call_day_count = Optional(int)
    call_max_oneday_count = Optional(int)
    call_max_oneday_date = Optional(date)
    sms_count = Optional(int)
    version = Optional(int)
    update_time = Optional(datetime)

class MinedIntimateContactInfo(db.Entity):
    user_id = Required(DataUser)
    contact_phonenum = Required(str)
    score = Optional(float)
    rank = Optional(int)
    version = Optional(int)
    update_time = Optional(datetime)

class MinedCorpContactInfo(db.Entity):
    user_id = Required(DataUser)
    contact_phonenum = Required(str)
    score = Optional(float)
    rank = Optional(int)
    corp_name = Optional(str)
    version = Optional(int)
    update_time = Optional(datetime)

class GeTuiResult(db.Entity):
    owner_id = Required(DataUser)
    home_offset = Optional(int)
    work_offset = Optional(int)
    last_login_time = Optional(str,nullable=True)
    version = Optional(int)

class Baiducredit(db.Entity):
    owner_id = Required(DataUser)
    home_distance = Optional(int)
    company_distance = Optional(int)
    

class DishonestLogin(db.Entity):
    owner_id = Required(DataUser)
    hit_rule = Optional(str)
    is_hit = Optional(int)
    version = Optional(int)

class LoginPlatforms(db.Entity):
    owner_id = Required(DataUser)
    phone_loan_times = Optional(int)
    phone_loan_platform_num = Optional(int)
    phone_loan_times_per_platform = Optional(float)
    idcard_loan_times = Optional(int)
    idcard_loan_platform_num = Optional(int)
    idcard_loan_times_per_platform = Optional(float)
    loan_times_per_platform = Optional(float)
    phone_dishonest_times = Optional(int)
    idcard_dishonest_times = Optional(int)
    version = Optional(int)

class SzrResult(db.Entity):
    owner_id = Required(DataUser)
    status = Optional(int)
    grade = Optional(str,nullable=True)
    source_id = Optional(str,nullable=True)
    data_build_time = Optional(str,nullable=True)
    money_bound = Optional(str,nullable=True)
    data_status = Optional(str,nullable=True)
    version = Optional(int)

class PhoneCall(db.Entity):
    cell_phone = Optional(str, 20)
    other_cell_phone = Optional(str, 64)
    call_place = Optional(str, 255)
    start_time = Optional(datetime)
    use_time = Optional(int)
    call_type = Optional(str, 64)
    init_type = Optional(str, 64)
    subtotal = Optional(float)
    update_time = Optional(datetime)
    version = Optional(int)
    owner_id = Required(DataUser)

class LocationInfo(db.Entity):
    user_id = Required(DataUser)
    location = Optional(str)
    first_time = Optional(datetime)
    last_time = Optional(datetime)
    version = Optional(int)
    update_time = Optional(datetime)

class Ebusiness_Basic(db.Entity):
    owner_id = Required(DataUser)
    website_id = Optional(str,255)
    nickname = Optional(str,255)
    real_name = Optional(str,255)
    is_validate_real_name = Optional(int)
    level = Optional(str,255)
    cell_phone = Optional(str,255)
    email = Optional(str,255)
    security_level = Optional(str,255)
    register_date = Optional(datetime)
    update_time = Optional(datetime)
    version = Optional(int)
    datasource = Optional(str,255)

class Ebusiness_feature(db.Entity):
    user_id = Required(DataUser)
    total_order_count = Optional(int)
    total_price = Optional(float)
    used_days = Optional(int)
    price_per_day = Optional(float)
    version = Optional(int)
    update_time = Optional(datetime)

class Deliver_Address(db.Entity):
    owner_id = Required(DataUser)
    address = Optional(str,255)
    lng = Optional(float)
    lat = Optional(float)
    predict_addr_type = Optional(str,255)
    begin_date = Optional(datetime)
    end_date = Optional(datetime)
    total_amount = Optional(float)
    total_count = Optional(float)
    version = Optional(int)
    receiver_list = Set('Receiver')

class Receiver(db.Entity):
    owner_id = Required(Deliver_Address)
    name = Optional(str,255)
    phone_num_list = Optional(str,255)
    amount = Optional(float)
    count = Optional(float)
    version = Optional(int)

class Data_Source(db.Entity):
    owner_id = Required(DataUser)
    key = Optional(str,255)
    name = Optional(str,255)
    account = Optional(str,255)
    category_name = Optional(str,255)
    category_value = Optional(str,255)
    status = Optional(str,255)
    reliability = Optional(str,255)
    binding_time = Optional(datetime)
    version = Optional(int)
