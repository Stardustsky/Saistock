#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:19
# @Author  : Stardustsky
# @File    : core.py
# @Software: PyCharm

import os
from multiprocessing import Pool
from stock_market import market_emotion_index, market_money
from stock_self import mid_stock_basic,get_stock_active,short_stock_basic, nine_change
from spider import get_hot_plate,get_research_report,get_gb_report,get_gb_yb
from func import driver_init


def market_status():
    """
    获得当前市场整体状态
    :return:
    """
    market_score, market_info = market_emotion_index()
    money_flow = market_money()
    gb_data = get_gb_report()
    return market_score, market_info, money_flow, gb_data


def stock_status(stock_code,driver, stock_type="short"):
    """
    获得股票当前状态
    :param stock_code:
    :param stock_type:
    :return:
    """
    if stock_type == "short":
        stock_active_score, stock_active_info = get_stock_active(stock_code, stock_type)
        nine_change_index, nine_change_info = nine_change(stock_code)
        stock_code = stock_code[1:]
        stock_info = short_stock_basic(stock_code,driver)
        stock_info['active_score'] = stock_active_score
        stock_info['active_info'] = stock_active_info
        stock_info['nine_change_index'] = nine_change_index
        stock_info['nine_change_info'] = nine_change_info
        return stock_info

    elif stock_type == "long":
        stock_long_score, stock_long_info = get_stock_active(stock_code, stock_type)
        nine_change_index, nine_change_info = nine_change(stock_code)
        stock_code = stock_code[1:]
        stock_info = mid_stock_basic(stock_code, driver)
        stock_info['active_score'] = stock_long_score
        stock_info['active_info'] = stock_long_info
        stock_info['nine_change_index'] = nine_change_index
        stock_info['nine_change_info'] = nine_change_info
        return stock_info


def news_status(stock_code):
    pass


def plate_status(driver):
    """
    获得当前市场热点以及机构调研结果
    :return:
    """
    # hot_stock_list, hot_concept_dict = get_hot_plate(driver)
    research_report = get_research_report()
    gb_yb = get_gb_yb()
    # return hot_stock_list, hot_concept_dict, research_report
    return gb_yb, research_report


def core_func(driver):
    """
    核心控制函数
    :param driver:
    :param stock_code:
    :param stock_type:
    :return:
    """
    hot_info = plate_status(driver)
    market_score, market_info, money_flow, gb_data = market_status()
    return market_score, market_info, money_flow, gb_data, hot_info

# print stock_status("0600624")
