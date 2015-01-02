app = angular.module("fa_blog", ["ui.router","fa_blog_service","ngAnimate"]);

app.config(function($stateProvider, $urlRouterProvider) {

	$urlRouterProvider.otherwise('/home');

	$stateProvider

	// HOME STATES AND NESTED VIEWS ========================================
	.state('home', {
		url : '/home',
		templateUrl : 'static/html/p1.html',
		controller : PostListController
//		controller : function($scope, $resource) {
//			var Todo = $resource('/api/post',
//					null,
//					{getData: {method:'GET',isArray: true}}
//			);
//
//			Todo.getData().$promise.then(function(todo) {
//			   // success
//			   $scope.posts = todo;//'>>>>>>>>'+JSON.stringify(todo);
//			}, function(errResponse) {
//			   // fail
//				$scope.posts = 'failed'+errResponse.status
//			});
//		}
	})
 
	// ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
	.state('about', {
	// we'll get to this in a bit
	});

});
// var customInterpolationApp = angular.module('fa_blog', []);
//
//	 customInterpolationApp.config(function($interpolateProvider) {
//		 $interpolateProvider.startSymbol('[[');
//		 $interpolateProvider.endSymbol(']]');
//	 });
app.controller('TestController', function($scope, $element) {
	$scope.selected = 0;
	$scope.click = function() {
		console.log($element.find('a'));
	};
	
	$scope.active_select = function(id) {
		console.log(id)
		if (id===$scope.selected) return 'active';
		return '';
	}
	
	$scope.setMaster = function(section) {
	    $scope.selected = section;
	    console.log(section)
	}

	$scope.isSelected = function(section) {
	    return $scope.selected === section ? 'active':'';
	}
	$scope.menu_active = $scope.isSelected;
	$scope.s2 = $scope.isSelected;
	
	
	$scope.showButton = function () {
        $scope.expression = true;
    }
    $scope.hideButton = function () {
        $scope.expression = false;
    }
});


app.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[');
	$interpolateProvider.endSymbol(']}');
}]);



