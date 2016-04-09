# -*- coding: utf-8 -*-
__author__ = 'jz'

from flask.ext import restful
from flask.ext.restful import reqparse

from scs_app.db_connect import *
from scs_app.service.article_service import ArticleService
from scs_app.utils.time_format import now_timestamp

parser = reqparse.RequestParser()

#site table
parser.add_argument('type', type=str)
parser.add_argument('name', type=str)
parser.add_argument('lang', type=str)
#article table
parser.add_argument('processed', type=str)
parser.add_argument('collect_time', type=str)
parser.add_argument('publish_time', type=str)

parser.add_argument('time_field', type=str)
parser.add_argument('time', type=str)

parser.add_argument('order_by', type=str)
parser.add_argument('order_type', type=str)

parser.add_argument('page_index', type=int)
parser.add_argument('page_size', type=int)

parser.add_argument('location_sid', type=str)


class ArticleListResource(restful.Resource):
    def __init__(self):
        self.db = get_connection()
        self.service = ArticleService()

    # /api/articles?processed=1&publish_time=100,1000&order_by=publish_time&order_type=asc&start_index=1&count=30
    def get(self):
        args = parser.parse_args()
        # 分页
        page_index = args.get('page_index', 1)
        page_size = args.get('page_size', 20)
        if page_index <= 0:
            page_index = 1
        if page_size not in [5, 10, 15, 20, 30, 50]:
            page_size = 20
        limit = [(page_index - 1) * page_size, page_size]
        # 排序及筛选
        order_by = args.get('order_by')
        order_type = args.get('order_type') if args.get('order_type') else 'DESC'
        time_field = args.get('time_field')
        time = args.get('time')
        if not order_by:
            order_by = time_field if time_field else 'collect_time'

        dict_where = {k: v for k, v in args.items() if
                      k in 'type,name,lang,processed,collect_time,publish_time,location_sid' and v is not None}

        # 处理时间
        now_time = now_timestamp()
        # todo 计算真实的时间
        day = 1000 * 3600 * 24
        time_dict = {'1D': day, '1W': day * 7, '1M': day * 30, '3M': day * 91, '6M': day * 183, '1Y': day * 365}
        if time in time_dict:
            dict_where[time_field] = str(now_time - time_dict[time]) + ',' + str(now_time)


        print(dict_where)
        print(order_by)
        print(order_type)
        print(limit)
        result, total = self.service.get_articles_and_site(dict_where=dict_where, order_by=order_by,
                                                           order_type=order_type,
                                                           limit=limit)
        response_data = {
            'data': result,
            'page': {
                'page_index': page_index,
                'page_size': page_size,
                'total': total
            }
        }
        return response_data
