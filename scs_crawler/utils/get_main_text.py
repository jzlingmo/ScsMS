__author__ = 'jz'
# -*- coding: utf-8 -*-


# 以k行为行块计算值：
# （1和2均为求最大连续值，假设正文连续，求出正文的起始行和结束行）
# 1、标签总字符数为负数，其它总字符数为整数，相加为该行值
# 2、去除所有除a外的标签，赋予视频、图片相应权值，确定一个负数阈值相加（为了球最大值），每行字符数即为该值
#
# 3、去净所有标签，计算每行的字符数，即为该行值（提供一个阈值确定正文起始行）
#
# #视觉内容块：
# 去除所有不相关块，提取含有字符数最多的块作为正文块，提取正文块中的文字作为正文


import re


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
        temp = (text_b - text_a) - 10
        group_value.append(temp)
    left, right = sum_max(group_value)
    return left, right, len('\n'.join(tmp[:left])), len('\n'.join(tmp[:right]))


def extract(content):
    left, right, x, y = cal_start_and_end(content)
    print(left)
    print(right)
    result = '\n'.join(content.split('\n')[left:right])
    return remove_empty_line(remove_any_tag(result))

import urllib

from parse_item import get_title, clean_html_body

if __name__ == '__main__':
    url = 'http://blog.csdn.net/aoyoo111/article/details/7846987'
    url = 'http://www.cnblogs.com/huangcong/archive/2011/08/31/2160633.html'
    u = urllib.urlopen(url)
    buffer = u.read()

    test_file = open('test1.html', 'r')
    file_text = test_file.read().decode('gbk')
    # file_text = buffer

    print('title:' + get_title(file_text))
    html_body = file_text
    # 清洗html
    html_body = clean_html_body(html_body)
    print('-----------------------')
    print(extract(html_body))
    print('-----------------------')


