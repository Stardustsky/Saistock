#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:24
# @Author  : Stardustsky
# @File    : external_index.py
# @Software: PyCharm
# @外部指数模块

from spider import get_usa_index_data


def external_index(broser=""):
    usa_stock_index = 1
    nsdk_index, dqs_index = get_usa_index_data(broser)
    nsdk_range = float(nsdk_index['range'].encode("utf-8").replace("%", ""))
    dqs_range = float(dqs_index['range'].encode("utf-8").replace("%", ""))
    if nsdk_range <= -4.0 or dqs_range <= -4.0:
        usa_stock_index /= 5
    elif -4.0 < nsdk_range <= -3.0 or -4.0 < dqs_range <= -3.0:
        usa_stock_index /= 3.0
    elif -2.5 < nsdk_range <= -2.0 or -2.5 < dqs_range <= -2.0:
        usa_stock_index /= 1.3
    elif -2.0 < nsdk_range <= -1.0 or -2.0 <= dqs_range <= -1.0:
        usa_stock_index /= 1.1
    elif nsdk_range >= 2.0 or dqs_range >= 2.0:
        usa_stock_index /= 1.1
    elif 1.0 > nsdk_range >= -1.0 or 1.0 > dqs_range >= -1.0:
        usa_stock_index *= 1.1

    # print dqs_range < -3.0
    # print nsdk_range, dqs_range
    # print usa_stock_index
    return usa_stock_index

# external_index()