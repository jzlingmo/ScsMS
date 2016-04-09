'use strict';

/* Services */

var appServices = angular.module('appServices', []);
//用于前后端服务器分离 后端服务器地址
var host = ''
var spider_host = 'http://localhost:6800'

appServices.service('ArticleService', ['$http',
    function ($http) {
        //获取文章
        this.getArticleList = function (filter, page) {
            var data = jsonToUrl(filter)
            if (data) {
                data = '&' + data;
            }
            return $http.get(host + '/api/articles?page_index=' + page.page_index + '&page_size=' + page.page_size
                + data);
        };
        //获取单篇文章
        this.getArticle = function (article_sid) {
            return $http.get(host + '/api/articles/' + article_sid);
        }
        //更新单篇文章
        this.updateArticle = function (article_sid, article) {
            return $http.put(host + '/api/articles/' + article_sid, article);
        }
        //删除单篇文章
        this.deleteArticle = function (article_sid) {
            return $http.delete(host + '/api/articles/' + article_sid);
        }
        //单篇提取关键字和摘要
        this.getSinExtract = function (article_sid) {
            return $http.get('/api/articles/' + article_sid + 'action/extract')
        }
        //单篇地理位置分类
        this.getSinLocation = function (article_sid) {
            return $http.get('/api/articles/' + article_sid + 'action/location')
        }
        //todo 多篇提取关键字和摘要
        this.getMultiExtract = function (count) {
            return ''
        }
        //多篇地理位置分类
        this.getMultiLocation = function (count) {
            return $http.post('/api/articles/action/location', {'count': count})
        }


    }
]);

appServices.service('LocationService', ['$http',
    function ($http) {
        this.getLocationWithCount = function () {
            return $http.get('/api/locations?type=count');
        }
    }
]);

appServices.service('ChartService', ['$http',
    function ($http) {
        this.getCharts = function (filter) {
            var data = jsonToUrl(filter)
            if (data) {
                data = '&' + data;
            }
            return $http.get('/api/charts?' + data);
        }
    }
]);

appServices.service('SessionService', ['$http', '$rootScope',
    function ($http, $rootScope) {
        this.login = function (username, password) {
            var data = {'username': username, 'password': password}
            return $http.post('/api/session', data);
        }

        this.logout = function () {
            return $http.delete('/api/session?api_key=' + encodeURIComponent($rootScope.api_key));
        }

    }
]);

appServices.service('SiteService', ['$http',
    function ($http) {
        this.get_all = function () {
            return $http.get('/api/sites')
        }
        this.post = function (site) {
            return $http.post('/api/sites', site)
        }
        this.update = function (sid, site) {
            return $http.put('/api/sites/' + sid, site)
        }
        this.delete = function (sid) {
            return $http.delete('/api/sites/' + sid)
        }

    }
]);

appServices.service('KeywordService', ['$http',
    function ($http) {
        this.get_all = function () {
            return $http.get('/api/keywords')
        }
        this.post = function (keyword) {
            return $http.post('/api/keywords', keyword)
        }
        this.update = function (sid, keyword) {
            return $http.put('/api/keywords/' + sid, keyword)
        }
        this.delete = function (sid) {
            return $http.delete('/api/keywords/' + sid)
        }

    }
]);

appServices.service('SpiderService', ['$http',
    function ($http) {
        this.get = function () {
//            return $http.get(spider_host+'schedule.json',{project:'scs_crawler',spider:'scs_spider'})
            return $http.get('/api/spider')
        };
        this.post = function (data) {
            //start_time interval
            return $http.post('/api/spider', data)
        }
        this.start = function () {
            return $http.post('/api/spider/start')
        }
        this.stop = function (sid) {
            return $http.post('/api/spider/stop', {'sid': sid})
        }

    }
]);

appServices.service('CountService', ['$http',
    function ($http) {


        this.get_all = function () {
            return $http.get('/api/count?type=all')
        }

        this.get_processed = function () {
            return $http.get('/api/count?type=processed')
        }

        this.get_supported_lc = function () {
            return $http.get('/api/count?type=supported_lc')
        }

        this.get_has_lc = function () {
            return $http.get('/api/count?type=has_lc')
        }

    }
]);

//将键值对转换成url
function jsonToUrl(json) {
    var params = []
    for (var key in json) {
        params.push(key + '=' + json[key])
    }
    return params.join('&')
}