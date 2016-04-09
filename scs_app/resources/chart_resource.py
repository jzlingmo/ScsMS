# -*- coding: utf-8 -*-
__author__ = 'jz'

import time
from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *

parser = reqparse.RequestParser()
# publish_time collect_time
parser.add_argument('x', type=str)
# day,week,month,year
parser.add_argument('group', type=str)
# site.type site.name
parser.add_argument('key', type=str)


def format_time(group):
    d = 1000 * 3600 * 24
    if group == 'd':
        return '%Y%m%d', ''
    elif group == 'm':
        return '%Y%m', '01'
    elif group == 'y':
        return '%Y', '0101'
    else:
        return '%Y%m%d', ''


class ChartResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()

    def get(self):
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        group = args.get('group', 'd')
        x = args.get('x', 'collect_time')
        key = args.get('key', 'name')

        time_format, append = format_time(group)
        result = []

        data = []

        # [
        #     {key:'',values:[  [time,count],[time,count]  ]}, # one item
        #     {key:'',values:[time,count]}
        # ]
        #1 从site表取出所有的site.sid 和 site.name/site.type
        if key == 'name':
            sites = self.db.query("select name as 'key' from site")
        elif key == 'type':
            sites = self.db.query("select distinct type as 'key' from site")

        #2 遍历sid查询values
        all_times = set()
        for site in sites:
            item = {}
            values = {}
            rs = self.db.query(
                "select DATE_FORMAT(FROM_UNIXTIME(" + x + "/1000),%s) as time,count(*) as count from article "
                                                          "left join site on article.site_sid=site.sid"
                                                          " where site." + key + "=%s GROUP BY time",
                (time_format, site['key']))
            for value in rs:
                t = str(value['time']) + append
                ti = time.mktime(time.strptime(t, '%Y%m%d')) * 1000
                all_times.add(ti)
                values[ti] = int(value['count'])
            item['key'] = site['key']
            item['values'] = values
            result.append(item)

        all_times = list(all_times)
        all_times.sort()
        for rs in result:
            # rs
            # {
            #     key: '',
            #     values: {time:count,time: count}
            # }, # one item
            rs_values = rs['values']
            item = {}
            values = []
            for t in all_times:
                values.append([t, rs_values[t] if t in rs_values else 0])
            item['key'] = rs['key']
            item['values'] = values
            data.append(item)

        return data