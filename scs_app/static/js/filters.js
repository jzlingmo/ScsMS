'use strict';

/* Filters */
var host = ''

var appFilters = angular.module('appFilters', [])

appFilters.filter('active0', function () {
    return function (input) {
        switch (input) {
            case 0:
                return '已激活'
            case 1:
                return '未激活'
        }
    };
});

appFilters.filter('iscontain', function () {
    return function (input) {
        switch (input) {
            case 0:
                return '不包含'
            case 1:
                return '包含'
        }
    };
});

appFilters.filter('processed', function () {
    return function (input) {
        switch (input) {
            case 0:
                return '待处理'
            case 1:
                return '已处理'

        }
    };
});

appFilters.filter('has', function () {
    return function (input) {
        switch (input) {
            case 0:
                return '不包含'
            case 1:
                return '包含'

        }
    };
});

appFilters.filter('position', function () {
    return function (input) {
        switch (input) {
            case 1:
                return '标题'
            case 2:
                return '正文'

        }
    };
});
