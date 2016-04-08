# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
import calendar

def get_today():
    return date.today()

def get_tomorrow():
    return date.today() + timedelta(1)

def get_yestoday():
    return date.today() - timedelta(1)

def get_first_day_of_week():
    return date.today() - timedelta(date.today().weekday())

def get_first_day_of_month():
    return date.today().replace(day=1)

def get_first_day_of_year():
    return date.today().replace(day=1, month=1)

SPECIAL_WORKDAY=(date(2015, 5, 1),
                 date(2015, 6, 22),
                 date(2015, 9, 3),
                 date(2015, 9, 4),
                 date(2015, 9, 27),
                 date(2015, 10, 1),
                 date(2015, 10, 2),
                 date(2015, 10, 3),
                 date(2015, 10, 6),
                 date(2015, 10, 7),
)

SPECIAL_WEEKEND=(
                 date(2015, 9, 6),
                 date(2015, 10, 10),
)

def is_workday(day):
    if not day:
        day = date.today()
    if day.weekday() >=0 and day.weekday() <=4:
        if day in SPECIAL_WORKDAY:
            return False
        else:
            return True
    else:
        if day in SPECIAL_WEEKEND:
            return True
        else:
            return False

#计算T+i个工作日
def get_next_workday(day=None, i=1):
    if not day:
        day = date.today()
    next_day = day
    for j in range(0, i):
        next_day += timedelta(1)
        while (not is_workday(next_day)):
            next_day += timedelta(1)
    return next_day

def get_next_workdaytime(day=None, i=1):
    if not day:
        day = datetime.now()
    next_day = day
    for j in range(0, i):
        next_day += timedelta(1)
        while (not is_workday(next_day.date())):
            next_day += timedelta(1)
    return next_day

#i个月后的日期
def get_forword_month_day(start_day=None, i=1):
    if not start_day:
        start_day = datetime.now()
    month = start_day.month - 1 + i
    year = start_day.year + month / 12
    month = month % 12 + 1
    day = min(start_day.day, calendar.monthrange(year,month)[1])
    return datetime(year,month,day)

if __name__ == "__main__":
    d = date.today()
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 4, 30)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 5, 1)
    print d, is_workday(d), get_next_workday(d)
    print d, is_workday(d), get_next_workday(d, 3)
    d = date(2015, 5, 2)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 5, 3)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 5, 4)
    print d, is_workday(d), get_next_workday(d)
    print d, is_workday(d), get_next_workday(d, 1)
    print d, is_workday(d), get_next_workday(d, 2)
    print d, is_workday(d), get_next_workday(d, 3)
    d = date(2015, 9, 2)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 9, 3)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 9, 4)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 9, 5)
    print d, is_workday(d), get_next_workday(d)
    d = date(2015, 9, 6)
    print d, is_workday(d), get_next_workday(d)
    #print get_forword_month_day(d, 1)
    #print get_forword_month_day(d, 2)
    #print get_forword_month_day(d, 3)
    #print get_forword_month_day(d, 9)
    #print get_first_day_of_year()
