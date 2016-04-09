# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()

parser.add_argument('sid', type=str)
parser.add_argument('start_time', type=str)
parser.add_argument('interval', type=str)


class SpiderResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        spider = self.db.get('select * from spider limit 0,1')
        return spider

    def post(self):
        args = parser.parse_args()
        sid = args.get('sid')
        if not sid:
            return 'spider not exist', 404
        dict_row = {k: v for k, v in args.iteritems() if v is not None}
        self.db.update_by_dict('spider', dict_row, {'sid': sid})
