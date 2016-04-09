# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
parser.add_argument('sid', type=str)

parser.add_argument('keyword', type=str)
parser.add_argument('has', type=str)
parser.add_argument('position', type=str)


class KeywordsResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        args = parser.parse_args()
        keywords = self.db.query('select * from keyword order by sid DESC')
        return keywords

    def post(self):
        args = parser.parse_args()
        fields = []
        params = []
        for k, v in args.items():
            if v is None:
                continue
            fields.append(k)
            params.append(v)

        sid = self.db.insert(
            "insert into keyword(" + ','.join(fields) + ") values (" + ','.join(['%s'] * len(fields)) + ")", params)
        return sid
