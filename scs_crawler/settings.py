# -*- coding: utf-8 -*-
# Scrapy settings for scs_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scs_crawler'

SPIDER_MODULES = ['scs_crawler.spiders']
NEWSPIDER_MODULE = 'scs_crawler.spiders'

# ITEM_PIPELINES = ['scs_crawler.pipelines.StorePipeline']
DOWNLOAD_DELAY = 0.5  # 250 ms of delay
RANDOMIZE_DOWNLOAD_DELAY = True

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}

#宽度优先爬取
SCHEDULER_ORDER = 'BFO'
DEPTH_LIMIT = 0  # 爬取深度限制
DEPTH_PRIORITY = 2  # 爬取深度的优先级

DOWNLOAD_TIMEOUT = 30  # 网页下载超时时间 默认180 seconds

#GOOGLE_CACHE_DOMAINS = ['www.woaidu.org',]

#all below configs are to avoid getting banned
#To make RotateUserAgentMiddleware enable.
USER_AGENT = ''
COOKIES_ENABLED = False
# DOWNLOAD_DELAY = 2 # 2s of delay

DOWNLOADER_MIDDLEWARES = {
    #    'scs_crawler.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':50,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scs_crawler.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    #    'scs_crawler.pipelines.bookfile.WoaiduBookFile',
    #    'scs_crawler.pipelines.drop_none_download.DropNoneBookFile',

    'scs_crawler.pipelines.drop_crawled_url_pipeline.DropCrawledUrl': 100,
    'scs_crawler.pipelines.parse_item_pipeline.ParseItem': 200,
    'scs_crawler.pipelines.keyword_pipeline.Keyword': 300,
    'scs_crawler.pipelines.mysql_store_pipeline.MysqlStore': 400,
    'scs_crawler.pipelines.final_test_pipeline.FinalTest': 900,
}

LOG_FILE = 'scs_crawler.log'

# LOG_ENABLED = True
# LOG_ENCODING = 'utf-8'
# LOG_FILE = '/home/xxx/services_runenv/crawlers/proxy/proxy/log/proxy.log'
# LOG_LEVEL = 'DEBUG'
# LOG_STDOUT = False

# STATS_CLASS = 'scs_crawler.statscol.graphite.GraphiteStatsCollector'

GRAPHITE_HOST = '127.0.0.1'
GRAPHITE_PORT = 1002
GRAPHITE_IGNOREKEYS = []