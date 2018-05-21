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
import sys

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields=('grade','id')

class DaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Day
        fields=('day','id')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password','id')
        extra_kwargs = {'password': {'write_only': True},'id':{'read_only':True}}

    
    def create(self, validated_data):
        user = User(
            email = validated_data.pop("email"),
            username = validated_data.pop("username")
        )
        user.set_password(validated_data.pop("password"))
        user.save()
        
        return user  

class AssignmentSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Assignment
        fields =('title','description','start_date','end_date','status','id',)
        extra_kwargs = {'id':{'read_only':True}}



    def update(self,assignment_id,validated_data):
        assignment = Assignment.objects.get(pk=assignment_id)
        title = validated_data.pop('title')    
        description = validated_data.pop('description')
        start_date = validated_data.pop('start_date')
        end_date = validated_data.pop('end_date')
        status = validated_data.pop('status')
        assignment.status = status
        assignment.title = title
        assignment.description = description
        assignment.start_date = start_date
        assignment.end_date = end_date
        assignment.save()
        return assignment

class EmployeeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields =('id','user','is_admin','days','grades','assignments')
        extra_kwargs = {'is_admin': {'write_only': True},'id':{'read_only':True}}
    days = DaySerializer(many=True,required=False)
    grades = GradeSerializer(many=True,required=False)
    assignments = AssignmentSerializer(many=True,required=False)
    user =  UserSerializer(required=False)

    def create(self,validated_data):
        emp = validated_data
        days = emp.pop('days')
        grades = emp.pop('grades')
        user_dic = emp.pop('user')
        assignments = emp.pop('assignments')
        user = User(username=user_dic.pop('username'),email=user_dic.pop('email'))
        user.set_password(user_dic.pop('password'))
        user.save()
        employee = Employee(user=user,**emp)
        employee.save()
        day_lis =[]
        grade_lis= []
        for day in days:
            d = Day.objects.get(day=day['day'])
            day_lis.append(d)
        for grade in grades:
            g = Grade.objects.get(grade=grade['grade'])
            grade_lis.append(g)
        employee.days.set(day_lis)
        employee.grades.set(grade_lis)
        employee.save()
        return employee

    def update(self,employee,validated_data):
          
        return employee



    

        

    

