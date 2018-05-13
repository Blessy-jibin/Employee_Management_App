from django.urls import path
from .views import (Employee,Day,Grade,CreateEmployee)
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
	path('create_employee',CreateEmployee.as_view(), name='employee') , 
	path('days',Day.as_view(),name='days'),
	path('grades',Grade.as_view(),name='grades'),
	

	# path('home',views.home,name='home'),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
