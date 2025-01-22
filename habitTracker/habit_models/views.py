from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import db
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['POST'])
def signup(request):
    if request.data['password'] != request.data['retype_password']:
        return Response(status = 400, data = "Error: password and retye_password don't match!")
    try:
        user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'])
        return Response(status = 201, data = "Successful!")
    except db.utils.IntegrityError:
        return Response(status = 422, data = "Error: username already exists!")

@api_view(['POST'])
def login(request):
    if 'username' in request.data:
        user = authenticate(username = request.data['username'], password = request.data['password'])
    elif 'email' in request.data:
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response(data = 'User does not exist!', status = 401)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'Message' : 'Login successful!'})
    else:
        return Response(status = 400, data = "Error: User does not exist!")