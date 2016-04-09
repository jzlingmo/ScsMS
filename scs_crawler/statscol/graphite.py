#!/usr/bin/python
#-*-coding:utf-8-*-

from scrapy import log
from socket import socket
from time import time
from scs_crawler.utils import color
from scrapy.statscol import StatsCollector



class GraphiteClient(object):
    """
        The client thats send data to graphite.
        
        Can have some ideas from /opt/graphite/examples/example-client.py
    """

    def __init__(self, host="127.0.0.1", port=2000):
        self.style = color.color_style()
        self._sock = socket()
        self._sock.connect((host, port))

    def send(self, metric, value, timestamp=None):
        try:
            self._sock.send("%s %g %s\n\n" % (metric, value, timestamp or int(time())))
        except Exception as err:
            self.style.ERROR("SocketError(GraphiteClient): " + str(err))


class GraphiteStatsCollector(StatsCollector):
    """
        send the stats data to graphite.
        
        The idea is from Julien Duponchelle,The url:https://github.com/noplay/scrapy-graphite
        
        How to use this:
            1.install graphite and configure it.For more infomation about graphite you can visit
        http://graphite.readthedocs.org/en/0.9.10/ and http://graphite.wikidot.com.
            2.edit /opt/graphite/webapp/content/js/composer_widgets.js,locate the ‘interval’
        variable inside toggleAutoRefresh function,Change its value from ’60′ to ’1′.
            3.add this in storage-aggregation.conf:
                [scrapy_min]
                pattern = ^scrapy\..*_min$
                xFilesFactor = 0.1
                aggregationMethod = min

                [scrapy_max]
                pattern = ^scrapy\..*_max$
                xFilesFactor = 0.1
                aggregationMethod = max

                [scrapy_sum]
                pattern = ^scrapy\..*_count$
                xFilesFactor = 0.1
                aggregationMethod = sum
            4.in settings set:
                STATS_CLASS = 'scrapygraphite.GraphiteStatsCollector'
                GRAPHITE_HOST = '127.0.0.1'
                GRAPHITE_PORT = 2003
                
        The screenshot in woaidu_crawler/screenshots/graphite
    """

    GRAPHITE_HOST = '127.0.0.1'
    GRAPHITE_PORT = 2000
    GRAPHITE_IGNOREKEYS = []#to ignore it,prevent to send data to graphite

    def __init__(self, crawler):
        super(GraphiteStatsCollector, self).__init__(crawler)

        host = crawler.settings.get("GRAPHITE_HOST", self.GRAPHITE_HOST)
        port = crawler.settings.get("GRAPHITE_PORT", self.GRAPHITE_PORT)
        self.ignore_keys = crawler.settings.get("GRAPHITE_IGNOREKEYS", self.GRAPHITE_IGNOREKEYS)
        self._graphiteclient = GraphiteClient(host, port)

    def _get_stats_key(self, spider, key):
        if spider is not None:
            return "scrapy.spider.%s.%s" % (spider.name, key)
        return "scrapy.%s" % (key)

    def set_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).set_value(key, value, spider)
        self._set_value(key, value, spider)

    def _set_value(self, key, value, spider):
        if isinstance(value, (int, float)) and key not in self.ignore_keys:
            k = self._get_stats_key(spider, key)
            self._graphiteclient.send(k, value)

    def inc_value(self, key, count=1, start=0, spider=None):
        super(GraphiteStatsCollector, self).inc_value(key, count, start, spider)
        self._graphiteclient.send(self._get_stats_key(spider, key), self.get_value(key))

    def max_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).max_value(key, value, spider)
        self._graphiteclient.send(self._get_stats_key(spider, key), self.get_value(key))

    def min_value(self, key, value, spider=None):
        super(GraphiteStatsCollector, self).min_value(key, value, spider)
        self._graphiteclient.send(self._get_stats_key(spider, key), self.get_value(key))

    def set_stats(self, stats, spider=None):
        super(GraphiteStatsCollector, self).set_stats(stats, spider)
        for key in stats:
            self._set_value(key, stats[key], spider)