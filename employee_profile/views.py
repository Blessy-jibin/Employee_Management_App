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
from .serializers import ( UserSerializer)
from .models import Assignment
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
from datetime import datetime
import sys;
import hashlib


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
	return Response({"token": token.key})



@authentication_classes([TokenAuthentication])
@permission_classes([])
def login(request):   
    return render_to_response('login.html', locals())  

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def adminpage(request):
    #boards = Board.objects.all()
    return render_to_response('adminpage.html',locals())






