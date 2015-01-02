angular.module('fa_blog_service', ['ngResource'])
	.factory('Post', function($resource) {
		return $resource('/api/post', null , {query: {method: 'GET',isArray: true}	});
	});
