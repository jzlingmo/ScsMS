# -*- coding: utf-8 -*-
__author__ = 'jz'

import string

from scs_app.db_connect import *


class ArticleService():
    def __init__(self):
        self.db = get_connection()

    def get_article_by_sid(self, article_sid):
        fields = 'article.sid,article.url,title,content,keywords,abstract,collect_time,publish_time,author,' \
                 'processed,processed_tp,processed_lc,' \
                 'name as site_name,type as site_type,lang as site_lang,site.url as site_url'
        sql = 'select '+fields+' from article left join site on article.site_sid = site.sid where article.sid=%s'
        params = [article_sid, ]
        article = self.db.get(sql, params)
        return article

    # dict_where={'processed':0,'collect_time':'100,200'}
    # order_by='publish_time,sid'
    # limit=[1,10]
    def get_articles_and_site(self, dict_where=None, order_by=None, order_type='DESC', limit=None, need_count=True):
        fields = 'article.sid,article.url,article.location_sid,title,collect_time,publish_time,author,processed,name,type,lang'
        where_clause = []
        parameters = []

        sql_select_fields = "SELECT " + fields + " FROM article LEFT JOIN site ON article.site_sid=site.sid"
        sql_select_count = "SELECT COUNT(*) FROM article LEFT JOIN site ON article.site_sid=site.sid"
        sql_rest = ""
        if dict_where:
            for k, v in dict_where.iteritems():
                # article table
                if k in 'location_sid':
                    where_clause.append('article.' + k + '=%s')
                    parameters.append(v)
                # site table
                if k in 'type,name,lang':
                    where_clause.append('site.' + k + '=%s')
                    parameters.append(v)

                elif k in 'processed':
                    if v == '':
                        continue
                    where_clause.append(k + '=%s')
                    parameters.append(int(v))

                # need between
                elif k in 'publish_time,collect_time':
                    v = string.split(v, ',')
                    v_len = len(v)
                    if v_len == 1 and not v[0]:
                        v = int(v[0]) if v.isdigit() else v
                        where_clause.append(k + '=%s')
                        parameters.append(v)
                    elif v_len == 2:
                        if v[0] == '':
                            # <= v[1]
                            max = int(v[1]) if v[1].isdigit() else v[1]
                            where_clause.append(k + '<= %s')
                            parameters.append(max)
                        elif v[1] == '':
                            # >=v[0]
                            min = int(v[0]) if v[0].isdigit() else v[0]
                            where_clause.append(k + '>= %s')
                            parameters.append(min)
                        else:
                            # between v[0] and v[1]
                            max = int(v[1]) if v[1].isdigit() else v[1]
                            min = int(v[0]) if v[0].isdigit() else v[0]
                            where_clause.append(k + ' BETWEEN %s AND %s ')
                            parameters.append(min)
                            parameters.append(max)
            if where_clause:
                sql_rest += " WHERE " + ' AND '.join(where_clause)

        if order_by:
            sql_rest += " ORDER BY " + ' '.join((order_by, order_type))
        if need_count:
            total = self.db.query(sql_select_count + sql_rest, parameters)
            total = total[0]['COUNT(*)']
        if limit:
            sql_rest += " LIMIT " + ','.join((str(limit[0]), str(limit[1])))

        articles = self.db.query(sql_select_fields + sql_rest, parameters)
        if need_count:
            return articles, total
        return articles

    def update_article_by_id(self, article_id, row_dict):
        where_dict = {'sid': article_id}
        update_count = self.db.update_by_dict('article', row_dict, where_dict)
        return update_count

    def delete_article_by_id(self, article_id):
        sql = 'delete from article where sid=%s'
        params = [article_id, ]
        delete_count = self.db.execute_rowcount(sql, params)
        return delete_count