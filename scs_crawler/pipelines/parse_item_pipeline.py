# -*- coding: utf-8 -*-
import re

from scs_crawler.pipelines.article_drops import NoTitleDrop, NotContentPageDrop
from scs_crawler.utils import color
from scs_crawler.utils.parse_item import clean_html_body, get_format_time, extract, get_main_text, get_title
from scs_crawler.utils.validate_content_url import validate_content_url


class ParseItem(object):
    crawled_urls = {}

    def __init__(self):
        self.style = color.color_style()

    def process_item(self, item, spider):

        url = item['url']
        html = item['html']
        pattern = item['pattern']
        #如果存在匹配规则 则直接进入匹配规则进行匹配
        if pattern:
            if re.search(pattern, url):
                #匹配为内容页
                item['title'] = get_title(html)
                item['publish_time'] = get_format_time(html)
                item['content'] = get_main_text(html)
                return item
            else:
                raise NotContentPageDrop(info='pattern not match', url=url)

        #0 过滤非新闻网页
        rs = validate_content_url(url)
        if not rs[0]:
            raise NotContentPageDrop(info=rs[1], url=url)

        #1 获取标题
        # 从title中获取标题
        item['title'] = get_title(html)
        # 不存在title 则drop item
        if not item['title']:
            raise NoTitleDrop(url)

        # 页面过期后将不再存在
        if u'页面没有找到' in item['title']:
            raise NotContentPageDrop(info='page not found', url=url)

        # 清洗html
        html = clean_html_body(html)
        #2 获取发布时间
        format_time = get_format_time(html)
        if not format_time:
            raise NotContentPageDrop(info='html no time', url=url)
        item['publish_time'] = format_time

        #3 提取正文
        item['content'] = get_main_text(html)

        return item