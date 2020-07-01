#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 下午2:17
# @Author  : Stardustsky
# @File    : test_server.py
# @Software: PyCharm
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import urllib
import HTMLParser
import json
from module.core import news_status,market_status,plate_status,stock_status,core_func
from module.stock_notice import *
from module.func import *


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        driver = driver_init()
        market_score, market_info, money_flow, hot_info = core_func(driver)
        driver.quit()
        try:
            stock = str(self.get_argument("stock"))
            select_type = str(self.get_argument("select_type"))
            sub = self.get_argument("sub")
            if sub:
                driver = driver_init()
                stock_info = stock_status(stock, driver, stock_type=select_type)
                driver.quit()
                self.render("index.html",
                            market=[market_score, market_info],
                            money=money_flow,
                            market_hot=hot_info,
                            stock_self=stock_info,
                            stock_code=stock
                            )
        except:
            print u'获取个股信息失败.'
            stock_info = dict()
            stock_info['basic_score'] = "None"
            stock_info['basic_info'] = "None"
            stock_info['stock_analysis'] = "None"
            stock_info['active_score'] = "None"
            stock_info['active_info'] = "None"
            stock_info['stock_businiess'] = "None"
            stock_info['stock_concept'] = "None"
            stock_info['stock_news'] = "None"
            stock_info['affair'] = "None"
            stock_info['nine_change_index'] = "0"
            stock_info['nine_change_info'] = "None"
            self.render("index.html",
                        market=[market_score, market_info],
                        money=money_flow,
                        market_hot=hot_info,
                        stock_self=stock_info,
                        stock_code=u"None"
                        )






    def post(self):
        mails = ['crimson_he@163.com', 'zer0forpentest@126.com']
        res = nine_change_notice(mails)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
        ]

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/"
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    port = 3333
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()