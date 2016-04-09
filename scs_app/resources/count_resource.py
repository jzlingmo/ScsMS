# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
parser.add_argument('type', type=str)
parser.add_argument('lang', type=str)


class CountResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        args = parser.parse_args()
        type = args.get('type')
        count = 0
        if type == 'all':
            rs = self.db.query('select count(*) as count from article')
            count = rs[0]['count']
        elif type == 'processed':
            rs = self.db.query('select count(*) as count from article where processed=1')
            count = rs[0]['count']

        elif type == 'supported_lc':
            rs = self.db.query("select count(*) as count from article left join site on article.site_sid=site.sid where lang='cn'")
            count = rs[0]['count']
        elif type == 'has_lc':
            rs = self.db.query('select count(*) as count from article where location_sid is not NULL')
            count = rs[0]['count']
        return count