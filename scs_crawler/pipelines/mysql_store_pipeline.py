# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import datetime
import traceback

import torndb

from scs_app import config
from scs_crawler.utils import color


class MysqlStore(object):
    def __init__(self):
        self.style = color.color_style()

        try:
            self.db = torndb.Connection(host=config.HOST, database=config.DATABASE,
                                        user=config.USER, password=config.PASSWORD)
        except Exception as e:
            print self.style.ERROR("ERROR(StorePipeline): %s" % (str(e),))
            traceback.print_exc()

    def process_item(self, item, spider):
        article = {
            'site_sid': item.get('site_sid', None),
            'title': item.get('title', None),
            'url': item.get('url', None),
            'collect_time': int(time.time() * 1000),
            'content': item.get('content', None),
            'publish_time': item.get('publish_time', None)
        }
        sql_insert = 'insert into article(site_sid,title,url,collect_time,content,publish_time) ' \
                     'values(%s,%s,%s,%s,%s,%s)'
        self.db.insert(sql_insert, article['site_sid'], article['title'], article['url'], article['collect_time'],
                       article['content'], article['publish_time'])
        return item