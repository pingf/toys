function IndexController($scope) {

}

function AboutController($scope) {

}

function PostListController($scope, Post) {
	Post.query().$promise.then(function(posts) {
		$scope.posts = posts
	}, function(errResponse) {
		// fail
		$scope.posts = 'failed' + errResponse.status
	});
	
	$scope.click = function() {
		$scope.test='hello';
	}	
	
	$scope.person = {
	        firstName: "John",
	        lastName: "Doe",
	        fullName: function() {
	            var x;
	            x = $scope.person;
	            return x.firstName + " " + x.lastName;
	        }
	    };
}

function PostDetailController($scope, $routeParams, Post) {
	var postQuery = Post.get({
		postId : $routeParams.postId
	}, function(post) {
		$scope.post = post;
	});
}


