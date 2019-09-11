#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午2:11
# @Author  : Stardustsky
# @File    : center.py
# @Software: PyCharm

import json
import urllib2
from module.core import news_status,market_status,plate_status,stock_status


stock_list = {
    "中国平安":601318
}



def main():
    market_score, market_info = market_status()
    hot_stock_list, hot_concept_dict = plate_status()

if __name__ == '__main__':
    stock_num = ""