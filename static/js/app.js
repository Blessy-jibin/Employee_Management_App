

var app	 = angular.module('app', ['ngCookies','ui.bootstrap','ngMaterial', 'ngMessages']);


app.config(function($interpolateProvider) {
  // changing angular default template rendering to '{[{}]}'.
  //This will helpto avoid conflict with django template tag
  $interpolateProvider.startSymbol('[{');
  $interpolateProvider.endSymbol('}]');
});

set_default_token_value = function($rootScope){
	$rootScope.auth_token = null;
}

get_http_header = function($cookies){
  	headers = {
   		"Content-Type": "application/json",
 	}

    var userToken = localStorage.getItem("c_token");
    if (userToken == null) {
        return(headers);
    }else{
        headers.Authorization = "Token " + userToken
    }
  	return(headers);
}

already_logged_in =  function($cookies){
    var userToken = localStorage.getItem("c_token");
    if (  userToken === undefined || userToken === "undefined"  ||  userToken === null) {
        return false;
    } else {
          return true;
    }

}

app.controller('loginController', function ($scope, $http, $rootScope, $cookies) {
    
    $scope.initialize_login_controller = function(){
        //this is required once in real case
        // if(already_logged_in($cookies)) {
        //      window.location.replace("/");
        // }
    };

    $scope.authenticate_app = function(){
		var data = {};
		$scope.login_error_status = false;
    	data.username = $scope.username;
    	data.password = $scope.password;
        loginValidation(data, $cookies);
	};

    
	function loginValidation (userData, $cookies) {
       
		var headers = get_http_header($cookies)
		$http({
		  method: 'POST',
		  url: '/auth_login',
		  headers: headers,
		  data:userData,
		}).then(function (data) {
			if(data.status == 200){
				$scope.login_error_status = false;
                localStorage.setItem("c_token", data.data.token);
                window.location.replace("/");

				}
	    }, function (error) {
	    	$scope.login_error_status = true;
	    });
	 };

});



app.controller("adminController", function($scope,$http, $rootScope, $cookies,$mdDialog) {

    $scope.initializeAdminController = function(){
        $scope.show_add_employee_form = false; 
        $scope.hide_add_employee_button = false;
        $scope.grades = ['Grade-1','Grade-2','Grade-3','Grade-4','Grade-5','Grade-6','Grade-7'];
    };

    $scope.logout = function ($cookies) {
        localStorage.setItem("c_token", undefined);
        window.location.replace("/login");
    };

    $scope.addEmployee = function(){
        $scope.show_add_employee_form = true;
        $scope.hide_add_employee_button = true;
        $scope.new_employee =  {};
        $scope.new_employee.grades = [];
        $scope.new_employee.assignments = [];
    };
    
    $scope.changeGrade = function(grade) {
        var index_of_grade = $scope.new_employee.grades.indexOf(grade); 
        if(index_of_grade === -1) {
            $scope.new_employee.grades.push(grade);
        } else {
            $scope.new_employee.grades.splice(index_of_grade, 1)
        }
    }
    
    $scope.addAssignment  = function(){
        $scope.assignment = {};   
    }

    $scope.assignAssignment = function(){
            $scope.new_employee.assignments.push($scope.assignment);
            $('#AssignmentModal').modal('hide');
            console.log($scope.new_employee);
    }

    function createNewJobInfo (jobData,$cookies) {
        console.log($scope.job);
        var headers = get_http_header($cookies);
        // jobData.job_url = jobData.url.url;
        $http({
          method: 'POST',
          url: '/jobs',
          headers: headers,
          data:jobData,
        }).then(function (data) {
            if(data.status == 201){
                $scope.get_job_list_view();
                var modal=angular.element($('#myJobModal'));
                modal.modal('hide');
                $scope.job = {};
                $scope.newtasks = [];
                $scope.tasks = [];
                $scope.changeCollapse(jobData.stage);
            }
        }, function (error) {
            if(error.status == 401){
                localStorage.setItem("c_token", undefined);
                window.location.replace("/login");
            }
        });
     };

    

    $scope.deleteJobInfo = function(jobId) {
        var headers = get_http_header($cookies);

        $http({
          method: 'DELETE',
          url: '/job/'+jobId,
          headers: headers,
          data:{'jobId' : jobId}
        }).then(function (data) {
            if(data.status == 204){
                $('#thisJob').modal('hide');
                $scope.get_job_list_view();
                }
        }, function (error) {
            if(error.status == 401){
                localStorage.setItem("c_token", undefined);
                window.location.replace("/login");

            }
            console.log('error',error);
        });
     };

    
    
    

    
    

    

    
    

    

    

});