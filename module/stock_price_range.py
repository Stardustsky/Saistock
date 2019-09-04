#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:27
# @Author  : Stardustsky
# @File    : price_range.py
# @Software: PyCharm

from spider import get_price_data
import numpy as np


def stock_info(stock, broser=""):
    """
    :return: 中线推荐指数，当前股票活跃度
    """
    stock_max_price, stock_buttom_price, stock_avarage_price, stock_now_price, stock_volume = get_price_data(stock)
    long_line = (stock_max_price - stock_avarage_price) / (stock_avarage_price - stock_buttom_price) / (stock_now_price / stock_avarage_price)
    short_active_rate = stock_volume[0:9].mean() / stock_volume.mean()
    # print stock_volume[0:9]
    # print stock_volume
    # print long_line, short_active_rate
    if long_line > 3.5:
        long_line = 3.5
    if short_active_rate > 2.0:
        short_active_rate = 2.0
    return long_line, short_active_rate

# stock_info("1000526")