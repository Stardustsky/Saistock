#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 11:03
# @Author  : Stardustsky
# @File    : stock_notice.py
# @Software: PyCharm
from func import stock_email,read_stock_conf
from stock_self import nine_change
import datetime
import time

def nine_change_notice():
    dict_info = ""
    code = read_stock_conf()
    for key, value in code:
        res = nine_change(key)
        dict_info += key[1:]+":"+unicode(value, 'utf-8')+":[info] "+res[1]+"\n"
    print dict_info
    stock_email('454640446@qq.com', dict_info)
    return dict_info


def price_notice():
    pass


def clock_notice():
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    while True:
        obj = open("common/date.ini", 'r+')
        date = obj.readlines()[0]
        if now_time != date:
            obj.seek(0)
            obj.truncate()
            obj.writelines(now_time)
            nine_change_notice()
        obj.close()
        time.sleep(43200)



def notice_center():
    pass

clock_notice()