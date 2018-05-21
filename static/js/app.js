//angular module
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
                $rootScope.logged_in_user_id = data.data.id;
                superuser = data.data.is_admin;
                console.log('id',data.data.id);
                if(superuser){
                window.location.replace("/adminhome");
                }else{
                window.location.replace("/employeehome"); 
                }  
			}
	    }, function (error) {
	    	$scope.login_error_status = true;
	    });
	 };

});

app.controller("adminController", function($scope,$http, $rootScope, $cookies,$mdDialog,$q,$timeout) {

    $scope.initializeAdminController = function(){
        $scope.show_add_employee_form = false; 
        $scope.show_search_employees_form = false;
        getDays(); // $scope.grades is set using this function
        getGrades(); // $scope.days is set using this function
    }; 
    

    class User{
        constructor() {

            this.username = new String();
            this.password = new String() ;
            this.email = new String();
            
        }
    }
    class Employee{
        constructor() {
            this.is_admin = false;
            this.user = new User();
            this.grades  = [];
            this.days = [];
            this.assignments=[];
        }
    }

    class Assignment{
        constructor() {
            this.title = new String();
            this.description = new String();
            this.start_date  = new String();
            this.end_date = new String();
            this.status=new String();
        }
    }
    class Search{
        constructor() {
            this.grades  = [];
            this.days = [];
            this.start_date ="";
            this.end_date = "";
            
        }
    }

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
                $scope.days = day_rec;
                console.log($scope.days);
                
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
                $scope.grades = grade_rec;
                console.log($scope.grades);
            }
           
          }, function (error) {
             if(error.status == 401){
                console.log(error);
            }
            });
    }

    
    $scope.addEmployeeInit = function(){
        $scope.show_add_employee_form = true;
        $scope.show_search_employees_form = false;//hide the add Search emplloyees form 
        $scope.newEmployee =  new Employee();
    };

    $scope.searchEmployeeInit = function(){
        $scope.show_search_employees_form = true;
        $scope.show_add_employee_form = false;//hide the add Employee form
        $scope.search = new Search();
        $scope.search_invalid_dates =false;
        
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
        console.log($scope.newEmployee.days);
    }

    $scope.changeSearchGrades = function(grade_id) {
        var index_of_grade = $scope.search.grades.indexOf(grade_id); 
        if(index_of_grade === -1) {
            $scope.search.grades.push(grade_id);
        } else {
            $scope.search.grades.splice(index_of_grade, 1)
        }
        console.log($scope.search.grades);
    }
    
    $scope.changeSearchDays = function(day_id) {
        var index_of_grade = $scope.search.days.indexOf(day_id); 
        if(index_of_grade === -1) {
            $scope.search.days.push(day_id);
        } else {
            $scope.search.days.splice(index_of_grade, 1)
        }
        console.log($scope.search.days);
    }

    $scope.addAssignmentInit  = function(emp){
        $scope.assignment = new Assignment();
        $scope.assignment.status = "pending";
        $scope.selectedEmployee = new Employee();
        $scope.selectedEmployee = emp;
        assignments = $scope.selectedEmployee.assignments;
        $scope.assignment_dates_invalid = false;
        $scope.already_assignment = false;
    }

    $scope.assignAssignment = function(){
        start_date = new Date($scope.assignment.start_date);
        end_date =new Date( $scope.assignment.end_date); 
        console.log(start_date,end_date);
        if(start_date > end_date){
            $scope.assignment_dates_invalid = true;
            // alert('start_date is greater than end_date');
        }

        if(start_date <= end_date){
            $scope.assignment_dates_invalid = false;
            length = $scope.selectedEmployee.assignments.length;//check is there assignments there
            // no assignments add one
            if(length==0){
                addAssignment($scope.selectedEmployee.id,$scope.assignment);
            }
            //already assignment. check for dates
            if(length>0){
                dates = findAssignmentDates($scope.selectedEmployee.assignments);
                smallest_date = dates.smallest_date;
                largest_date = dates.largest_date;
                if(start_date>largest_date || end_date<smallest_date){
                    console.log('valid date');
                    $scope.already_assignment  = false;
                    addAssignment($scope.selectedEmployee.id,$scope.assignment);

                }else{
                    // alert('Already assignment in the time period');
                    $scope.already_assignment  = true;
                }  
            }
        }
    }
    
    $scope.createEmployee = function(){
        
        employee_data = $scope.newEmployee;
        console.log(employee_data);
        uncheckAll();
        createNewEmployee(employee_data,$cookies);
        $scope.error_creating_employee = false;
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
                uncheckAll();
                $scope.sucess_creating_employee = true;
                $timeout(function(){
                    $scope.sucess_creating_employee = false;
                }, 5000);
            }
        }, function (error) {
            if(error.status == 400){
                $scope.error_creating_employee = true;
                console.log('error',$scope.error_creating_employee);
            }
        });
     };
    

    $scope.searchEmployees = function(){
        var search_data = $scope.search;
        days = search_data.days;
        grades = search_data.grades;
        start_date = search_data.start_date;
        end_date = search_data.end_date;
        if(days.length>0){
            days = days.join(",");
            search_data.days = days;
            $scope.days_not_selected = false;
        }
        else{
            $scope.days_not_selected = true;
        }
        if(grades.length>0){
            grades = grades.join(",");
            search_data.grades = grades;
            $scope.grades_not_selected = false;
        }
        else{
            $scope.grades_not_selected = true;
        }
        if( new Date(end_date) >= new Date(start_date) )
        {
            $scope.search_invalid_dates = false;
        }else{
            $scope.search_invalid_dates = true;
        }
        if(new Date(end_date) >= new Date(start_date) && days.length>0 && grades.length>0){
            getEmployees(search_data,$cookies);
            uncheckAll();
        }
    }

    function getEmployees(search_data,$cookies) {
        $scope.all_emp = [];
        var headers = get_http_header($cookies);
        $http({
          method: 'GET',
          url: '/search_employee',
          headers: headers,
          params: search_data,
        }).then(function (data) {
            if(data.status == 200){
                 $scope.show_search_employees_form = false; 
                 uncheckAll();
                $scope.emp = data.data;
            }
        }, function (error) {
            if(error.status == 400){
                
            }
        });
    };

    $scope.getAllEmployees =function($cookies){
        var headers = get_http_header($cookies);
        $scope.emp = [];
        $http({
          method: 'GET',
          url: '/all_employees',
          headers: headers,
        }).then(function (data) {
            if(data.status == 200){
                $scope.all_emp = data.data;
                $scope.show_search_employees_form = false;
            }
        }, function (error) {
            if(error.status == 400){
                
            }
        });

    }
    
    function uncheckAll() {
      angular.forEach($scope.grades, function (grade) {
         grade.Selected = false;
        });
      angular.forEach($scope.days, function (day) {
         day.Selected = false;
        });
    };

    findAssignmentDates = function(assignments){
        dates=[];
        for(i in assignments){
            dates.push(new Date(assignments[i].start_date));
            dates.push(new Date(assignments[i].end_date));
        }
        max_date = new Date(Math.max.apply(null,dates));
        min_date  = new Date(Math.min.apply(null,dates));
        return {'smallest_date':min_date , 'largest_date':max_date};
    }

    function updateEmployee(id,employee_data){
        var headers = get_http_header($cookies);
        console.log(employee_data);
        $http({
          method: 'PUT',
          url: '/employee/'+id ,
          headers: headers,
          data: employee_data,
        }).then(function (data) {
            if(data.status == 200){
                 console.log(data.data);

                 $('#AssignmentModal').modal('hide');
                 
            }
        }, function (error) {
            if(error.status == 401){
                
            }
        });


    };

    function addAssignment(id,assignment){
        var headers = get_http_header($cookies);
        data = {};
        data.employee_id = id;
        data.assignment = assignment;
        $http({
          method: 'POST',
          url: '/assignment',
          headers: headers,
          data: data,
        }).then(function (data) {
            if(data.status == 200){
                 console.log(data.data);
                 $scope.selectedEmployee.assignments.push($scope.assignment);
                 $('#AssignmentModal').modal('hide');
                 
            }
        }, function (error) {
            if(error.status == 401){
                
            }
        });



    };

});

app.controller("employeeController", function($scope,$http, $rootScope, $cookies,$mdDialog,$q) {
    
    $scope.initializeEmployeeController = function(){
        getEmployeeInfo();
        
    }; 

    function getEmployeeInfo(){

        var headers = get_http_header($cookies);
        $http({
          method: 'GET',
          url: '/employeeinfo',
          headers: headers,
        }).then(function (data) {
            if(data.status == 200){
                data = data.data;
                $scope.emp =data[0];
                console.log($scope.emp);
            }
        }, function (error) {
            if(error.status == 401){
                
            }
        });
    } 



    $scope.acceptAssignment = function(assignment){
        console.log('accpet button clicked');
        updated_assignment = angular.copy(assignment);
        updated_assignment.status = "accepted";
        updateAssignment(assignment,updated_assignment);
    };

    $scope.declineAssignment = function(assignment){
        console.log('decline buton clicked');
         updated_assignment = angular.copy(assignment);
         updated_assignment.status = "declined";
        updateAssignment(assignment,updated_assignment);
    };

    $scope.logout = function ($cookies) {
        localStorage.setItem("c_token", undefined);
        window.location.replace("/login");
    };

    function updateAssignment(assignment,updated_assignment){
        var headers = get_http_header($cookies);
        data = updated_assignment;
        console.log(data);
        $http({
          method: 'PUT',
          url: '/assignment',
          headers: headers,
          data: data,
        }).then(function (data) {
            if(data.status == 200){
                assignment.status = data.data.status;
                console.log(',,',assignment);
                
            }
        }, function (error) {
            if(error.status == 401){
                
            }
        });
    };    
});