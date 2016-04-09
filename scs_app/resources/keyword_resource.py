# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()

parser.add_argument('keyword', type=str)
parser.add_argument('has', type=str)
parser.add_argument('position', type=str)


class KeywordResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def put(self, sid):
        args = parser.parse_args()
        dict_row = {k: v for k, v in args.iteritems() if v is not None}
        dict_where = {'sid': sid}
        self.db.update_by_dict('keyword', dict_row, dict_where)

    def delete(self, sid):
        self.db.execute('delete from keyword where sid=%s', (sid,))
        return 'delete success'
