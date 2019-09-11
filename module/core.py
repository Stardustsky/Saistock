#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:19
# @Author  : Stardustsky
# @File    : core.py
# @Software: PyCharm

import os
from multiprocessing import Pool
from initial import read_stock_conf
from stock_market import market_emotion_index
from stock_self import mid_stock_basic,stock_active,short_stock_basic
from spider import get_hot_plate


def market_status():
    """
    获得当前市场整体状态
    :return:
    """
    market_score, market_info = market_emotion_index()
    return market_score, market_info


def stock_status(stock_code, stock_type="short"):
    """
    获得股票当前状态
    :param stock_code:
    :param stock_type:
    :return:
    """
    if stock_type == "short":
        stock_active_score, stock_active_info = stock_active(stock_code, stock_type)
        stock_code = stock_code[1:]
        stock_basic_score, stock_basic_info = short_stock_basic(stock_code)
        return stock_active_score, stock_active_info, stock_basic_score, stock_basic_info
    elif stock_type == "long":
        stock_long_score, stock_active_info = stock_active(stock_code, stock_type)
        stock_code = stock_code[1:]
        stock_basic_score, stock_basic_info = mid_stock_basic(stock_code)
        return stock_long_score, stock_active_info, stock_basic_score, stock_basic_info


def news_status(stock_code):
    pass

def plate_status():
    """
    获得当前市场热点
    :return:
    """
    hot_stock_list, hot_concept_dict = get_hot_plate()
    return hot_stock_list, hot_concept_dict

print stock_status("0600155",stock_type="long9ui09")