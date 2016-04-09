# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
parser.add_argument('sid', type=str)

parser.add_argument('url', type=str) #
parser.add_argument('pattern', type=str)
parser.add_argument('name', type=str) #
parser.add_argument('type', type=str) #
parser.add_argument('lang', type=str) #
parser.add_argument('visible', type=str)


class SitesResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        sites = self.db.query('select * from site order by sid DESC')
        return sites

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
            "insert into site(" + ','.join(fields) + ") values (" + ','.join(['%s'] * len(fields)) + ")", params)
        return sid