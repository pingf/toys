var navList = angular.module('navList', []);

navList.controller('navCtrl', ['$scope', '$location', function ($scope, $location) {
    $scope.navClass = function (page) {
    	console.log($location.path())
        var currentRoute = $location.path().substring(1) || 'home';
        console.log(page);
        console.log(currentRoute);
        console.log('--------');
        return page === currentRoute ? 'active' : 'inactive';
    };        	
}]);
