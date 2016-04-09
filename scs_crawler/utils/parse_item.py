# -*- coding: utf-8 -*-

import re
import time

from bs4 import BeautifulSoup, Comment
from readability.readability import Document

days = {
    u'\d{4}-\d{1,2}-\d{1,2}': u'%Y-%m-%d',
    u'\d{4}/\d{1,2}/\d{1,2}': u'%Y/%m/%d',
    u'\d{4}年\d{1,2}月\d{1,2}日': u'%Y年%m月%d日',
    u'\d{4}年\d{1,2}月\d{1,2}号': u'%Y年%m月%d号',
    u'(Jan|Feb|March|April|May|June|July|Aug|Sep|Otc|Nov|Dec) {1}\d{1,2}, {1}\d{4}': u'%m %d, %Y',
}

times = {
    u'\d{1,2}:\d{1,2}:\d{1,2}': u'%H:%M:%S',
    u'\d{1,2}:\d{1,2}': u'%H:%M'
}


def get_day(text_str):
    for x in days:
        result = re.search(x, text_str)
        if result:
            a = result.group(0)
            a = a.replace('Jan', '1')
            a = a.replace('Feb', '2')
            a = a.replace('March', '3')
            a = a.replace('April', '4')
            a = a.replace('May', '5')
            a = a.replace('June', '6')
            a = a.replace('July', '7')
            a = a.replace('Aug', '8')
            a = a.replace('Sep', '9')
            a = a.replace('Otc', '10')
            a = a.replace('Nov', '11')
            a = a.replace('Dec', '12')
            return {a: days[x]}
    return {}


def get_time(text_str):
    for x in times:
        result = re.search(x, text_str)
        if result:
            return {result.group(0): times[x]}
    return {}


def get_format_time(text_str):
    """
    @return int 13位时间戳
    """
    date_data = get_day(text_str)
    #如果不存在日期 返回None
    if not date_data:
        return None
    time_data = get_time(text_str)
    format_data = dict(date_data, **time_data)

    time_str = ' '.join(format_data.keys())
    format_str = ' '.join(format_data.values())
    return int(time.mktime(time.strptime(time_str, format_str)) * 1000)
    # return datetime.datetime.strptime(time_str, format_str)


def get_title(html):
    soup = BeautifulSoup(html)
    title = None
    h1_title = None

    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # h1中提取title
    h1_titles = soup.findAll('h1')
    if h1_titles:
        for ele in h1_titles:
            if ele.string:
                h1_title = ele.string.strip()
                break

    # 不存在title
    if not title and h1_title:
        title = h1_title

    return title


def clean_html_body(html):
    soup = BeautifulSoup(html)

    #移除脚本、样式、注释和链接
    for tag in soup.findAll('script'):
        tag.extract()
    for tag in soup.findAll('noscript'):
        tag.extract()
    for tag in soup.findAll('style'):
        tag.extract()
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll('a'):
        del tag['href']
        #移除图片
    for tag in soup.findAll('img'):
        tag.extract()
    for tag in soup.findAll('iframe'):
        tag.extract()
    for tag in soup.findAll('input'):
        tag.extract()
    for tag in soup.findAll('ins'):
        tag.extract()
    r = re.compile(r'\n+', re.M | re.S)
    return r.sub('\n', unicode(soup.body))


def remove_empty_line(content):
    #移除多余的空行
    r = re.compile(r'''^/s+$''', re.M | re.S)
    s = r.sub('', content)
    r = re.compile(r'''\n+''', re.M | re.S)
    s = r.sub('\n', s)
    # 去除首行回车
    if s.find('\n') == 0:
        s = s.replace('\n', '', 1)
    return s


def remove_any_tag(s):
    s = re.sub(r'''<[^>]+>''', '', s)
    return s.strip()


def remove_any_tag_but_a(s):
    text = re.findall(r'''<a[^r][^>]*>(.*?)</a>''', s, re.I | re.S | re.S)
    text_b = remove_any_tag(s)
    return len(''.join(text)), len(text_b)


def remove_image(s, n=50):
    image = 'a' * n
    r = re.compile(r'''<img.*?>''', re.I | re.M | re.S)
    s = r.sub(image, s)
    return s


def remove_video(s, n=1000):
    video = 'a' * n
    r = re.compile(r'''<embed.*?>''', re.I | re.M | re.S)
    s = r.sub(video, s)
    return s


def sum_max(values):
    print(values)
    current_max = values[0]
    glo_max = -1000000
    left, right = 0, 0
    for index, value in enumerate(values):
        current_max += value
        if current_max > glo_max:
            glo_max = current_max
            right = index
        elif current_max < 0:
            current_max = 0
            for i in range(right, -1, -1):
                glo_max -= values[i]
                if abs(glo_max < 0.00001):
                    left = i
                    break
    return left, right + 1


def cal_start_and_end(content, k=1):
    if not content:
        return None, None, None, None
    tmp = content.split('\n')
    group_value = []
    for i in range(0, len(tmp), k):
        group = '/n'.join(tmp[i:i + k])
        group = remove_image(group)
        group = remove_video(group)
        text_a, text_b = remove_any_tag_but_a(group)
        temp = (text_b - text_a) - 4
        group_value.append(temp)
    left, right = sum_max(group_value)
    return left, right, len('\n'.join(tmp[:left])), len('\n'.join(tmp[:right]))


def extract(content):
    left, right, x, y = cal_start_and_end(content)
    result = '\n'.join(content.split('\n')[left:right])
    return remove_empty_line(remove_any_tag(result))


def get_main_text(html):
    main_text = Document(html).summary()
    main_text = BeautifulSoup(main_text).getText()
    # 处理空行
    r = re.compile(r'\n+', re.M | re.S)
    main_text = r.sub('\n', main_text)
    # 去除首行回车
    if main_text.find('\n') == 0:
        main_text = main_text.replace('\n', '', 1)

    return main_text


import urllib

if __name__ == '__main__':
    url = "http://www.defense.gov/news/newsarticle.aspx?id=122291" #美国国防部
    url = "http://vietnamnet.vn/vn/giao-duc/175665/thu-giang-vien---chung-ta-dung-tu-lua-minh--.html" # 越南网
    u = urllib.urlopen(url)
    buffer = u.read()

    test_file = open('test3.html', 'r')
    file_text = test_file.read().decode('utf8')
    file_text = buffer

    print('title:' + get_title(file_text))
    html_body = file_text
    # 清洗html
    html_body = clean_html_body(html_body)
    # print(html_body)
    print(get_format_time(html_body))
    print('--------------------------------------------')
    # print(extract(html_body))
    print(get_main_text(html_body))
    a = 'May 20, 2014'
    print(get_format_time(a))



        # text2 = u""" <html><body><script type> var a = 0;
        # $('#tbtj-1').innerHTML = '<iframe src="' + config.baseurl + config.channels[countArr[0]] + '.html" width="295" height="129" frameborder="0" border="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>';
        #                 $('#tbtj-3').innerHTML = '<iframe src="' + config.baseurl + config.channels[countArr[1]] + '.html" width="295" height="129" frameborder="0" border="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>';
        #                 $('#tbtj-4').innerHTML = '<iframe src="' + config.baseurl + config.channels[countArr[2]] + '.html" width="295" height="129" frameborder="0" border="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>';
        #                 i = Math.floor(Math.random() * 4);
        #                 var slide = new NTES.ui.Slide ($('#js-epSpRecommend > .tabctrl > span'),$('#js-epSpRecommend > .tabcon > div'),'current','mouseover', 10000);
        #                 slide.show(i);
        # </script><a href="http://sdfkjjsdf">aaa</a>this is content</body><html>"""
