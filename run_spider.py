__author__ = 'jz'


from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from scrapy.utils.project import get_project_settings

from scs_crawler.spiders.scs_spider import ScsSpider


def setup_crawler():
    spider = ScsSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

setup_crawler()
log.start()
reactor.run()