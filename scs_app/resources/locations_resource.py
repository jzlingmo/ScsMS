# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()

parser.add_argument('type', type=str)


class LocationsResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        args = parser.parse_args()
        type = args.get('type')
        locations = []
        if type == 'count':

            locations = self.db.query('SELECT location.sid,location.name,count(article.sid) AS count from location ' +
                                      'left JOIN article on location.sid=article.location_sid group by location.sid')
        else:
            locations = self.db.query('select * from location')
        return locations