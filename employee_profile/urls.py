from django.urls import path
from .views import (EmployeeInfo,GetDays,GetGrades,CreateEmployee,SearchEmployee)
from employee_profile import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('auth_login',views.auth_login,name='auth_login'),
	path('login', views.login, name='login'),
	# path('create_user', UserCreate.as_view(), name='user_view'),
	path('adminhome',views.adminpage,name='default'),
	path('home',views.employeepage,name='default'),
	path('employee/<int:pk>', EmployeeInfo.as_view(), name='employee'),
	path('search_employee',SearchEmployee.as_view(),name='search_employee'),
	path('create_employee',CreateEmployee.as_view(), name='create_employee') , 
	path('days',GetDays.as_view(),name='days'),
	path('grades',GetGrades.as_view(),name='grades'),
	

	# path('home',views.home,name='home'),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
