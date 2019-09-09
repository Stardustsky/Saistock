#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:16
# @Author  : Stardustsky
# @File    : spider.py
# @Software: PyCharm

import urllib2
import os
import json
import pandas as pd
import datetime
import time
from lxml import etree
import requests
from bs4 import BeautifulSoup
import fileinput
from selenium import webdriver







# def get_data(stock="sz000001"):
#     url = uri+stock+".html"
#     chrome.get("http://quote.eastmoney.com/sz000001.html")
#     # print chrome.page_source
#     # current_price = chrome.find_element_by_xpath('//*[@id="price9"]').text
#     # print current_price
#
#     print chrome.find_element_by_xpath('//*[@id="price9"]').text
#
#     # selector.xpath('//*[@id="hxc3_cs_testcanvas"]/div[1]')[0].text
# #
#
# def get_price_range_data():
#     pass
#


def get_price_data(stock="", t_length=-100):
    """
    获取股票100日内最高价/最低价/平均价/现价/10日涨跌幅/股票活跃度
    :param stock:
    :param t_length:
    :return:
    """
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    old_time = (datetime.datetime.now() + datetime.timedelta(days=t_length)).strftime('%Y%m%d')
    wy_api = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER"%(stock, old_time, now_time)
    response = urllib2.urlopen(wy_api)
    data = response.read()
    data = data.replace('\'', '')
    data = data.decode('gbk').encode('utf-8')
    obj = open("data/%s.csv"%stock, "w")
    obj.write(data)
    obj.close()
    df = pd.read_csv("data/%s.csv"%stock)
    df = df[(True ^ df['成交量'].isin([0]))]
    stock_avarage_price = df['收盘价'].mean()
    stock_max_price = df['收盘价'].max()
    stock_buttom_price = df['收盘价'].min()
    stock_now_price = df['收盘价'][1]
    stock_price_range = df['涨跌幅'][0:10]
    stock_100_volume = df['成交量'][0:50].mean()
    stock_5_volume = df['成交量'][0:5].mean()
    stock_active = stock_5_volume / stock_100_volume
    return stock_max_price, stock_buttom_price, stock_avarage_price, stock_now_price, stock_active, stock_price_range


def get_china_index_data():
    """
    获取上证指数，创业板指数
    :return:
    """
    cyb_index = dict()
    sz_index = dict()
    # 创业板指数
    cyb = "http://hq.sinajs.cn/list=sz399006"
    # 上证指数
    sz = "http://hq.sinajs.cn/list=sh000001"
    index = map(urllib2.urlopen, [cyb, sz])
    data_cyb = index[0].read()
    cyb_index["now"] = data_cyb.split(",")[3]
    cyb_index["lastday"] = data_cyb.split(",")[2]
    data_sz = index[1].read()
    sz_index["now"] = data_sz.split(",")[3]
    sz_index["lastday"] = data_sz.split(",")[2]
    return sz_index, cyb_index


def get_usa_index_data():
    """
    获取美股行情
    :return:
    """
    nsdk_index = dict()
    dqs_index = dict()
    # 纳斯达克指数
    usa_nsdk = "http://hq.sinajs.cn/list=gb_ixic"
    # 道琼斯指数
    usa_dqs = "http://hq.sinajs.cn/list=gb_dji"
    index = map(urllib2.urlopen, [usa_dqs, usa_nsdk])
    data_dqs = index[0].read()
    dqs_index["idx"] = data_dqs.split(",")[1]
    dqs_index["range"] = data_dqs.split(",")[2]
    data_nsdk = index[1].read()
    nsdk_index["idx"] = data_nsdk.split(",")[1]
    nsdk_index["range"] = data_nsdk.split(",")[2]

    return nsdk_index, dqs_index

def get_a50_index_data():
    """
    获取富时A50行情
    :return:
    """
    a50_index = dict()
    a50 = "http://hq.sinajs.cn/list=hf_CHA50CFD"
    index = urllib2.urlopen(a50).read().split(",")
    a50_index["now"] = index[2]
    a50_index["lastday"] = index[7]
    a50_index["range"] = (float(index[2]) - float(index[7])) / float(index[7])*100
    return a50_index



def get_stock_info(stock):
    """
    获取股票基本面信息
    :param stock:
    :param broser:
    :return:
    """
    driver = driver_init()
    stock_info = dict()
    base_url = "http://search.10jqka.com.cn/stockpick/search?tid=stockpick&qs=stockpick_diag&ts=1&w=%s"%stock
    driver.get(base_url)
    stock_info["stock_pe_active"] = driver.find_element_by_xpath('//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[5]/div/a').text
    stock_info["stock_pe_static"] = driver.find_element_by_xpath('//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[6]/div').text
    stock_info["stock_businiess"] = driver.find_element_by_xpath('//*[@id="dp_block_0"]/div/div/table/tbody/tr/td[3]/div/a').text
    stock_info["stock_concept"] = driver.find_element_by_xpath('//*[@id="dp_block_0"]/div/div/table/tbody/tr/td[6]').text
    stock_info["stock_anaysis"] = driver.find_element_by_xpath('//*[@id="dp_block_65"]/div/div[2]/div[1]/div').text
    stock_info["stock_facm"] = driver.find_element_by_xpath('//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[3]/div').text
    try:
        stock_info["stock_news"] = driver.find_element_by_xpath('//*[@id="dp_block_6"]/div/div[1]').text
        stock_info["affair"] = driver.find_element_by_xpath('//*[@id="dp_block_1"]/div/div[1]/table').text
    except Exception as e:
        stock_info["affair"] = ""
    driver.quit()


    # broser.get(base_url)
    # stock_info['pe'] = broser.find_element_by_xpath('//*[@id="gt6"]').text
    # stock_info['value'] = broser.find_element_by_xpath('//*[@id="gt7"]').text
    # '''流通市值'''
    # stock_info['famc'] = broser.find_element_by_xpath('//*[@id="gt14"]').text
    # stock_info['block1'] = chrome.find_element_by_xpath('//*[@id="zjlxbk"]/tr[1]/td[1]/a').text
    # stock_info['block2'] = chrome.find_element_by_xpath('//*[@id="zjlxbk"]/tr[2]/td[1]/a').text
    # stock_info['block3'] = chrome.find_element_by_xpath('//*[@id="zjlxbk"]/tr[3]/td[1]/a').text
    return stock_info


def driver_init():
    chromedriver = "lib/chromedriver2.36"
    os.environ["webdriver.chrome.driver"] = chromedriver
    option = webdriver.ChromeOptions()
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('headless')
    chrome = webdriver.Chrome(chromedriver, chrome_options=option)
    return chrome



# print get_a50_index_data()
# print get_china_index_data()
# print get_usa_index_data()
# print get_stock_info()["stock_value"]
# print get_stock_info("000526")