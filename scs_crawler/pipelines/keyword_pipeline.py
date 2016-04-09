# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import time
import datetime
import traceback

import torndb

from scs_crawler.pipelines.article_drops import KeywordNotFitDrop
from scs_app import config
from scs_crawler.utils import color


class Keyword(object):
    def __init__(self):
        self.style = color.color_style()
        #1标题 2正文 {'keyword':1}
        self.has_keyword = {}
        self.no_keyword = {}

        try:
            self.db = torndb.Connection(host=config.HOST, database=config.DATABASE,
                                        user=config.USER, password=config.PASSWORD)
            # 初始化关键字
            rs = self.db.query('select * from key_conf')
            for one in rs:
                if one['has'] == 1:
                    self.has_keyword[one['keyword']] = one['position']
                elif one['has'] == 0:
                    self.no_keyword[one['keyword']] = one['position']
            print(self.has_keyword)
            print(self.no_keyword)
        except Exception as e:
            print self.style.ERROR("ERROR(StorePipeline): %s" % (str(e),))
            traceback.print_exc()

    def process_item(self, item, spider):
        title = item.get('title', None)
        content = item.get('content', None)
        url = item.get('url', None)
        # # 临时用于匹配国防部
        # if True:
        #     if re.search('weapon', title + content, re.IGNORECASE):
        #         return item
        #     else:
        #         raise KeywordNotFitDrop(info='keyword weaponry not fit', url=url)

        # 匹配关键字
        for (k, v) in self.no_keyword.items():
            if v == 1 and k in title:
                raise KeywordNotFitDrop(info='keyword not fit', url=url)
            if v == 2 and k in content:
                raise KeywordNotFitDrop(info='keyword not fit', url=url)

        # 一旦匹配进入下一pipeline
        for (k, v) in self.has_keyword.items():
            if v == 1 and k in title:
                return item
            if v == 2 and k in content:
                return item

        raise KeywordNotFitDrop(info='keyword not fit', url=url)