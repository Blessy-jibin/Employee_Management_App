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
from django.conf import settings
import datetime
import hashlib
from django.db.models import Q , Count
from itertools import chain

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
	return Response({"token": token.key,"is_admin":user.is_superuser})



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
    return render_to_response('employeepage.html',locals())

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateEmployee(generics.ListCreateAPIView):
    """
    Create a new employee.
    
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,**kwargs):
    	
    	emp_serializer = EmployeeSerializer(data=request.data)
    	if emp_serializer.is_valid():
    		emp_serializer.save()
    		print(emp_serializer.data)
    		return Response(emp_serializer.data)
    	return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    	

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
class GetAllEmployees(generics.ListCreateAPIView):
	"""
    List all employees
    
    """
	permission_classes = (IsAuthenticated,)
	serializer_class = EmployeeSerializer
	queryset = Employee.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LoggedInEmployeeInfo(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = EmployeeSerializer

	def get_queryset(self):
		print ("Reached")
		try:
			return Employee.objects.filter(user=self.request.user)
		except Employee.DoesNotExist:
			raise Http404

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SearchEmployee(generics.ListCreateAPIView):
    """
    Serach employee
    
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        days_string = request.GET['days']
        grades_string = request.GET['grades']
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        today = datetime.datetime.now()
        if start_date :
        	start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d" ).strftime("%Y-%m-%d")
        else:
        	start_date  = today
        if end_date :
        	end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d" ).strftime("%Y-%m-%d")
        else:
        	end_date = today
        days =  days_string.split(',')
        grades = grades_string.split(',')
        print(grades)
        employees = Employee.objects.filter(days__in=days,grades__in=grades).annotate(num_days=Count('days',distinct=True),num_grades=Count('grades',distinct=True)).filter(num_days=len(days),num_grades=len(grades))
        employees = sorted(employees, key = lambda x: x.id) #sorting employess accoring to creation
        free_employees = [] #employees with assignment
        employees_without_assignment = [] #employees without any assignment
        for employee in employees:
        	assignments = employee.assignments.all()
        	if assignments:
        		#check if emplyee has already assignment in the time period
        		invalid_assignments = employee.assignments.filter(~(Q(start_date__gt=end_date)| Q(end_date__lt=start_date)))
        		if not invalid_assignments:
        			#if not any assignment in the time period
        			free_employees.append(employee)
        	else:
        		employees_without_assignment.append(employee)
        free_employees = free_employees + employees_without_assignment
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
		if emp_serializer.is_valid():
			emp_serializer.save()
			return Response(emp_serializer.data)
		return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class Assignments(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AssignmentSerializer

	def post(self,request):
		employee_id = request.data.pop('employee_id')
		employee = Employee.objects.get(id=employee_id)
		assignment = request.data.get('assignment')
		assig_serializer = AssignmentSerializer(data=assignment)
		if assig_serializer.is_valid():
			assignment = assig_serializer.data
			Assignment.objects.create(employee=employee,**assignment)
			return Response(assig_serializer.data)
		else:
			return Response(assig_serializer.error, status=status.HTTP_400_BAD_REQUEST)

	def put(self,request,*args, **kwargs):
		assignment_id = request.data.get('id')
		assig_serializer = AssignmentSerializer(assignment_id,data=request.data)
		if assig_serializer.is_valid():
			assig_serializer.save()
			return Response(assig_serializer.data)
		else:
			return Response(assig_serializer.error, status=status.HTTP_400_BAD_REQUEST)

