#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:30
# @Author  : Stardustsky
# @File    : external_market.py
# @Software: PyCharm

from spider import get_china_index_data


def internal_index(broser=""):
    china_sz_index = 1
    china_cyb_index = 1
    sz_index, cyb_index = get_china_index_data(broser)
    sz_score = float(sz_index['score'].encode("utf-8"))
    cyb_score = float(cyb_index['score'].encode("utf-8"))
    if sz_score < 2500:
        china_sz_index *= 1.5
    elif 2500 <= sz_score < 2700:
        china_sz_index *= 1.3
    elif 2700 <= sz_score < 3000:
        china_sz_index *= 1.2
    elif 3000 < sz_score < 3700:
        china_sz_index *= 1.0
    elif 3700 <= sz_score < 4800:
        china_sz_index *= 1.4
    elif 4800 <= sz_score < 5000:
        china_sz_index *= 1.1
    elif 5000 <= sz_score < 6000:
        china_sz_index *= 0.8
    elif 6000 <= sz_score:
        china_sz_index *= 0.5
    # print china_sz_index
    return china_sz_index

# internal_index()
