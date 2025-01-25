from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import db
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Create your views here.  
class AuthenticationViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            })
        if not "email" in serializer.data and not "username" in serializer.data:
            return Response({
                "status" : False,
                "message" : "At least one of username or email is required."
            })
        if "username" in serializer.data:
            username = serializer.data["username"]
            password = serializer.data["password"]
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                return Response({
                    "status" : True,
                    "data" : {'token' : str(Token.objects.get_or_create(user = user_obj)[0])}
                })
            return Response({
                "status" : False,
                "data" : {},
                "message" : "Invalid Credentials"
            })
        else:
            try:
                user = User.objects.get(email=serializer.data['email'])
            except User.DoesNotExist:
                return Response({
                "status" : False,
                "data" : {},
                "message" : "Invalid Credentials"
            })
            else:
                user_obj = authenticate(username=user.username, password=serializer.data['password'])
                if user_obj:
                    return Response({
                        "status" : True,
                        "data" : {'token' : str(Token.objects.get_or_create(user = user_obj)[0])}
                    })
                return Response({
                    "status" : False,
                    "data" : {},
                    "message" : "Invalid Credentials"
                })
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        if request.data['password'] != request.data['retype_password']:
            return Response(status = 400, data = "Error: password and retype_password don't match!")
        try:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'])
            return Response(status = 201, data = "Successful!")
        except db.utils.IntegrityError:
            return Response(status = 422, data = "Error: username already exists!")

class logoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({
            "status" :True,
            "message" : "Logout successful!"
        })