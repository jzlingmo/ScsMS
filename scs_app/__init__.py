# -*- coding: utf-8 -*-
__author__ = 'jz'

import sys

from flask import Flask, g, render_template
from flask.ext import restful

from scs_app.db_connect import *

from resources.session_resource import SessionResource

from resources.article_resource import ArticleResource
from resources.articles_resource import ArticleListResource
from resources.chart_resource import ChartResource
from resources.count_resource import CountResource
from resources.keyword_resource import KeywordResource
from resources.keywords_resource import KeywordsResource
from resources.site_resource import SiteResource
from resources.sites_resource import SitesResource
from resources.sin_action_resource import SinActionResource
from resources.mul_action_resource import MulActionResource

from resources.spider_resource import SpiderResource
from resources.spider_action_resource import SpiderActionResource

from resources.locations_resource import LocationsResource


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')

# 登录接口（权限） 根据用户名和密码创建session 根据sessionid删除session
api.add_resource(SessionResource, '/api/session')

api.add_resource(ArticleResource, '/api/articles/<int:article_id>')
api.add_resource(ArticleListResource, '/api/articles')

api.add_resource(LocationsResource, '/api/locations')

api.add_resource(ChartResource, '/api/charts')
api.add_resource(CountResource, '/api/count')

api.add_resource(KeywordResource, '/api/keywords/<int:sid>')
api.add_resource(KeywordsResource, '/api/keywords')

api.add_resource(SiteResource, '/api/sites/<int:sid>')
api.add_resource(SitesResource, '/api/sites')

api.add_resource(SinActionResource, '/api/articles/<int:article_sid>/action/<string:type>')
api.add_resource(MulActionResource, '/api/articles/action/<string:type>')

api.add_resource(SpiderResource, '/api/spider')
api.add_resource(SpiderActionResource, '/api/spider/<string:action>')