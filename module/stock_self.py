#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 下午5:44
# @Author  : Stardustsky
# @File    : stock_self.py
# @Software: PyCharm

from spider import get_stock_info
import re


def stock_basic(stock, broser):
    try:
        basic = get_stock_info(stock, broser)
        famc = float(re.findall("\d+", basic['famc'])[0])
        value = float(re.findall("\d+", basic['value'])[0])
        famc_scale = famc / value
        pe = float(basic['pe'])
    except Exception:
        pe = 300.0
    stock_basic_score = 1
    if famc >= 5000:
        stock_basic_score *= 0.7
    elif 5000 > famc >= 2000:
        stock_basic_score *= 0.75
    elif 2000 > famc >= 1000:
        stock_basic_score *= 0.8
    elif 1000 > famc >= 500:
        stock_basic_score *= 0.95
    elif 500 > famc >= 100:
        stock_basic_score *= 1.1
    elif 100 > famc >= 50:
        stock_basic_score *= 0.9
    elif 50 > famc >= 10:
        stock_basic_score *= 0.85
    elif famc <= 10:
        stock_basic_score *= 0.7

    if pe > 150:
        stock_basic_score *= 0.88
    elif 150 >= pe > 60:
        stock_basic_score *= 0.9
    elif 60 >= pe > 20:
        stock_basic_score *= 0.95
    elif 20 >= pe > 10:
        stock_basic_score *= 1
    elif 10 >= pe > 5:
        stock_basic_score *= 1.1
    elif pe < 5:
        stock_basic_score *= 1.2

    if famc_scale > 1.5:
        famc_scale = 1.5
    stock_basic_score /= famc_scale
    if stock_basic_score > 1.8:
        stock_basic_score = 1.8
    # print stock_basic_score
    return stock_basic_score

# stock_basic("000526")
