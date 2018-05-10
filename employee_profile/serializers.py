from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.status import HTTP_401_UNAUTHORIZED

from django.db import transaction
from .models import Assignment
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


# class AssignmentSerializer(serializers.ModelSerializer):

#     created_at = serializers.DateTimeField(
#                 read_only=True,
#                 default=serializers.CreateOnlyDefault(datetime.now)
#     )
    
#     class Meta:
#         model = Assignment
#         fields = ('assignment_title','created_at','stage','user')

    
#     def create(self, validated_data):
#         request = self.context.get("request")
#         user = request.user
#         assignment = Assignment.objects.create(user=user,**validated_data)
#      	Task.objects.create(job=job_obj, **dic_save)
#      	return job_obj

    # def update(self,job,validated_data):
    #     job.job_title = validated_data.pop('job_title')
    #     job.deadline = validated_data.pop('deadline')
    #     job.stage = validated_data.pop('stage')
    #     tasks = Task.objects.filter(job=job)
    #     for task in tasks:
    #         task.delete()

    #     for task in validated_data.pop('tasks'):
    #         dic_save = {'action_date': task.get('action_date'), 'action': task.get('action'),'done':task.get('done')}
    #         Task.objects.create(job=job, **dic_save)
    #     job.save()
    #     return job