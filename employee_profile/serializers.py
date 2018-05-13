from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.status import HTTP_401_UNAUTHORIZED

from django.db import transaction
from .models import Assignment,Employee,Admin,Day,Grade
import hashlib

import requests
import re
import json
import base64
import os
import urllib.parse as urlparse
from django.conf import settings
from datetime import datetime
# from selenium import webdriver
import sys;

DRIVER = settings.BASE_DIR+'/chrome_server/chromedriver'



class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields=('grade',)

class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day
        fields=('day',)

class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields =('is_admin','days','grades','user')
        days = DaySerializer(many=True)
        grades = GradeSerializer(many=True)

    days = DaySerializer(many=True)
    grades = GradeSerializer(many=True)

    def create(self,validated_data):
        emp = validated_data
        days = emp.pop('days')
        grades = emp.pop('grades')
        employee = Employee(user=user,**emp)
        employee.save()
        day_lis =[]
        garde_lis= []
        for day in days:
            d = Day.objects.get(day=day['day'])
            day_lis.append(d)
        for grade in grades:
            g = Grade.objects.get(grade=grade['grade'])
            garde_lis.append(g)
        employee.days.set(day_lis)
        employee.grades.set(garde_lis)
        return employee

        
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'employee')
#         extra_kwargs = {'password': {'write_only': True}}

#     employee =  EmployeeSerializer(write_only=True)

#     def create(self, validated_data):
#         user = User(
#             email = validated_data.pop("email"),
#             username = validated_data.pop("username")
#         )
#         user.set_password(validated_data.pop("password"))
#         user.save()
#         emp = validated_data.pop('employee')
#         days = emp.pop('days')
#         grades = emp.pop('grades')
#         new_employee = Employee(user=user,**emp)
#         new_employee.save()
#         day_lis =[]
#         garde_lis= []
#         for day in days:
#             d = Day.objects.get(day=day['day'])
#             day_lis.append(d)
#         for grade in grades:
#             g = Grade.objects.get(grade=grade['grade'])
#             garde_lis.append(g)
#         new_employee.days.set(day_lis)
#         new_employee.grades.set(garde_lis)
#         return user  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        user = User(
            email = validated_data.pop("email"),
            username = validated_data.pop("username")
        )
        user.set_password(validated_data.pop("password"))
        user.save()
        
        return user  

    

        

    

