#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-09-09 16:15
# @Author  : Stardustsky
# @File    : stock_market.py
# @Software: PyCharm

from spider import get_usa_index_data,get_a50_index_data,get_china_index_data,get_money_flow,get_usa_futures_index



def external_index():
    """
    外围市场指数分析
    :return:
    """
    usa_stock_index = 1.0
    usa_stock_info = ""
    nsdk_index, dqs_index = get_usa_index_data()
    nsdk_range = float(nsdk_index['range'].encode("utf-8").replace("%", ""))
    dqs_range = float(dqs_index['range'].encode("utf-8").replace("%", ""))

    if nsdk_range <= -4.0 or dqs_range <= -4.0:
        usa_stock_index /= 5
        usa_stock_info = u"美股暴跌，恐带来全球性金融风险，请勿参与股市"
    elif -4.0 < nsdk_range <= -3.0 or -4.0 < dqs_range <= -3.0:
        usa_stock_index /= 3.0
        usa_stock_info = u"美股暴跌，恐带来全球股市同步暴跌，请及时清仓"
    elif -2.5 < nsdk_range <= -2.0 or -2.5 < dqs_range <= -2.0:
        usa_stock_index /= 1.3
        usa_stock_info = u"美股大跌，可能导致A股市场恐慌大跌，请及时清仓或降低仓位"
    elif -2.0 < nsdk_range <= -1.0 or -2.0 <= dqs_range <= -1.0:
        usa_stock_index /= 1.1
        usa_stock_info = u"美股微跌，对A股影响有限，可正常参与股票交易或微减仓"
    elif nsdk_range >= 2.0 or dqs_range >= 2.0:
        usa_stock_index *= 1.1
        usa_stock_info = u"美股大涨，外围市场情绪较好，可正常参与股市交易"
    elif 1.0 > nsdk_range >= -1.0 or 1.0 > dqs_range >= -1.0:
        usa_stock_index *= 1.0
        usa_stock_info = u"美股正常区间波动，对A股未造成影响，可正常参与股市交易"

    return usa_stock_index, usa_stock_info


def internal_index():
    """
    国内股市指数分析
    :return:
    """
    sz_index, cyb_index = get_china_index_data()
    sz_score = float(sz_index['now'])
    cyb_score = float(cyb_index['now'])
    cn_plate_score = 1
    cn_plate_info = ""
    if sz_score < 2500:
        cn_plate_score *= 1.5
        cn_plate_info = u"大盘估值已接近历史底部，可大量布局"
    elif 2500 <= sz_score < 2700:
        cn_plate_score *= 1.3
        cn_plate_info = u"大盘估值严重低于市场均值，可布局优质蓝筹"
    elif 2700 <= sz_score < 3000:
        cn_plate_score *= 1.2
        cn_plate_info = u"大盘估值已接近历史底部，可大量布局"
    elif 3000 < sz_score < 3700:
        cn_plate_score *= 1.0
        cn_plate_info = u"大盘估值位于中部区域，可适当参与股票交易"
    elif 3700 <= sz_score < 4800:
        cn_plate_score *= 1.3
        cn_plate_info = u"大盘估值显示出牛市特征，可适当参与股票交易"
    elif 4800 <= sz_score < 5000:
        cn_plate_score *= 1.1
        cn_plate_info = u"大盘估值较高，轻仓或不参与股票交易"
    elif 5000 <= sz_score < 6000:
        cn_plate_score *= 0.7
        cn_plate_info = u"大盘估值过高，下跌风险较大，可清仓投资其它理财产品"
    elif 6000 <= sz_score:
        cn_plate_score *= 0.5
        cn_plate_info = u"大盘估值已超过历史最高位，有暴跌风险，及时撤资"
    # print china_sz_index
    return cn_plate_score, cn_plate_info


def a50_index():
    """
    A50指数分析
    :return:
    """
    cn_a50_index = get_a50_index_data()
    cn_a50_range = float(cn_a50_index['range'])
    cn_a50_score = 1.0
    cn_a50_info=""
    if cn_a50_range >= 2.0:
        cn_a50_score *= 1.5
        cn_a50_info = u"A50指数暴涨，市场情绪极好，请积极参与"
    elif 2.0 > cn_a50_range >= 1.0:
        cn_a50_score *= 1.4
        cn_a50_info = u"A50指数大涨，市场情绪较好，请积极参与"
    elif 1.0 > cn_a50_range >= 0.4:
        cn_a50_score *= 1.2
        cn_a50_info = u"A50指数微涨，股市上涨概率较大，可参与交易"
    elif 0.4 > cn_a50_range >= -0.4:
        cn_a50_score *= 1.0
        cn_a50_info = u"A50指数正常波动，对市场影响较小，可参与交易"
    elif -0.4 > cn_a50_range >= -1.0:
        cn_a50_score *= 0.85
        cn_a50_info = u"A50指数下跌，可能对市场情绪有一定影响，建议进行减仓"
    elif -1.0 > cn_a50_range >= -2.0:
        cn_a50_score *= 0.8
        cn_a50_info = u"A50指数大跌，市场情绪较差，建议找机会减仓或清仓"
    elif -2.0 > cn_a50_range:
        cn_a50_score *= 0.6
        cn_a50_info = u"A50指数大跌，市场情绪极差，非确定性股票请及时清仓止损"
    return cn_a50_score, cn_a50_info


def market_emotion_index(idx_type="short"):
    """
    市场整体情绪分析
    :param idx_type:
    :return:
    """
    cn_idx, cn_info = internal_index()
    usa_idx, usa_info = external_index()
    a50_idx, a50_info = a50_index()
    if idx_type == 'short':
        market_score = usa_idx * 0.3 + a50_idx * 0.7
        if market_score >= 1.2:
            market_info = u"市场情绪极好，可积极参与股市"
        elif 1.2 > market_score >= 1.1:
            market_info = u"市场情绪很好，可积极参与股市"
        elif 1.1 > market_score >= 1.05:
            market_info = u"市场有所上涨，情绪较好，可选择强势股票交易"
        elif 1.05 > market_score >= 0.95:
            market_info = u"市场情绪一般，较为平淡，可选择性参与"
        elif 0.95 > market_score >= 0.9:
            market_info = u"市场有所下跌，可能存在下行风险，建议减仓"
        elif 0.9 > market_score >= 0.85:
            market_info = u"市场情绪较差，指数面临下调风险"
        elif 0.85 > market_score >= 0.8:
            market_info = u"市场情绪极差，指数面临大跌风险"
        elif 0.8 > market_score:
            market_info = u"及时清仓逃避大跌"

        return market_score, [market_info, usa_info, a50_info]


def market_money():
    """
    北向资金分析
    :return:
    """
    money_flow = get_money_flow()
    money_flow_dict = dict()
    money_flow_info = ""
    bx = int(money_flow['hk2sz']) + int(money_flow['hk2sh'])
    nx = int(money_flow['sz2hk']) + int(money_flow['sh2hk'])
    if bx > 500000:
        money_flow_info = u"北向资金大幅流入，市场大概率迎来大涨"
    if 500000 > bx >= 200000:
        money_flow_info = u"北向资金流入较多，市场大概率迎来上涨"
    if 200000 > bx >= 100000:
        money_flow_info = u"北向资金少量流入，市场可能震荡微涨"
    if 100000 > bx >= -100000:
        money_flow_info = u"北向资金正常波动，市场正常震荡"
    if -100000 > bx >= -200000:
        money_flow_info = u"北向资金呈流出状态，市场可能迎来下跌"
    if -200000 > bx >= -450000:
        money_flow_info = u"北向资金流出较多，市场可能迎来大跌"
    if -450000 > bx:
        money_flow_info = u"北向资金大幅流出，市场可能迎来暴跌"
    money_flow_dict['bx'] = bx
    money_flow_dict['nx'] = nx
    money_flow_dict['info'] = money_flow_info
    return money_flow_dict


def usa_futures():
    """
    美股期指
    :return:
    """
    usa_futures = get_usa_futures_index()

# print market_emotion_index()[0]
# print market_emotion_index()[1][0]
# print market_emotion_index()[1][1]
# print market_emotion_index()[1][2]
# market_money()
