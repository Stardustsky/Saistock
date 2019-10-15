#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 下午5:49
# @Author  : Stardustsky
# @File    : func.py
# @Software: PyCharm
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def read_stock_conf():
    stock_no = dict()
    config = ConfigParser.ConfigParser()
    config.readfp(open("common/stock.ini"), "rb")
    code = config.items("stock_code")
    return code


def stock_email(recv,mess):
    """
    邮件提醒功能
    :param stockName:
    :return:
    """
    # 第三方 SMTP 服务
    mail_host = "smtp.sina.com"  # 设置服务器
    mail_user = "sai_stock@sina.com"  # 用户名
    mail_pass = "e763eedb6a5d7c3b"  # 口令
    sender = 'sai_stock@sina.com'
    receiver = recv
    message = MIMEText(mess, _charset='utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver, 'utf-8')
    subject = "股票提醒"
    try:
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
# aa = read_stock_conf()
# print len(aa)
# print aa[0]

# stock_email("天齐锂业")
# print read_stock_conf()