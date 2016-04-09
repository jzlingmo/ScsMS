# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()

parser.add_argument('url', type=str) #
parser.add_argument('pattern', type=str)
parser.add_argument('name', type=str) #
parser.add_argument('type', type=str) #
parser.add_argument('lang', type=str) #
parser.add_argument('visible', type=str)


class SiteResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def put(self, sid):
        args = parser.parse_args()
        dict_row = {k: v for k, v in args.iteritems() if v is not None}
        dict_where = {'sid': sid}
        self.db.update_by_dict('site', dict_row, dict_where)

    def delete(self, sid):
        self.db.execute('delete from site where sid=%s', (sid,))
        return 'delete success'