var app = angular.module('ntust-ask-course-app',['ngProgress']);

app.controller('courseCtrl', function($scope, $http, ngProgress){
    $scope.search = function(){
        ngProgress.start();
        $http.get('http://course.ntustsg.com/api/',{params: {keyword: $scope.course['keyword']}}).success(function(data){
            $scope.results = data;
            $scope.num = 0;
            $scope.maxnum = data.hits.length;
            ngProgress.complete();
        }).error(function(data){
            console.log(data);
        });
    };

    $scope.nextItem = function(){
        if($scope.num < $scope.maxnum - 1){
            $scope.num += 1;
        }
    };
    $scope.previousItem = function(){
        if($scope.num > 0){
            $scope.num -= 1;    
        }
    };
});

app.filter('nl2br', function($sce){
    return function(msg,is_xhtml) { 
        var is_xhtml = is_xhtml || true;
        var breakTag = (is_xhtml) ? '<br />' : '<br>';
        var msg = (msg + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
        return $sce.trustAsHtml(msg);
    }
});

app.filter('range', function() {
  return function(input, min, max) {
    min = parseInt(min); //Make string input int
    max = parseInt(max);
    for (var i=min; i<max; i++)
      input.push(i);
    return input;
  };
});