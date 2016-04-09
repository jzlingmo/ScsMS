# -*- coding: utf-8 -*-

import traceback

import torndb
from scrapy.exceptions import DropItem

from scs_app import config
from scs_crawler.utils import color
from scs_crawler.pipelines.article_drops import CrawledUrlDrop


class DropCrawledUrl(object):
    crawled_urls = {}

    def __init__(self):
        self.style = color.color_style()
        # 初始化urls
        try:
            db = self.db = torndb.Connection(host=config.HOST, database=config.DATABASE,
                                             user=config.USER, password=config.PASSWORD)
            result = db.query('select url from article')
            self.crawled_urls = {k['url']: 0 for k in result}
        except Exception as e:
            print self.style.ERROR("ERROR(DropCrawledUrl): %s" % (str(e),))
            traceback.print_exc()

    def process_item(self, item, spider):
        url = item.get('url')
        if url in self.crawled_urls:
            raise CrawledUrlDrop(item['url']).__str__()
        else:
            # 添加新的url
            self.crawled_urls[url] = 0
        return item
