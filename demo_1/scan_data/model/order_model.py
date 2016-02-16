#encoding=utf-8
from pony.orm import *
from datetime import datetime

from model import db

#db = Database('mysql', host = '121.40.208.254', passwd = 'test1', user = 'root', db = 'TkCash4')
#db = Database('mysql', host = 'rdsxf1ekwvspuq5myl2rp.mysql.rds.aliyuncs.com', passwd = 'tktest', user = 'tk_test', db = 'tk_test')
#db = Database('mysql', host = '121.40.208.254', passwd = 'chick1234', user = 'chick', db = 'TkCash')

VERIFY_STATUS = {'not_passed': 0,
                 'checking': 1,
                 'deny': 2,
                 'pass': 3}

BANK_LIST = ['', u'中国建设银行', u'中国银行', u'中国农业银行', u'招商银行',
             u'广发银行', u'兴业银行', u'中国工商银行', u'中国光大银行',
             u'中国邮政']

APPLY_STATUS = []

class User(db.Entity):
    name = Optional(str, 64)
    phone_no = Required(str, 20)
    password = Required(str, 64)
    channel = Optional(str)
    id_no = Optional(str, 20)
    payment_password = Optional(str, 64)
    create_time = Required(datetime)
    device_name = Optional(str)
    wechat_openid = Optional(str)
    bind_wechat_time = Optional(int)
    last_contract_id = Optional(str, 64)
    device_id = Optional(int, size = 64)
    invitation_id = Optional('User', reverse = 'invitee_list')
    invitee_list = Set('User', reverse = 'invitation_id')
    market_score = Optional(int, default = 0)
    imei = Optional(str, 64)
    imsi = Optional(str, 64)
    android_id = Optional(str, 64)
    local_phone_no = Optional(str, 20)

    check_status = Optional('CheckStatus')
    profile = Optional('Profile')
    id_card_info = Optional('IdCard')

    contact = Set('ContactInfo')
    bankcard = Set('BankCard')
    feedback = Set('Feedback')
    address_book = Set('AddressBook')
    call_records = Set('CallRecord')
    phone_call = Set('PhoneCall')

    apply = Set('Apply')

    weibo_account = Set('WeiboInfo')
    weibo_content = Set('WeiboContent')
    chsi_info = Set('Chsi')

    renren_info = Optional('RenrenAccountInfo')

    signed_contract = Set('Contract')

class Apply(db.Entity):
    create_at = Optional(datetime)
    create_by_id = Required(User)
    finish_time = Optional(datetime)
    money = Optional(int)
    status = Optional(str)
    type = Optional(str)
    pic = Optional(str)
    last_commit_at = Optional(datetime)
    repayment_id = Optional(int)


class CheckStatus(db.Entity):
    owner_id = Required(User)
    #个人资料的填写状态以及审核状态,每两位表示一种资料类型。
    #从低到高依次是个人基本信息（姓名、身份证号码）、联系人信息、学信网、身份证正面、背面、手持
    profile_status = Required(int, size = 64)
    profile_check_status = Required(int, size = 64)
    #提高额度的填写状态和审核状态，每两位表示一种资源类型
    #从低到高以此是微博、人人、通讯录
    increase_status = Optional(int, size = 64)
    increase_check_status = Optional(int, size = 64)
    credit_limit = Required(int)
    max_credit = Required(int)
    apply_status = Optional(int)
    #实名认证提交状态，每两位表示一种资料类型，目前依次是基本信息、学信网
    real_id_verify_status = Optional(int, size = 64)
    #机器自动审核的结果
    auto_check_status = Optional(int)


class Profile(db.Entity):
    owner_id = Required(User)
    gender = Optional(int)
    #工作信息
    job = Optional(int)
    company = Optional(str)
    work_address = Optional(str)
    company_phone = Optional(str, 20)
    family_address = Optional(str)
    expect_amount = Optional(int)
    email = Optional(str)

class IdCard(db.Entity):
    #身份证信息
    owner_id = Required(User)
    id_no = Optional(str, 20)
    id_pic_front = Optional(str, 64)
    id_pic_back = Optional(str, 64)
    id_pic_self = Optional(str, 64)
    id_birth = Optional(datetime)
    id_name = Optional(str, 64)
    id_address = Optional(str)
    id_ctime = Optional(datetime)

    #info_renren = Set('RenrenInfo')
    #info_weibo = Set('WeiboInfo')

class ContactInfo(db.Entity):
    owner_id = Required(User)
    name = Required(str, 64)
    address = Optional(str)
    id_no = Optional(str, 20)
    phone_no = Required(str, 20)
    relationship = Required(int)
    in_addressbook = Optional(int)
    call_times = Optional(int, default = 0)

class BankCard(db.Entity):
    number = Required(str, 32)
    user_id = Required(User)
    bank = Optional(str, 64)
    bank_type = Optional(int)
    card_type = Optional(int, default = 0)

#class FocusPicture(db.Entity):
#    pic_url = Required(str)
#    action_url = Required(str)

class Feedback(db.Entity):
    content = Required(str)
    contact = Optional(str)
    owner_id = Optional(User)
    sub_time = Required(datetime)

class AddressBook(db.Entity):
    phone_number = Required(str, 255)
    name = Optional(str, 64)
    owner_id = Required(User)
    create_time = Optional(int)
    call_times = Optional(int, default = 0)

class CallRecord(db.Entity):
    phone_number = Required(str, 255)
    name = Optional(str, 64)
    #duration = Optional(str, 20)
    duration = Optional(int)
    call_type = Required(int)
    call_time = Required(str, 20)
    owner_id = Required(User)

class PhoneCall(db.Entity):
    cell_phone = Optional(str, 20)
    other_cell_phone = Optional(str,20)
    call_place = Optional(str,255)
    start_time = Optional(datetime)
    use_time = Optional(int)
    call_type = Required(str, 16)
    init_type = Required(str, 16)
    subtotal = Optional(float)
    update_time = Optional(datetime)
    version = Optional(int)
    owner_id = Optional(User)


class WeiboInfo(db.Entity):
    user_id = Required(User)
    username = Required(str, 64)
    province = Optional(int)
    city = Optional(int)
    blog_url = Optional(str)
    gender = Optional(str)
    followers_count = Required(int)
    friends_count = Required(int)
    statuses_count = Required(int)
    favourites_count = Required(int)
    bi_followers_count = Required(int)
    create_at = Required(str, 64)
    verified = Required(int)

class WeiboContent(db.Entity):
    user_id = Required(User)
    username = Required(str, 64)
    content = Required(str, 512)
    source = Optional(str)
    create_at = Required(str, 64)
    comments_count = Required(int)
    reposts_count = Required(int)

class Chsi(db.Entity):
    chsi_name = Required(str, 64)
    school = Required(str)
    head_img = Optional(str)
    gender = Optional(str, 20)
    id_card_number = Optional(str, 20)
    nation = Optional(str)      #民族
    birthday = Optional(str, 20)
    education = Optional(str, 20)   #学历
    collage = Optional(str)     #学院
    school_class = Optional(str)    #班级
    major = Optional(str)       #专业
    student_id = Optional(str)  #学号
    edu_type = Optional(str)    #教育形式(普通全日制什么的)
    enrollment = Optional(str)  #入学时间
    edu_duration = Optional(str, 64)    #学制
    edu_status = Optional(str)      #学籍状态(是毕业还是其他什么的)
    create_at = Optional(datetime)
    user_id = Required(User)

class ChsiAuthInfo(db.Entity):
    username = Optional(buffer)
    password = Optional(buffer)
    code = Optional(str, 32)
    user_id = Required(int, size = 64)

class ContactReverseTimes(db.Entity):
    phone_no = PrimaryKey(str, 20)
    times = Required(int)

class AddressbookReverseTimes(db.Entity):
    phone_no = PrimaryKey(str, 20)
    times = Required(int)

class SendMessageRecord(db.Entity):
    phone_no = Required(str, 20)
    send_time = Required(datetime)
    msg_type = Required(int)    #1:注册, 2:忘记密码
    is_success = Required(int)  #0：失败，1：成功

class BankPayRecord(db.Entity):
    user_id = Required(int)
    pay_time = Required(datetime)
    amount = Required(int)
    sn = Required(str)
    cardid = Required(str)
    is_succcess = Required(int)

class Contract(db.Entity):
    contract_id = PrimaryKey(str)
    sign_time = Required(datetime)
    owner_id = Required(User)
    order_number = Optional(str)

class RenrenAccountInfo(db.Entity):
    owner_id = Required(User)
    username = Required(str, 64)
    province = Optional(str, 32)
    city = Optional(str, 32)
    is_star = Optional(int)         #是否是星级用户
    gender = Optional(str)
    birthday = Optional(str)
    vip_level = Optional(int)       #vip等级
    visitor_count = Optional(int)   #访客人数
    status_count = Optional(int)    #发布的状态数
    blog_count = Optional(int)      #发布的日志数
    album_count = Optional(int)     #相册数
    share_count = Optional(int)     #分享数
    photo_count = Optional(int)     #照片数
    friend_count = Optional(int)    #好友数
    education = Set('RenrenEducation')

class RenrenEducation(db.Entity):
    school = Required(str)
    start_year = Optional(int)
    type = Optional(str)
    department = Optional(str)
    owner_id = Required(RenrenAccountInfo)


#db.generate_mapping(create_tables = True)

if __name__ == "__main__":
    #test()
    print 'done'
