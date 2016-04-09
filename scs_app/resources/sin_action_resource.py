# -*- coding: utf-8 -*-
__author__ = 'jz'

import re

from flask.ext import restful
from flask.ext.restful import reqparse
from snownlp import SnowNLP

from scs_app.db_connect import *


parser = reqparse.RequestParser()
parser.add_argument('sid', type=str)


class SinActionResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self, article_sid, type):
        args = parser.parse_args()
        if type == 'extract':
            article = self.db.get('select title,content from article where sid=%s', (article_sid,))
            s = SnowNLP(article['content'])
            keywords = s.keywords()
            abstract = s.summary()
            keywords = ','.join(keywords)
            abstract = ','.join(abstract)
            self.db.update('update article set keywords=%s,abstract=%s,processed=1 where sid=%s',
                           (keywords, abstract, article_sid))
            return {
                'sid': article_sid,
                'keywords': keywords,
                'abstract': abstract
            }
