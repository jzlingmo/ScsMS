'use strict';

/* Directives */

var appDirectives = angular.module('appDirectives', []);

appDirectives.directive('areaChart', function () {
    function link(scope, ele, attr) {

        var ele = ele[0]
        var svg = d3.select(ele).append('svg')

        var colors = d3.scale.category20();
        var keyColor = function (d, i) {
            return colors(d.key)
        };
        var chart = nv.models.stackedAreaChart()
            .height(400)
            .margin({right: 50})
            .x(function (d) {
                return d[0]
            })
            .y(function (d) {
                return d[1]
            })
            .showControls(true)
            .useInteractiveGuideline(true)
            .color(keyColor)
            .clipEdge(true)
            .transitionDuration(500);

        wrapChartData()

        var time = '%Y-%m-%d'
        scope.$watch("data", wrapChartData);
        scope.$watch("time", setTime);

        function setTime() {
            time = format_time(scope.time)
        }

        function wrapChartData() {
            var data = scope.data
            svg.datum(data).transition().duration(1000).call(chart)
            chart.xAxis.tickFormat(function (d) {
                return d3.time.format(time)(new Date(d))
            });
            chart.yAxis
                .tickFormat(d3.format(',f'));

            nv.utils.windowResize(chart.update);
        }

        function format_time(time) {
            switch (time) {
                case 'd':
                    return '%Y-%m-%d';
                    break;
                case 'm':
                    return '%Y-%m';
                    break;
                case 'y':
                    return '%Y';
                    break;
            }
        }
    }

    return {
        link: link,
        restrict: 'E',
        scope: { data: '=', time: '='}
    }
})

appDirectives.directive("switch", function () {
    return {
        restrict: "EA",
        replace: true,
        scope: {
            model: "=ngModel",
            on: "=",
            off: "=",
            changeExpr: "@ngChange",

            disabled: "@"
        },
        template: "<div class='switch' ng-class='{active: model==on}'><div class='switch-handle'></div></div>",
        link: function (scope, elem, attrs) {

            elem.on('click tap', function () {
                if (attrs.disabled == null) {
                    scope.model = scope.model == scope.on ? scope.off : scope.on;
                    scope.$apply();

                    if (scope.changeExpr != null) {
                        scope.$parent.$eval(scope.changeExpr);
                    }
                }
            });

            elem.addClass('switch-transition-enabled');
        }
    };
});
