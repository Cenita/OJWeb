import time
import datetime


def get_current_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    sunday += one_day

    # datatime类型转格式字符串
    monday = monday.strftime("%a %b %d %H:%M:%S %Y")
    sunday = sunday.strftime("%a %b %d %H:%M:%S %Y")

    # 格式字符串转时间戳
    monday = int(time.mktime(time.strptime(monday)))
    sunday = int(time.mktime(time.strptime(sunday)))

    return monday, sunday

def get_current_mouth():
    first = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
    last = datetime.date(datetime.date.today().year, datetime.date.today().month + 1, 1) - datetime.timedelta(1)

    # datatime类型转格式字符串
    first = first.strftime("%a %b %d %H:%M:%S %Y")
    last = last.strftime("%a %b %d %H:%M:%S %Y")

    # 格式字符串转时间戳
    first = int(time.mktime(time.strptime(first)))
    last = int(time.mktime(time.strptime(last)))
    return first, last
