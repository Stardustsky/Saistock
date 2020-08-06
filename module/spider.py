#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 下午3:16
# @Author  : Stardustsky
# @File    : spider.py
# @Software: PyCharm

import urllib2
import os
import pandas as pd
import datetime
import sys
import json
import cookielib
from selenium import webdriver
from os import path


# ========================================指数类宏观数据抓取函数===================================================
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


def get_usa_futures_index(driver):
    """
    获取道琼斯30、标普500期货指数
    :return:
    """
    usa_futures = dict()
    futures_url = "https://cn.investing.com/indices/us-30-futures"
    driver.get(futures_url)
    usa_futures['dqs'] = float(driver.find_element_by_xpath('//*[@id="sb_changepc_8873"]').text[:-1])
    usa_futures['bp'] = float(driver.find_element_by_xpath('//*[@id="sb_changepc_8839"]').text[:-1])
    return usa_futures


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
    a50_index["range"] = (float(index[2]) - float(index[7])) / float(index[7]) * 100
    return a50_index


# ========================================个股数据抓取函数===================================================
def get_price_data(stock, t_length=-100):
    """
    获取股票100日内最高价/最低价/平均价/现价/10日涨跌幅/股票活跃度
    :param stock:
    :param t_length:
    :return:
    """
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    old_time = (datetime.datetime.now() + datetime.timedelta(days=t_length)).strftime('%Y%m%d')
    wy_api = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER" % (
    stock, old_time, now_time)
    response = urllib2.urlopen(wy_api)
    data = response.read()
    if len(data) > 100:
        data = data.replace('\'', '')
        data = data.decode('gbk').encode('utf-8')
        obj = open("module/data/%s.csv" % stock, "w")
        obj.write(data)
        obj.close()
        df = pd.read_csv("module/data/%s.csv" % stock)
    else:
        print u"[info]输入股票代码有误，请核对后重新输入"
    df = df[(True ^ df['成交量'].isin([0]))]

    stock_avarage_price = df['收盘价'].mean()
    stock_max_price = df['收盘价'].max()
    stock_buttom_price = df['收盘价'].min()
    stock_now_price = df['收盘价'][1]
    stock_price_range = df['涨跌幅'][0:10]
    stock_100_volume = df['成交量'][0:50].mean()
    stock_3_volume = df['成交量'][0:3].mean()
    stock_active = stock_3_volume / stock_100_volume
    stock_nine_change = df[0:13]
    return stock_max_price, stock_buttom_price, stock_avarage_price, stock_now_price, stock_active, stock_price_range, stock_nine_change
    # except:
    #     print u"[info]输入股票代码有误，请核对后重新输入"


def get_stock_info(stock, driver):
    """
    获取股票基本面信息
    :param stock:
    :param broser:
    :return:
    """
    # driver = driver_init()
    stock_info = dict()
    base_url = "http://search.10jqka.com.cn/stockpick/search?tid=stockpick&qs=stockpick_diag&ts=1&w=%s" % stock
    driver.get(base_url)
    # 动态市盈率
    stock_info["stock_pe_active"] = driver.find_element_by_xpath(
        '//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[5]/div/a').text
    # 静态市盈率
    stock_info["stock_pe_static"] = driver.find_element_by_xpath(
        '//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[6]/div').text
    # 公司经营
    stock_info["stock_businiess"] = driver.find_element_by_xpath(
        '//*[@id="dp_block_0"]/div/div/table/tbody/tr/td[3]/div/a').text
    # 公司概念
    stock_info["stock_concept"] = driver.find_element_by_xpath(
        '//*[@id="dp_block_0"]/div/div/table/tbody/tr/td[6]').text
    # 同花顺分析结果
    stock_info["stock_analysis"] = driver.find_element_by_xpath('//*[@id="dp_block_65"]/div/div[2]/div[1]/div').text
    # 公司市值
    stock_info["stock_facm"] = driver.find_element_by_xpath(
        '//*[@id="dp_tablemore_3"]/div/div/div/div/table/tbody/tr/td[3]/div').text
    try:
        # 公司新闻
        stock_info["stock_news"] = driver.find_element_by_xpath('//*[@id="dp_block_6"]/div/div[1]').text
        # 公司重大事项
        stock_info["affair"] = driver.find_element_by_xpath('//*[@id="dp_block_1"]/div/div[1]/table').text
    except Exception as e:
        stock_info["stock_news"] = "None"
        stock_info["affair"] = "None"
    # driver.quit()

    return stock_info


def get_stock_data(stock):
    """
    获取股票价格信息
    :param stock:
    :return:
    """
    # now_time = datetime.datetime.now().strftime('%Y%m%d')
    # old_time = (datetime.datetime.now() + datetime.timedelta(days=t_length)).strftime('%Y%m%d')
    # print stock[1]
    if stock[0] == "0":
        stock = "sh"+stock[1:]
    else:
        stock = "sz"+stock[1:]
    wy_api = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=240&ma=no&datalen=20" %stock
    print wy_api
    response = urllib2.urlopen(wy_api)
    data = response.read()
    data = json.loads(data)
    return data


# ========================================板块、热门、研报等分析数据抓取函数============================================
def get_hot_plate(driver):
    """
    获取热门股票以及板块信息
    :return:
    """
    # driver = driver_init()
    try:
        # 获取热点股票列表
        hot_stock_list = list()
        base_url = "http://search.10jqka.com.cn/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E7%83%AD%E7%82%B9%E5%89%8D20%E6%8C%89%E6%B6%A8%E5%B9%85%E6%8E%92%E5%88%97&queryarea="
        driver.get(base_url)
        hot_stock = driver.find_element_by_xpath('//*[@id="tableWrap"]/div[2]/div/div[2]/div/table').text
        data = hot_stock.split("\n")
        for i in range(len(data) / 3):
            hot_stock_list.append(data[i * 3 + 2])

        # 获取热门概念及原因
        hot_concept_dict = dict()
        base_url = "http://search.10jqka.com.cn/stockpick?qs=return_stock"
        driver.get(base_url)
        hot_concept = driver.find_element_by_xpath('//*[@id="hltj_right_hc_query_li_st"]/ul').text
        data = hot_concept.split("\n")
        for i in range(len(data) / 3):
            hot_concept_dict[(data[i * 3 + 1])] = data[i * 3 + 2]
        return hot_stock_list, hot_concept_dict
    except Exception as e:
        print "[info]抓取信息失败."
        return [], []

    # driver.quit()



def get_money_flow():
    """
    抓取南北向资金流动情况,主要以北向资金为准
    :return:
    """
    money_flow = dict()
    url = "http://push2.eastmoney.com/api/qt/kamt/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54"
    response = urllib2.urlopen(url).read()
    money = json.loads(response)['data']
    # 北向资金流向
    money_flow['hk2sz'] = money['hk2sz']['dayNetAmtIn']
    money_flow['hk2sh'] = money['hk2sh']['dayNetAmtIn']
    # 南向资金流向
    money_flow['sz2hk'] = money['sz2hk']['dayNetAmtIn']
    money_flow['sh2hk'] = money['sh2hk']['dayNetAmtIn']

    return money_flow


def get_gb_report():
    """
    研报社短线情绪分析
    :return:
    """
    report_api = "http://admin.gbhome.com/api/v4/common/3in1/discovery?pageNum=1&pageSize=6&keyword="
    response = urllib2.urlopen(report_api)
    data = json.loads(response.read())["data"]["records"]
    return data[1:]


def get_gb_yb():
    art_content = dict()
    yb_api = "http://admin.gbhome.com//api/v4/common/3in1/zlContent?pageNum=1&pageSize=5&zlId=1000003"
    yb_content = "http://admin.gbhome.com/api/common/zlArticle/detail/"
    header = {"Authorization":"Bearer eyJhbGciOiJIUzUxMiJ9.eyJ3eFVzZXJJZCI6MTAzNzEyNywic3ViIjoiMTAzNzEyNyIsIm1vYmlsZVBob25lIjoiMTgyMDI4MjMxMzYiLCJjaGFubmVsIjoiQW5kcm9pZCIsImV4cCI6MTU5NzU0NDM1NywiaWF0IjoxNTk0OTUyMzU3fQ.Bu6GiGLrxtCWfZEVZPcVUUDLodEWC4kpeRTXnNoR_YkSddOJCEpb9G0NgC3yXc9r6TWxjUH5wykgNtXSYJbdDQ"}
    response = urllib2.urlopen(yb_api)
    data = json.loads(response.read())["data"]["records"]
    for i in data:
        zid = i["id"].replace("zlArticle", "")
        title = i["title"]
        c_url = yb_content + zid
        req = urllib2.Request(c_url, headers=header)
        res = urllib2.urlopen(req).read()
        art_content[title] = json.loads(res)["data"]["zlArticle"]["detail"]
    return art_content

def get_research_report():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    old_time = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    report_api = "http://reportapi.eastmoney.com/report/list?cb=datatable4702022&industryCode=*&pageSize=20&industry=*&rating=*&ratingChange=0&beginTime=%s&endTime=%s&pageNo=1&fields=&qType=0&orgCode=&code=*&rcode=&_=1573441834847"%(old_time,now_time)
    report_dict = dict()
    response = urllib2.urlopen(report_api)
    data = response.read()
    data = str.replace(data,"datatable4702022(", "")
    data = str.replace(data, ")", "")
    data = json.loads(data)["data"]
    for i in data:
        info = i["publishDate"] + " [" + i["stockName"] + "] " + i["title"]+" - "+i["orgSName"]
        report_dict[i["encodeUrl"]] = info
    return report_dict


# ========================================其它数据抓取函数============================================



# print get_gb_yb()
# print get_gb_report()

# print get_a50_index_data()
# print get_china_index_data()
# print get_usa_index_data()
# print get_stock_info()["stock_value"]
# print get_stock_info("600155")
# print get_hot_plate()
# get_money_flow()

# get_stock_data("002466")
# print get_research_report()
# get_usa_futures_index()
