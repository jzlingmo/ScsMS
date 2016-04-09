# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
parser.add_argument('count', type=str)


class MulActionResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def post(self, type):
        args = parser.parse_args()
        count = args.get('count')
        sids = []
        if type == 'extract':
            # todo multi extract
            pass
        elif type == 'location':
            articles = self.db.query(
                "select article.sid,title,content from article left join site on article.site_sid=site.sid"
                " where lang='cn' and location_sid IS NULL LIMIT 0," + count)
            locations = self.db.query('select sid,name,data from location where name!=%s', (u'其它',))
            other_sid = self.db.get('select sid from location where name=%s', (u'其它',))['sid']
            for article in articles:
                sids.append(article['sid'])
                content = article['title'] + article['content']
                lc = False
                for location in locations:
                    sid = location['sid']
                    words = [location['name']]
                    if location['data']:
                        words += location['data'].split('|')
                    for word in words:
                        if word in content:
                            lc = True
                            self.db.update('update article set location_sid=%s where sid=%s', (sid, article['sid']))
                            break
                    if lc:
                        break
                if not lc:
                    self.db.update('update article set location_sid=%s where sid=%s', (other_sid, article['sid']))
            return {
                'count': count,
                'sids': sids
            }
        else:
            return 'no such command', 404