from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,  authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import View
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import ( UserSerializer,EmployeeSerializer,DaySerializer,GradeSerializer,AssignmentSerializer)
from .models import Assignment,Day,Grade,Admin,Employee
from django.shortcuts import render_to_response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status 
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from urllib.request import urlopen
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import string
import random
import requests
import re
import json
import base64
import os
import urllib.parse as urlparse
from django.conf import settings
import datetime
import sys;
import hashlib
from django.db.models import Q
from itertools import chain

DRIVER = settings.BASE_DIR+'/chrome_server/chromedriver'

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def auth_login(request):
	username = request.data.get("username")
	password = request.data.get("password")
	user = authenticate(username=username, password=password)

	if not user:
		return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)
	token, created = Token.objects.get_or_create(user=user)
	return Response({"token": token.key,"admin":user.is_superuser})



@authentication_classes([TokenAuthentication])
@permission_classes([])
def login(request):   
    return render_to_response('login.html', locals())  

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def adminpage(request):
    return render_to_response('adminpage.html',locals())

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def employeepage(request):
    return render_to_response('home.html',locals())

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class Employee(generics.ListCreateAPIView):
    """
    List all employee, or create a new employee.
    
    """
    # permission_classes = (IsAuthenticated,)
    # serializer_class = EmployeeSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateEmployee(generics.ListCreateAPIView):
    """
    List all employee, or create a new employee.
    
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,**kwargs):
    	# user_serializer = UserSerializer(data=request.data)
    	# if user_serializer.is_valid():
    	# 	# user_serializer.save()
    	# 	request.data.update({'user':user_serializer.data})
    	print(request.data)
    	emp_serializer = EmployeeSerializer(data=request.data)
    	if emp_serializer.is_valid():
    		emp_serializer.save()
    		print(emp_serializer.data)
    		return Response(emp_serializer.data)
    	return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    	# return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetDays(generics.ListCreateAPIView):
	"""
    List all days
    
    """
	permission_classes = (IsAuthenticated,)
	serializer_class = DaySerializer
	queryset = Day.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetGrades(generics.ListCreateAPIView):
	"""
    List all grades
    
    """
	permission_classes = (IsAuthenticated,)
	serializer_class = GradeSerializer
	queryset = Grade.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SearchEmployee(generics.ListCreateAPIView):
    """
    List all employee.
    
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        days_string = request.GET['days']
        grades_string = request.GET['grades']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        start_date = datetime.datetime.strptime(start_date,"%m/%d/%Y" ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date,"%m/%d/%Y" ).strftime("%Y-%m-%d")
        if not days_string:
        	days =[]
        else:
        	days =  days_string.split(',')
        if not grades_string:
        	grades = []
        else:
        	grades = grades_string.split(',')
        print(days,grades)
        if  days and grades:
        	employees = Employee.objects.filter(days__in=days).filter(grades__in=grades).distinct()
        elif not days and grades:
        	employees = Employee.objects.filter(grades__in=grades).distinct()
        elif not grades and days:
        	employees = Employee.objects.filter(days__in=days).distinct()
        else:
        	employees = Employee.objects.all().distinct()
        free_employees = []
        for employee in employees:
        	print(employee)
        	assignments = employee.assignments.all()
        	if assignments:
        		invalid_assignments = employee.assignments.filter(~(Q(start_date__gt=end_date)| Q(end_date__lt=start_date)))
        		# invalid_assignments = employee.assignments.exclude(id__in=valid_assignments)
        		if not invalid_assignments:
        			free_employees.append(employee)
        	else:
        		free_employees.append(employee)
        emp_serializer = EmployeeSerializer(free_employees,many=True)
        return Response(emp_serializer.data)

        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class EmployeeInfo(generics.ListCreateAPIView):

	permission_classes = (IsAuthenticated,)
	serializer_class = EmployeeSerializer

	def get(self, request, pk, *args, **kwargs):
		try:
			employee = Employee.objects.get(pk=pk)
			emp_serializer = EmployeeSerializer(employee)
			return Response(emp_serializer.data)	
		except Employee.DoesNotExist:
			raise Http404

	def put(self, request, pk,*args, **kwargs):
		employee = Employee.objects.get(pk=pk)
		request.data.pop('user')
		assignments = request.data.get('assignments')
		for assignment in assignments:
			assignment['start_date'] = datetime.datetime.strptime(assignment['start_date'],"%m/%d/%Y" ).strftime("%Y-%m-%d")
			assignment['end_date'] = datetime.datetime.strptime(assignment['end_date'],"%m/%d/%Y" ).strftime("%Y-%m-%d")
		emp_serializer = EmployeeSerializer(employee, data=request.data)
		if emp_serializer.is_valid():
			emp_serializer.save()
			return Response(emp_serializer.data)
		return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




