#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 下午5:49
# @Author  : Stardustsky
# @File    : initial.py
# @Software: PyCharm
import ConfigParser


def read_stock_conf():
    stock_no = dict()
    config = ConfigParser.ConfigParser()
    config.readfp(open("common/stock.ini"), "rb")
    code = config.items("stock_code")
    # for i in code:
    #      stock_no[i[0]] = i[1]
    return code


# aa = read_stock_conf()
# print len(aa)
# print aa[0]