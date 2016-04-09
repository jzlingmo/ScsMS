'use strict';

/* Controllers */

var appControllers = angular.module('appControllers', []);


//RootCtrl 注销 初始化全局变量
appControllers.controller('RootCtrl', ['$scope', '$rootScope', '$location', '$cookieStore', 'SessionService',
    function ($scope, $rootScope, $location, $cookieStore, SessionService) {
        //文章列表
        $rootScope.articles = [];
        $rootScope.a_page = {
            page_index: 0,
            page_size: 20,
            total: 0
        };
        //地理位置分类中的文章
        $rootScope.m_articles = [];
        $rootScope.m_page = {
            page_index: 0,
            page_size: 15,
            total: 0
        };
        $rootScope.current_location_sid = ''
        //已选择的值
        $rootScope.choosed = {
            processed: 0,
            time: '*',
            time_field: 'collect_time',
            order_type: 'DESC'
        };
        //注销
        $scope.logout = function () {
            SessionService.logout()
            $cookieStore.remove('current_user')
            $cookieStore.remove('api_key')
            $rootScope.loggedIn = false;
            $location.path('/login');
        }
    }
]);

//login
appControllers.controller('loginCtrl', ['$scope', '$rootScope', '$location', '$cookieStore', 'SessionService',
    function ($scope, $rootScope, $location, $cookieStore, SessionService) {
        $scope.user = {username: '', password: ''};
        $scope.loginError = false;
        //if logined should redirect to main
        if ($rootScope.loggedIn) {
            console.log('to home')
            $location.path('/home');
        }
        $scope.login = function () {
            SessionService.login($scope.user.username, $scope.user.password).success(function (data) {
                $scope.user = {
                    username: '',
                    password: ''
                }
                $rootScope.api_key = data.api_key
                $rootScope.current_user = data.user
                $cookieStore.put('current_user', data.user)
                $cookieStore.put('api_key', data.api_key)

                $location.path('/home')

            }).error(function (data, status, headers, config) {
                    $scope.loginError = true
                });

        }
    }
]);

//home
appControllers.controller('homeCtrl', ['$scope', '$http', 'SpiderService', 'CountService',
    function ($scope, $http, SpiderService, CountService) {
        $scope.hello = 'hello home';
        $scope.total_count = '+'
        $scope.processed_count = '+'
        $scope.supported_lc_count = '+'
        $scope.has_lc_count = '+'
        $scope.pid = ''

        CountService.get_all().success(function (data) {
            $scope.total_count = data
        })
        CountService.get_processed().success(function (data) {
            $scope.processed_count = data
        })

        CountService.get_supported_lc().success(function (data) {
            $scope.supported_lc_count = data
        })
        CountService.get_has_lc().success(function (data) {
            $scope.has_lc_count = data
        })
        SpiderService.get().success(function (spider) {
            $scope.pid = spider['pid']
        })

    }]);

//articles/
appControllers.controller('articlesCtrl', ['$scope', '$rootScope', '$filter', '$timeout', 'ArticleService',
    function ($scope, $rootScope, $filter, $timeout, ArticleService) {

        //所有选项
        $scope.options = {
            processed: [
                {'value': '', 'label': '全部'},
                {'value': '1', 'label': '已处理'},
                {'value': '0', 'label': '未处理'}
            ],
            dates: [
                {'value': '1D', 'label': '今天'},
                {'value': '1W', 'label': '最近一周'},
                {'value': '1M', 'label': '最近一个月'},
                {'value': '3M', 'label': '最近三个月'},
                {'value': '1Y', 'label': '最近一年'},
                {'value': '*', 'label': '全部'}
            ],
            time_field: [
                {value: 'collect_time', label: '采集时间'},
                {value: 'publish_time', label: '发布时间'}
            ]
        }


        $scope.$watch(function () {
            return $rootScope.choosed
        }, function () {
            console.log($rootScope.choosed)
            $rootScope.a_page = {
                page_index: 0,
                page_size: 20,
                total: 0
            };
            $scope.doRefresh()
        }, true)


        $scope.doRefresh = function () {
            ArticleService.getArticleList($rootScope.choosed, $rootScope.a_page).success(function (data) {
                $rootScope.articles = data.data
                $rootScope.a_page.page_index = data.page.page_index
                $rootScope.a_page.page_size = data.page.page_size
                $rootScope.a_page.total = data.page.total
            })
        }
        //初始化列表
        if (!$rootScope.articles) {
            $scope.doRefresh()
        }

        $scope.pageChanged = function () {
            $scope.doRefresh()
        };


    }]);

//article detail
appControllers.controller('articleCtrl', ['$scope', '$rootScope', '$http', '$location', '$routeParams', 'ArticleService', '$timeout',
    function ($scope, $rootScope, $http, $location, $routeParams, ArticleService, $timeout) {
        var article_sid = $routeParams.sid

        $scope.article = {
            sid: '',
            title: '',
            content: '',
            url: '',
            keywords: '',
            abstract: '',
            collect_time: '',
            publish_time: '',
            processed: '',
            processed_tp: '',
            processed_lc: '',
            topic_name: '',
            location_name: '',
            site_url: '',
            site_name: '',
            site_type: '',
            site_lang: ''
        }

        $scope.refreshing = false
        $scope.doRefresh = function () {
            $scope.refreshing = true
            ArticleService.getArticle(article_sid).success(function (data) {
                $scope.article = data
                $scope.refreshing = false
            })
        }
        $scope.doRefresh()

        //关键字和摘要抽取
        $scope.extracting = false
        $scope.extract = function () {
            $scope.extracting = true
            ArticleService.getSinExtract(article_sid).success(function (data) {
                $scope.article.keywords = data['keywords']
                $scope.article.abstract = data['abstract']
                console.log('extract end')
                $scope.extracting = false
            })
        }

        //摘要和关键字编辑模式
        $scope.keywords_edit = false
        $scope.abstract_edit = false
        var old_keywords = ''
        var old_abstract = ''
        //edit
        $scope.edit_keywords = function () {
            old_keywords = angular.copy($scope.article.keywords)
            $scope.keywords_edit = true
        }
        $scope.edit_abstract = function () {
            old_abstract = angular.copy($scope.article.abstract)
            $scope.abstract_edit = true
        }
        //cancel
        $scope.cancel_keywords = function () {
            $scope.article.keywords = old_keywords
            $scope.keywords_edit = false
        }
        $scope.cancel_abstract = function () {
            $scope.article.abstract = old_abstract
            $scope.abstract_edit = false
        }
        //save
        $scope.save_keywords = function () {
            ArticleService.updateArticle(article_sid, {keywords: $scope.article.keywords}).success(function () {
                $scope.keywords_edit = false
            })
        }
        $scope.save_abstract = function () {
            ArticleService.updateArticle(article_sid, {abstract: $scope.article.abstract}).success(function () {
                $scope.abstract_edit = false
            })

        }

        //删除
        $scope.delete_article = function () {
            //todo alert something to confirm
            ArticleService.deleteArticle(article_sid).success(function (data) {
                $location.path('/articles')
            })

        }
    }]);

//charts
appControllers.controller('chartsCtrl', ['$scope', 'ChartService', function ($scope, ChartService) {
    $scope.chartOption = {
        x: [
            {'value': 'collect_time', 'label': '根据采集时间'},
            {'value': 'publish_time', 'label': '根据发布时间'}
        ],
        group: [
            {'value': 'd', 'label': '按天'},
            {'value': 'm', 'label': '按月'},
            {'value': 'y', 'label': '按年'}
        ],
        key: [
            {'value': 'name', 'label': '按网站名称'},
            {'value': 'type', 'label': '按网站类型'}
        ]
    }
    //已选择的值
    $scope.choosed = {
        group: 'd',
        x: 'collect_time',
        key: 'name'
    };

    $scope.data = []

    $scope.doRefresh = function () {
        ChartService.getCharts($scope.choosed).success(function (data) {
            $scope.data = data
        })
    }
    //初始化图表
    $scope.doRefresh()
    //清除图表中的数据
    $scope.clearData = function () {
        $scope.data = []
    }
}]);

//map
appControllers.controller('mapCtrl', ['$scope', '$rootScope', 'CountService', 'ArticleService', 'LocationService',
    function ($scope, $rootScope, CountService, ArticleService, LocationService) {
        $scope.supported_lc_count = '+'
        $scope.has_lc_count = '+'

        $scope.refreshCount = function () {
            CountService.get_supported_lc().success(function (data) {
                $scope.supported_lc_count = data
            })
            CountService.get_has_lc().success(function (data) {
                $scope.has_lc_count = data
            })
        }
        $scope.refreshCount()

        //进行地理位置分类处理
        $scope.processing = false
        $scope.get_multi_location = function (per_count) {
            $scope.processing = true
            ArticleService.getMultiLocation(per_count).success(function (processed_count) {
                $scope.processing = false
                $scope.refreshCount()
                $scope.get_locations_with_count()
                if ($rootScope.current_location_sid != '') {
                    $scope.doRefresh()
                }
            })
        }

        //获取地理位置分类
        $scope.locations = []
        $scope.get_locations_with_count = function () {
            LocationService.getLocationWithCount().success(function (locations) {
                $scope.locations = locations
            })
        }
        $scope.get_locations_with_count()

        $scope.change_location = function (to_sid) {
            $rootScope.current_location_sid = to_sid
            $scope.doRefresh()
        }

        //根据地理位置获取文章列表
        $scope.doRefresh = function () {
            ArticleService.getArticleList({location_sid: $rootScope.current_location_sid}, $rootScope.m_page).success(function (data) {
                $rootScope.m_articles = data.data
                $rootScope.m_page.page_index = data.page.page_index
                $rootScope.m_page.page_size = data.page.page_size
                $rootScope.m_page.total = data.page.total
            })
        }
    }]);

//settings
appControllers.controller('settingsCtrl', ['$scope', 'LocationService',
    function ($scope, LocationService) {
        $scope.hello = 'hello settings';
        LocationService.getLocationWithCount().success(function (locations) {
            console.log(locations)
            $scope.locations = locations
        })
    }
]);

//keywords settings
appControllers.controller('settingsKeywordsCtrl', ['$scope', '$http', 'KeywordService', '$modal',
    function ($scope, $http, KeywordService, $modal) {
        $scope.keywords = '';

        $scope.refreshing = false
        $scope.deleting = ''
        $scope.doRefresh = function () {
            $scope.refreshing = true
            KeywordService.get_all().success(function (data) {
                $scope.keywords = data
                $scope.refreshing = false
                $scope.deleting = ''
            })
        }

        $scope.doRefresh()

        $scope.delete_keyword = function (sid) {
            $scope.deleting = sid
            KeywordService.delete(sid).success(function () {
                $scope.doRefresh()
            })
        }

        /*
         * 新增关键字
         * */
        $scope.open_new_keyword = function (size) {
            var modalInstance = $modal.open({
                templateUrl: '/static/views/modal/new_keyword.html',
                controller: NewKeywordCtrl, // 指定新增关键字的控制器
                size: size
            });

            modalInstance.result.then(function () {
                $scope.doRefresh()
            }, function () {
            });
        };
        var NewKeywordCtrl = function ($scope, $modalInstance, KeywordService) {
            $scope.keyword = {
                keyword: '',
                position: 1,
                has: 1
            };

            $scope.adding = false
            $scope.save = function () {
                $scope.adding = true
                KeywordService.post($scope.keyword).success(function () {
                    $modalInstance.close();
                    $scope.adding = false
                })
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
        }
    }]);

//sites settings
appControllers.controller('settingsSitesCtrl', ['$scope', '$http', '$modal', '$log', 'SiteService',
    function ($scope, $http, $modal, $log, SiteService) {
        $scope.sites = '';

        $scope.refreshing = false
        $scope.deleting = ''
        $scope.doRefresh = function () {
            $scope.refreshing = true
            SiteService.get_all().success(function (data) {
                $scope.sites = data
                $scope.refreshing = false
                $scope.deleting = ''
            })
        }

        $scope.doRefresh()

        $scope.delete_site = function (sid) {
            $scope.deleting = sid
            SiteService.delete(sid).success(function () {
                $scope.doRefresh()
            })
        }


        /*
         * 打开编辑抓取的网站
         * */
        $scope.open_edit = function (idx, size) {
            var modalInstance = $modal.open({
                templateUrl: '/static/views/modal/edit_site.html',
                controller: EditSiteCtrl, // 指定编辑网站的控制器
                size: size,
                resolve: {
                    site: function () {
                        return angular.copy($scope.sites[idx]);
                    }
                }
            });

            modalInstance.result.then(function (updated_site) {
                // close callback function
                $scope.sites[idx] = updated_site;
            }, function () {
                // dismiss callback function
            });
        };

        var EditSiteCtrl = function ($scope, $modalInstance, site, SiteService) {
            $scope.site_types = SITE_TYPES

            $scope.site = site;

            $scope.saving = false
            $scope.save = function () {
                $scope.saving = true
                SiteService.update($scope.site.sid, $scope.site).success(function () {
                    $modalInstance.close($scope.site);
                    $scope.saving = false
                })
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
        }
        /*
         * 新增抓取的网站
         * */
        $scope.open_new_site = function (size) {
            var modalInstance = $modal.open({
                templateUrl: '/static/views/modal/new_site.html',
                controller: NewSiteCtrl, // 指定编辑网站的控制器
                size: size
            });

            modalInstance.result.then(function () {
                $scope.doRefresh()
            }, function () {
            });
        };
        var NewSiteCtrl = function ($scope, $modalInstance, SiteService) {
            $scope.site_types = SITE_TYPES
            $scope.site = {
                url: '',
                name: '',
                type: '新闻',
                pattern: '',
                visible: 0
            };
            $scope.adding = false
            $scope.save = function () {
                $scope.adding = true
                SiteService.post($scope.site).success(function () {
                    $modalInstance.close();
                    $scope.adding = false
                })
            };

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel');
            };
        }
    }]);

//spider settings
appControllers.controller('settingsSpiderCtrl', ['$scope', 'SpiderService',
    function ($scope, SpiderService) {


        $scope.ismeridian = false;
        $scope.hstep = 1;
        $scope.mstep = 15;
        $scope.options = {
            hstep: [1, 2, 3, 4, 6, 8, 10, 12, 15, 18]
        };

        $scope.spider = {
            sid: '',
            start_time: new Date(0, 0, 0, 0, 0),
            work_time: 4,
            pid: '',
            script: ''
        };
        $scope.doRefresh = function () {
            SpiderService.get().success(function (data) {
                $scope.spider.sid = data.sid;
                $scope.spider.start_time = new Date(0, 0, 0, parseInt(data.start_time) / 3600, parseInt(data.start_time) % 3600 / 60); //Y,M,D,h,m
                $scope.spider.work_time = parseInt(data.work_time) / 3600;
                $scope.spider.pid = data.pid;
                $scope.spider.script = data.script;
            })
        }
        $scope.doRefresh();

        $scope.saving = false
        $scope.save = function () {
            $scope.saving = true
            var spider = angular.copy($scope.spider)
            spider.start_time = spider.start_time.getHours() * 3600 + spider.start_time.getMinutes() * 60
            spider.work_time = spider.work_time * 3600
            SpiderService.post(spider).success(function () {
                $scope.saving = false
            })
        }

        $scope.starting = false
        $scope.start_spider = function () {
            $scope.starting = true
            SpiderService.start().success(function (pid) {
                $scope.spider.pid = pid
                $scope.starting = false
            })
        }

        $scope.stopping = false
        $scope.stop_spider = function () {
            $scope.stopping = true
            SpiderService.stop($scope.spider.sid).success(function () {
                $scope.spider.pid = ''
                $scope.stopping = false
            })
        }
    }]);