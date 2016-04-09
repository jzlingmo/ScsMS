# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pattern = Field() # 内容页的匹配规则
    site_url = Field()  # 文章url地址*

    title = Field()  # 文章标题*
    url = Field()  # 文章url地址*

    html = Field()  # html源码*

    site_sid = Field()  # 文章来源site的sid

    content = Field()  # 文章正文
    publish_time = Field()  # 发表时间
    collect_time = Field()  # 采集时间