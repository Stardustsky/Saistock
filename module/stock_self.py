#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 下午5:44
# @Author  : Stardustsky
# @File    : stock_self.py
# @Software: PyCharm

from spider import get_price_data, get_stock_info, get_stock_data


def mid_stock_basic(stock):
    """
    中线股票基本面分析
    :param stock:
    :return:
    """
    stock_info = get_stock_info(stock)
    try:
        famc = float(stock_info["stock_facm"])
        active_pe = float(stock_info["stock_pe_active"])
        static_pe = float(stock_info["stock_pe_static"])

        if active_pe >= 300 or active_pe < 0:
            active_pe = 300.0
    except Exception:
        print u'[info]股票代码有误或网络错误。'
    stock_basic_score = 1
    stock_basic_info = ""

    # 市值分析
    if famc >= 5000:
        stock_basic_score *= 0.95
        stock_basic_info = u"公司市值巨大，"
    elif 5000 > famc >= 2000:
        stock_basic_score *= 0.96
        stock_basic_info = u"公司市值很大，"
    elif 2000 > famc >= 1000:
        stock_basic_score *= 0.97
        stock_basic_info = u"公司市值较大，"
    elif 1000 > famc >= 500:
        stock_basic_score *= 0.98
        stock_basic_info = u"公司市值略大，"
    elif 500 > famc >= 100:
        stock_basic_score *= 1.02
        stock_basic_info = u"公司市值适中，"
    elif 100 > famc >= 50:
        stock_basic_score *= 0.99
        stock_basic_info = u"公司市值较小，"
    elif 50 > famc >= 10:
        stock_basic_score *= 0.95
        stock_basic_info = u"公司市值很小，"
    elif famc <= 10:
        stock_basic_score *= 0.88
        stock_basic_info = u"公司市值极小，"

    # 市盈率分析
    if active_pe > 150:
        stock_basic_score *= 0.8
        stock_basic_info += u"市盈率>150，"
    elif 150 >= active_pe > 60:
        stock_basic_score *= 0.85
        stock_basic_info += u"市盈率>60，"
    elif 60 >= active_pe > 20:
        stock_basic_score *= 0.9
        stock_basic_info += u"市盈率20~60，"
    elif 20 >= active_pe > 10:
        stock_basic_score *= 1
        stock_basic_info += u"市盈率10~20，"
    elif 10 >= active_pe > 5:
        stock_basic_score *= 1.1
        stock_basic_info += u"市盈率5~10，"
    elif active_pe < 5:
        stock_basic_score *= 1.2
        stock_basic_info += u"市盈率<5，"

    if stock_basic_score >= 1.2:
        stock_basic_info += u"中线投资价值极大"
    elif 1.2 > stock_basic_score >= 1.1:
        stock_basic_info += u"中线投资价值较大"
    elif 1.1 > stock_basic_score >= 1.05:
        stock_basic_info += u"略有中线投资价值"
    elif 1.05 > stock_basic_score >= 0.95:
        stock_basic_info += u"中线投资价值一般"
    elif 0.95 > stock_basic_score >= 0.85:
        stock_basic_info += u"中线投资价值较差"
    elif 0.85 > stock_basic_score:
        stock_basic_info += u"不建议中线投资该股票"
    stock_info['basic_score'] = stock_basic_score
    stock_info['basic_info'] = stock_basic_info

    return stock_info


def short_stock_basic(stock, driver):
    """
    短线股票基本面分析
    :return:
    """
    stock_info = get_stock_info(stock, driver)
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
        stock_basic_score *= 0.91
        stock_basic_info = u"公司市值巨大，"
    elif 5000 > famc >= 2000:
        stock_basic_score *= 0.92
        stock_basic_info = u"公司市值很大，"
    elif 2000 > famc >= 1000:
        stock_basic_score *= 0.95
        stock_basic_info = u"公司市值较大，"
    elif 1000 > famc >= 500:
        stock_basic_score *= 0.98
        stock_basic_info = u"公司市值适中，"
    elif 500 > famc >= 100:
        stock_basic_score *= 1.06
        stock_basic_info = u"公司市值适中，"
    elif 100 > famc >= 50:
        stock_basic_score *= 1.2
        stock_basic_info = u"公司市值较小，"
    elif 50 > famc >= 10:
        stock_basic_score *= 1.1
        stock_basic_info = u"公司市值很小，"
    elif famc <= 10:
        stock_basic_score *= 0.95
        stock_basic_info = u"公司市值极小，"

    # 市盈率分析
    if active_pe > 190:
        stock_basic_score *= 0.93
        stock_basic_info += u"市盈率>190，"
    elif 190 >= active_pe > 150:
        stock_basic_score *= 0.95
        stock_basic_info += u"市盈率150~190，"
    elif 150 >= active_pe > 60:
        stock_basic_score *= 1.02
        stock_basic_info += u"市盈率60~150，"
    elif 60 >= active_pe > 20:
        stock_basic_score *= 1.05
        stock_basic_info += u"市盈率20~60，"
    elif 20 >= active_pe > 10:
        stock_basic_score *= 1.02
        stock_basic_info += u"市盈率10~20，"
    elif 10 >= active_pe > 5:
        stock_basic_score *= 0.98
        stock_basic_info += u"市盈率5~10，"
    elif active_pe < 5:
        stock_basic_score *= 0.95
        stock_basic_info += u"市盈率<5，"

    if stock_basic_score >= 1.2:
        stock_basic_info += u"短线投资基本面较好"
    elif 1.2 > stock_basic_score >= 1.1:
        stock_basic_info += u"短线投资基本面较好"
    elif 1.1 > stock_basic_score >= 1.05:
        stock_basic_info += u"短线投资基本面一般"
    elif 1.05 > stock_basic_score >= 0.95:
        stock_basic_info += u"短线投资基本面一般"
    elif 0.95 > stock_basic_score >= 0.85:
        stock_basic_info += u"短线投资基本面较差"
    elif 0.85 > stock_basic_score:
        stock_basic_info += u"短线投资基本面较差"

    stock_info['basic_score'] = stock_basic_score
    stock_info['basic_info'] = stock_basic_info

    return stock_info


def get_stock_active(stock, stock_type="short"):
    """
    股票活跃度分析
    :return:
    """

    stock_max_price, stock_buttom_price, stock_avarage_price, stock_now_price, stock_active, stock_price_range,stock_nine_change = get_price_data(
        stock)
    # 股票价格位置概况
    stock_long_line = stock_now_price / stock_max_price
    stock_active_info = ""
    stock_long_line_info = ""
    if stock_type == "short":
        if stock_active >= 3.0:
            stock_active_info = u"股票剧烈放量，关注是否形成趋势"
        elif 3.0 > stock_active >= 2.0:
            stock_active_info = u"股票大幅放量，关注是否与市场热点切合，可能形成连续上涨趋势"
        elif 2.0 > stock_active >= 1.5:
            stock_active_info = u"股票小幅放量，关注是否开始形成转折"
        elif 1.5 > stock_active >= 0.85:
            stock_active_info = u"股票量能正常波动，无明显变化"
        elif 0.85 > stock_active >= 0.8:
            stock_active_info = u"股票小幅缩量，存在下跌风险"
        elif 0.8 > stock_active:
            stock_active_info = u"股票大幅缩量，关注是否开始形成转折"
        return stock_active, stock_active_info

    if stock_type == "long":
        if stock_long_line >= 0.95:
            stock_long_line_info = u"股票价格接近100天内最高点，除业绩飙升外不适合长线持有"
        if 0.95 > stock_long_line >= 0.9:
            stock_long_line_info = u"股票价格处于100天内高位，请谨慎投资"
        if 0.9 > stock_long_line >= 0.85:
            stock_long_line_info = u"股票价格较低，可选择行业龙头或优质股持有"
        if 0.85 > stock_long_line >= 0.75:
            stock_long_line_info = u"股票价格接近100天内低位，可关注投资会"
        if 0.75 > stock_long_line >= 0.60:
            stock_long_line_info = u"股票价格极低，可能存在业绩爆雷或行业退坡情况，若非则为极佳投资机会"
        if stock_long_line < 0.6:
            stock_long_line_info = u"股票价格接近腰斩，关注公司是否有重大负面新闻或行业大幅退坡行为"
        return stock_long_line, stock_long_line_info


def nine_change(stock):
    data = get_stock_data(stock)
    nine_change_index = 0
    nine_change_info = "None"
    # print data[-1]['low']
    if (float(data[-1]['low']) < float(data[-3]['low']) and float(data[-1]['low']) < float(data[-4]['low'])) or (float(data[-2]['low']) < float(data[-3]['low']) and float(data[-2]['low']) < float(data[-4]['low'])):
        if float(data[-4]['close']) < float(data[-8]['close']):
            nine_change_info = u"六转买入信号已现，请注意观察"
            nine_change_index = 2
            if float(data[-8]['close']) < float(data[-12]['close']):
                nine_change_index = 2
                nine_change_info = u"八转买入信号已现，请关注是否出现九转"
                if float(data[-9]['close']) < float(data[-13]['close']):
                    nine_change_info = u"九转买入信号已现，请考虑抄底"
                    nine_change_index = 1

    if (float(data[-1]['high']) > float(data[-3]['high']) and float(data[-1]['high']) > float(data[-4]['high'])) or (float(data[-2]['high']) > float(data[-3]['high']) and float(data[-2]['high']) > float(data[-4]['high'])):
        if float(data[-4]['close']) > float(data[-8]['close']):
            nine_change_info = u"六转卖出信号已现，请注意观察"
            nine_change_index = 2
            if float(data[-8]['close']) > float(data[-12]['close']):
                nine_change_info = u"八转卖出信号已现，请注意九转卖出信号"
                nine_change_index = 2
                if float(data[-9]['close']) > float(data[-13]['close']):
                    nine_change_info = u"九转卖出信号已现，请考虑卖出或减小仓位"
                    nine_change_index = -1

    return nine_change_index, nine_change_info



# print stock_active("1000858")[1]
# print stock_active("0600519")[1]
# print stock_active("0600626")[1]
# print get_stock_active("0600624")
# print nine_change("0600624")
