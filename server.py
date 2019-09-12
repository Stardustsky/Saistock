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
from module.core import news_status,market_status,plate_status,stock_status


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        market_score, market_info = market_status()
        hot_stock_list, hot_concept_dict = plate_status()
        try:
            stock = str(self.get_argument("stock"))
            select_type = str(self.get_argument("select_type"))
            sub = self.get_argument("sub")
            if sub:
                stock_info = stock_status(stock, stock_type=select_type)
                self.render("index.html",
                            market=[market_score, market_info],
                            market_hot=[hot_stock_list, hot_concept_dict],
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
            self.render("index.html",
                        market=[market_score, market_info],
                        market_hot=[hot_stock_list, hot_concept_dict],
                        stock_self=stock_info,
                        stock_code=u"None"
                        )






    def post(self):
        payload = self.request
        print payload
        try:
            pass

        except Exception as e:
            self.render("index.html", outsql="", postsql="输入异常")

        self.render("index.html", outsql="", postsql="")



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
    port = 2222
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()