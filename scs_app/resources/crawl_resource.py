# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
parser.add_argument('type', type=str)

#进行爬虫的启动和停止
class CrawlResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        args = parser.parse_args()
        return