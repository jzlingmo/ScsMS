# -*- coding: utf-8 -*-
__author__ = 'jz'

from scrapy.exceptions import DropItem

from scs_crawler.utils import color


class NoTitleDrop(DropItem):
    """Product with no title exception"""

    def __init__(self, url="", *args):
        self.url = url
        self.style = color.color_style()
        DropItem.__init__(self, *args)

    def __str__(self):  #####for usage: print e
        print self.style.ERROR("DROP(NoTitleDrop):" + self.url)

        return DropItem.__str__(self)


class CrawledUrlDrop(DropItem):
    def __init__(self, url="", *args):
        self.url = url
        self.style = color.color_style()
        DropItem.__init__(self, *args)

    def __str__(self):  #####for usage: print e
        print self.style.ERROR("DROP(CrawledUrlDrop):" + self.url)
        return DropItem.__str__(self)


class NotContentPageDrop(DropItem):
    def __init__(self, info="", url="", *args):
        self.info = info
        self.url = url
        self.style = color.color_style()
        DropItem.__init__(self, *args)

    def __str__(self):  #####for usage: print e
        print self.style.ERROR("DROP(NotContentPageDrop):" + self.info + '|' + self.url)
        return DropItem.__str__(self)

class KeywordNotFitDrop(DropItem):
    def __init__(self, info="", url="", *args):
        self.info = info
        self.url = url
        self.style = color.color_style()
        DropItem.__init__(self, *args)

    def __str__(self):  #####for usage: print e
        print self.style.ERROR("DROP(KeywordNotFitDrop):" + self.info + '|' + self.url)
        return DropItem.__str__(self)