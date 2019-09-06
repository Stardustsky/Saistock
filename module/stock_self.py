#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 下午5:44
# @Author  : Stardustsky
# @File    : stock_self.py
# @Software: PyCharm

from spider import get_stock_info
import re


def mid_stock_basic(stock_info):
    """
    中线股票基本面分析
    :param stock:
    :return:
    """

    try:
        famc = float(stock_info["stock_facm"])
        active_pe = float(stock_info["stock_pe_active"])
        static_pe = float(stock_info["stock_pe_static"])

        if active_pe >= 300 or active_pe < 0:
            active_pe = 300.0
    except Exception:
        print u'[info]股票代码有误或网络错误。'
    stock_basic_score = 1

    # 市值分析
    if famc >= 5000:
        stock_basic_score *= 0.95
    elif 5000 > famc >= 2000:
        stock_basic_score *= 0.96
    elif 2000 > famc >= 1000:
        stock_basic_score *= 0.97
    elif 1000 > famc >= 500:
        stock_basic_score *= 0.98
    elif 500 > famc >= 100:
        stock_basic_score *= 1.02
    elif 100 > famc >= 50:
        stock_basic_score *= 0.99
    elif 50 > famc >= 10:
        stock_basic_score *= 0.95
    elif famc <= 10:
        stock_basic_score *= 0.88

    #市盈率分析
    if active_pe > 150:
        stock_basic_score *= 0.8
    elif 150 >= active_pe > 60:
        stock_basic_score *= 0.85
    elif 60 >= active_pe > 20:
        stock_basic_score *= 0.9
    elif 20 >= active_pe > 10:
        stock_basic_score *= 1
    elif 10 >= active_pe > 5:
        stock_basic_score *= 1.1
    elif active_pe < 5:
        stock_basic_score *= 1.2

    if stock_basic_score > 1.8:
        stock_basic_score = 1.8

    print stock_basic_score
    return stock_basic_score

