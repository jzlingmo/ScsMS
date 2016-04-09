# -*- coding: utf-8 -*-
__author__ = 'jz'

import re


days = {
    u'\d{6}/\d{2}': u'%Y%m/%d', # 201404/09
    u'\d{4}-\d{2}/\d{2}': u'%Y-%m/%d', # 2010-01/01
    u'\d{4}-\d{2}-\d{2}': u'%Y-%m-%d', # 2010-01-01
    u'\d{4}/\d{1,2}/\d{1,2}': u'%Y/%m/%d', # 2010/01/01
    u'\d{4}-\d{2}': u'%Y-%m', # 2010-01
    u'\d{4}\d{2}\d{2}': u'%Y%m%d', # 20100101
}


def validate_content_url(url):
    rs = [True, '']

    if url.endswith('/'):
        rs = [False, 'end with "/"']
    if url.count('/') < 4:
        rs = [False, 'level not enough']

    # 根据网页url中是否存在日期初步判断是否为新闻内容页
    url = url.rsplit('/', 1)[0]  # 去除文件名+后缀
    has_date = False
    for x in days:
        result = re.search(x, url)
        if result:
            has_date = True
            break

    if not has_date:
        rs = [False, 'no time']

    return rs


if __name__ == '__main__':
    urls = [
        'http://news.sina.com.cn/c/2014-04-09/214929897678.shtml',
        'http://news.sina.com.cn/c/20140409/214929897678.shtml',
        'http://news.sina.com.cn/c/201404/09/214929897678.shtml',
        'http://mil.huanqiu.com/world/2014-05/4992446.html'
    ]
    for url_z in urls:
        print(validate_content_url(url_z))