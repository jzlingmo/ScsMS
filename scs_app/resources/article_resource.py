# -*- coding: utf-8 -*-
__author__ = 'jz'

import string
import re

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *
from scs_app.service.article_service import ArticleService

parser = reqparse.RequestParser()
parser.add_argument('processed', type=int)
parser.add_argument('abstract', type=str)
parser.add_argument('keywords', type=str)


class ArticleResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()
        self.service = ArticleService()

    def get(self, article_id):
        article = self.service.get_article_by_sid(article_id)
        # 正文转义
        article['content'] = '<p>' + article['content']
        article['content'] = string.replace(article['content'], '\n', '<p>')
        article['content'] = re.sub(u"""\u3000{4}""", '<p>', article['content'])
        article['content'] = re.sub(u"""\u3000{2}""", '<p>', article['content'])
        article['content'] = re.sub(u"""\u00a0{2,}""", '<p>', article['content'])
        return article

    def put(self, article_id):
        row_dict = parser.parse_args()
        # 去除parse后不匹配的argument
        row_dict = {k: v for k, v in row_dict.iteritems() if v is not None}
        update_count = self.service.update_article_by_id(article_id, row_dict)
        return update_count

    def delete(self, article_id):
        delete_count = self.service.delete_article_by_id(article_id)
        return delete_count