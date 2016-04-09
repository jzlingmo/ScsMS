# -*- coding: utf-8 -*-
__author__ = 'jz'

import traceback

import torndb
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from bs4 import BeautifulSoup

from scs_app import config
from scs_crawler.items import ScsItem
from scs_crawler.utils import color


class ScsSpider(Spider):
    name = 'scs_spider'
    # allowed_domains = ['news.sina.com.cn']
    allowed_domains = ['huanqiu.com']
    start_urls = [
        #'http://www.chinadaily.com.cn/' #中国日报 英文版
    ]

    dict_urls = {} # {url:site_sid,...}

    #保存本次运行中已请求过的url
    unique_urls = {}

    def __init__(self):
        self.style = color.color_style()
        try:
            self.db = torndb.Connection(host=config.HOST, database=config.DATABASE,
                                        user=config.USER, password=config.PASSWORD)
            sites = self.db.query('select url,sid,pattern from site where visible = 0')
            self.start_urls = [site['url'] for site in sites]
            self.dict_urls = {site['url']: [site['sid'], site['pattern']] for site in sites}

        except Exception as e:
            print self.style.ERROR("ERROR(SpiderInit): %s" % (str(e),))
            traceback.print_exc()

    def parse(self, response):
        items = []

        html = response.body.decode(response.encoding)
        response_url = response.url
        # domain like www.sina.com
        download_slot = response.meta.get('download_slot')
        #get http or https
        root_url = response_url[0:response_url.index('://') + 3] + download_slot
        file1 = 'links.txt'
        link_file = open(file1, 'a')

        #返回item
        item = ScsItem()

        item['url'] = response_url
        for (k, v) in self.dict_urls.items():
            if k in item['url']:
                item['site_url'] = k
                item['site_sid'] = v[0]
                item['pattern'] = v[1]
                break
        item['html'] = html
        items.append(item)

        #保存网页
        # dirs = 'download/'
        # if base_url.rindex('/') == len(base_url) - 1:
        #     filename = base_url.split("/")[-2]
        # else:
        #     filename = base_url.split("/")[-1]
        # open(dirs + filename, 'wb').write(html)

        #parse url
        # soup = BeautifulSoup(html)
        hxs = Selector(response)
        # for a in soup.find_all('a'):
        for a in hxs.xpath('//a/@href').extract():

            # href = a.get('href')
            href = a

            #if is NoneType
            if not bool(href):
                continue
            href = href.strip()

            link_file.write(href + '\n')


            #0 if href is null
            if len(href) == 0:
                continue
                #1 if start with '#' or contain '@' 'javascript:' 'mailto:'
            if href.find('#') == 0 or href.find('@') != -1 or href.lower().find('javascript:') != -1 or href.find(
                    'mailto:') != -1:
                continue
                #2 solve relative url


            if href.find('://') == -1:
                #relative url
                if href.find('/') == 0:
                    # like '/title'
                    link = root_url + href
                else:
                    #like 'title'
                    link = root_url + '/' + href
            else:
                #absolute url 判断是否在同一域名下
                if href.find(root_url) == -1:
                    continue
                link = href
            #delete url after '#' like 'http://www.xx.com#head'
            link = link.split('#')[0]

            #将未请求过的url加入到请求队列中
            if link not in self.unique_urls:
                self.unique_urls[link] = 0
                items.append(self.make_requests_from_url(link))

        #posts = hxs.x('//h1/a/@href').extract()
        #items.extend([self.make_requests_from_url(url).replace(callback=self.parse_post)
        #          for url in posts])
        #page_links = hxs.x('//div[@class="wp-pagenavi"]/a[not(@title)]')
        #for link in page_links:
        #    if link.x('text()').extract()[0] == u'\xbb':
        #        url = link.x('@href').extract()[0]
        #        items.append(self.make_requests_from_url(url))
        return items
        #TODO  md5()


    def parse_item(self):
        item = []
        return item
