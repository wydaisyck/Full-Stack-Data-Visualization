import re
import datetime
from dateutil.relativedelta import relativedelta


def convert_time(timestring):
    start_time = timestring[0:10]
    end_time = timestring[13:23]
    start_time = int(re.sub(r'-', '', start_time))
    end_time = int(re.sub(r'-', '', end_time))
    return start_time, end_time


def get_ini_time():
    nowdate = datetime.datetime.now()
    end_date = int(nowdate.strftime("%Y%m%d"))
    start_date = end_date - 10000
    return start_date, end_date


def initimepicker():
    nowdate = datetime.datetime.now()
    last_year = (nowdate - relativedelta(years=1)).strftime('%Y-%m-%d')
    now_year = nowdate.strftime("%Y-%m-%d")
    inidate = last_year + " - " + now_year
    return inidate

