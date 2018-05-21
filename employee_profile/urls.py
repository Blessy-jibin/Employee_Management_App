from django.urls import path
from .views import (EmployeeInfo,GetDays,GetGrades,CreateEmployee,SearchEmployee,LoggedInEmployeeInfo,Assignments,GetAllEmployees)
from employee_profile import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('auth_login',views.auth_login,name='auth_login'),
	path('login', views.login, name='login'),
	path('adminhome',views.adminpage,name='default'),
	path('employeehome',views.employeepage,name='default'),
	path('employeeinfo',LoggedInEmployeeInfo.as_view(),name='employeeinfo'),
	path('employee/<int:pk>', EmployeeInfo.as_view(), name='employee'),
	path('assignment',Assignments.as_view(),name='assignment'),
	path('all_employees',GetAllEmployees.as_view(),name='all_employees'),
	path('employee',EmployeeInfo.as_view(),name='employee'),
	path('search_employee',SearchEmployee.as_view(),name='search_employee'),
	path('create_employee',CreateEmployee.as_view(), name='create_employee') , 
	path('days',GetDays.as_view(),name='days'),
	path('grades',GetGrades.as_view(),name='grades'),
	
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
