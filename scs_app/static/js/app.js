'use strict';


//
// Define the 'app' module.
//
var app = angular.module('app', [
    'ngAnimate',
    'ngRoute',
    'ngCookies',
    'ngSanitize',

    'mgcrea.ngStrap',
    'ui.bootstrap',

    'appServices',
    'appControllers',
    'appDirectives',
    'appFilters'
]);

app.config(function ($httpProvider, $routeProvider, $locationProvider) {
        $routeProvider
            .when('/login', {templateUrl: 'static/views/login.html', controller: 'loginCtrl'})
            //menu home
            .when('/home', {templateUrl: 'static/views/home.html', controller: 'homeCtrl'})
            //menu articles
            .when('/articles', {templateUrl: 'static/views/articles.html', controller: 'articlesCtrl'})
            .when('/articles/:sid', {templateUrl: 'static/views/article_detail.html', controller: 'articleCtrl'})
            //menu charts
            .when('/charts', {templateUrl: 'static/views/charts.html', controller: 'chartsCtrl'})
            //menu map
            .when('/map', {templateUrl: 'static/views/map.html', controller: 'mapCtrl'})
            .when('/map/:sid', {templateUrl: 'static/views/article_detail_map.html', controller: 'articleCtrl'})
            //menu settings
            .when('/settings', {templateUrl: 'static/views/settings.html', controller: 'settingsCtrl'})
            .when('/settings/keywords', {templateUrl: 'static/views/settings/keywords.html', controller: 'settingsKeywordsCtrl'})
            .when('/settings/sites', {templateUrl: 'static/views/settings/sites.html', controller: 'settingsSitesCtrl'})
            .when('/settings/spider', {templateUrl: 'static/views/settings/spider.html', controller: 'settingsSpiderCtrl'})
            // Catch all
            .otherwise({redirectTo: '/home'});

        // Without server side support html5 must be disabled.
        //$locationProvider.html5Mode(false);

        $httpProvider.interceptors.push(function ($rootScope, $location, $q, $cookieStore) {
            return {
                'request': function (request) {
                    // if we're not logged-in to the AngularJS app, redirect to login page
//                    $rootScope.loggedIn = true; //for test
                    var api_key = $cookieStore.get('api_key')
                    var current_user = $cookieStore.get('current_user')

                    if (!api_key){
                        $rootScope.loggedIn = false
                    }else{
                        if(!$rootScope.loggedIn){
                            $rootScope.current_user = current_user
                            $rootScope.api_key = api_key
                        }
                        $rootScope.loggedIn = true
                    }

                    if (!$rootScope.loggedIn && $location.path() != '/login') {
                        console.log('Not logined');
                        $location.path('/login');
                    }
                    return request;
                },
                'responseError': function (rejection) {
                    // if we're not logged-in to the web service, redirect to login page
                    if (rejection.status === 401) {
                        $rootScope.loggedIn = false;
                        $rootScope.api_key = ''
                        $rootScope.current_user = ''

                        $cookieStore.remove('api_key');
                        $cookieStore.remove('current_user');
                        if ($location.path() != '/login') {
                            $location.path('/login');
                        }
                    }
                    return $q.reject(rejection);
                }
            };
        });
    }
)