

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
                window.location.replace("/adminhome");

				}
	    }, function (error) {
	    	$scope.login_error_status = true;
	    });
	 };

});



app.controller("adminController", function($scope,$http, $rootScope, $cookies,$mdDialog,$q) {

    $scope.initializeAdminController = function(){
        $scope.show_add_employee_form = false; 
        $scope.hide_add_employee_button = false;
        getDays(); // $scope.grades is set using this function
        getGrades(); // $scope.days is set using this function
    }; 
    
    $scope.logout = function ($cookies) {
        localStorage.setItem("c_token", undefined);
        window.location.replace("/login");
    };

    function getDays(){
        headers = get_http_header($cookies)
        $http({
            method: 'GET',
            url: '/days',
            headers: headers,
          }).then(function (data) {
              if(data.status == 200){
                var day_rec = data.data;
                days = [];
                for (i in  day_rec) {
                    days.push(day_rec[i].day);
                }
                $scope.days = days;
            }
           
          }, function (error) {
             if(error.status == 401){
                console.log(error);
            }
            });
    }

    function getGrades(){
        headers = get_http_header($cookies)
        $http({
            method: 'GET',
            url: '/grades',
            headers: headers,
          }).then(function (data) {
              if(data.status == 200){
                var grade_rec = data.data;
                grades = [];
                for (i in  grade_rec) {
                    grades.push(grade_rec[i].grade);
                }
                $scope.grades = grades;
            }
           
          }, function (error) {
             if(error.status == 401){
                console.log(error);
            }
            });
    }

    class Employee{
        constructor() {
            this.is_admin = false;
            this.username = new String();
            this.password = new String() ;
            this.email = new String();
            this.grades  = [];
            this.days = [];
        }
    }

    $scope.addEmployee = function(){
        $scope.show_add_employee_form = true;
        $scope.hide_add_employee_button = true;
        $scope.newEmployee =  new Employee();
    };
    

    $scope.changeEmployeeGrades = function(grade) {
        var index_of_grade = $scope.newEmployee.grades.indexOf(grade); 
        if(index_of_grade === -1) {
            $scope.newEmployee.grades.push(grade);
        } else {
            $scope.newEmployee.grades.splice(index_of_grade, 1)
        }
    }
    
    $scope.changeEmployeeDays = function(day) {
        var index_of_day = $scope.newEmployee.days.indexOf(day); 
        if(index_of_day === -1) {
            $scope.newEmployee.days.push(day);
        } else {
            $scope.newEmployee.days.splice(index_of_day, 1);
        }
    }

    $scope.addAssignment  = function(){
        $scope.assignment = {};   
    }

    $scope.assignAssignment = function(){
            $scope.newEmployee.assignments.push($scope.assignment);
            $('#AssignmentModal').modal('hide');
    }
    
    $scope.createEmployee = function(){
        
        employee_data = $scope.newEmployee;
        day_lis = employee_data.days;
        grade_lis = employee_data.grades;
        days = [];
        grades = [];
        for (i in day_lis){
            dic = {}
            dic['day'] = day_lis[i];
            days.push(dic);
        }
        for (i in grade_lis){
            dic = {}
            dic['grade'] = grade_lis[i];
            grades.push(dic);
        }
        employee_data.days = days;
        employee_data.grades = grades;
        createNewEmployee(employee_data,$cookies);
    }

    function createNewEmployee(employee_data,$cookies) {
        
        var headers = get_http_header($cookies);
        $http({
          method: 'POST',
          url: '/create_employee',
          headers: headers,
          data:employee_data,
        }).then(function (data) {
            if(data.status == 200){
                $scope.show_add_employee_form = false;
                $scope.hide_add_employee_button = false;
            }
        }, function (error) {
            if(error.status == 401){
                
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

