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
from rest_framework import status
from datetime import date, timedelta, strptime

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
                    "data" : {'token' : str(Token.objects.get_or_create(user = user_obj)[0]),
                              'name' : user_obj.first_name,
                              'email' : user_obj.email,
                              'username' : user_obj.username}
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
            return Response(status = 400, data = {"error" : "password and retype_password don't match!"})
        try:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'], first_name = request.data['first_name'])
            return Response(status = 201, data = "Successful!")
        except db.utils.IntegrityError:
            return Response(status = 422, data = {"error": "username already exists!"})

class logoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'])
    def post(self, request):
        return Response({
            "status" :True,
            "message" : "Logout successful!"
        })

class HabitViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def authorize(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("token "):
            return 1
        
        token_key = auth_header.split(" ")[1]
        
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return 2
        else:
            return user
    @action(detail=False, methods=['get'])
    def fetchHabits(self, request):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            habits = Habit.objects.filter(user=user)
            serializer = HabitSerializer(habits, many=True)
            return Response({
                "status": True,
                "data": serializer.data
                })
    @action(detail=False, methods=['post'])
    def createHabit(self, request):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            new_habit = Habit(user=user, habit_name=request.data['name'], description=request.data['description'], start_date=request.data['start_date'], end_date=request.data['end_date'], frequency=request.data['frequency'], goal=request.data['goal'])
            new_habit.save()
            habit_progress = HabitProgress(habit = new_habit, completion_dates = [])
            habit_progress.save()
            streak_init = Streak(user=user, habit=new_habit)
            streak_init.save()
            return Response({
                "status": True,
                "data": HabitSerializer(new_habit).data
            })
    @action(detail=True, methods=['get'])
    def fetchById(self, request, id):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                habit = Habit.objects.get(id=id, user=user)
            except Habit.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Habit not found for the provided user."
                })
            serializer = HabitSerializer(habit)
            return Response({
                "status": True,
                "data": serializer.data
            })
    @action(detail=True, methods=['put'])
    def updateHabit(self, request, id):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                habit = Habit.objects.get(id=id, user=user)
            except Habit.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Habit not found for the provided user."
                })
            habit.habit_name = request.data['name']
            habit.description = request.data['description']
            habit.start_date = request.data['start_date']
            habit.end_date = request.data['end_date']
            habit.frequency = request.data['frequency']
            habit.goal = request.data['goal']
            habit.save()
            return Response({
                "status": True,
                "data": HabitSerializer(habit).data
            })
    @action(detail=True, methods=['delete'])
    def deleteHabit(self, request, id):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                habit = Habit.objects.get(id=id, user=user)
            except Habit.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Habit not found for the provided user."
                })
            habit.delete()
            return Response({
                "status": True,
                "data": "Habit deleted successfully"
            })
    
class HabitProgressViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def authorize(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("token "):
            return 1
        
        token_key = auth_header.split(" ")[1]
        
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return 2
        else:
            return user

    @action(detail=True, methods=['post'])
    def trackHabit(self, request, id):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                habit = Habit.objects.get(id=id, user=user)
            except Habit.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "Habit not found for the given user."
                })
            else:
                habit_progress = HabitProgress.objects.get_or_create(habit=habit)
                habit_progress.completed = request.data['completed']
                if habit_progress.completed:
                    date = request.data['date'] # date format: yyyy-mm-dd

                    # But what if the habit ends before the date? Or if it starts after start_date?
                    if not (habit.start_date <= date and date <= habit.end_date):
                        return Response({
                            "status": False,
                            "message": "Date is not within the habit's start and end date."
                        })
                    if not date in habit_progress.completion_dates:
                        habit_progress.completion_dates.append(date)
                        habit_progress.save()

                # Update streak.
                streak = Streak.objects.get(user = user, habit= habit)
                last_completed_before_update = streak.last_completed

                # Update last_completed date only if the supplied date is later than the date stored in it.
                if request.data['date'] > last_completed_before_update:
                    streak.last_completed = request.data['date']
                    streak.save()
                
                if habit_progress.completed:
                    supplied_date = strptime(request.data['date'], "%Y-%m-%d")
                    last_completed = strptime(streak.last_completed, "%Y-%m-%d")
                    if last_completed + timedelta(days=1) == supplied_date:
                        streak.streak_count += 1
                    else:
                        streak.streak_count = 1
                                
                return Response({
                    "status": True,
                    "message": "Habit progress updated successfully",
                    "data" : {
                        "progress_data" : HabitProgressSerializer(habit_progress).data,
                        "streak_data" : StreakSerializer(streak).data
                    }
                })
    
    @action(detail=True, methods=['get'])
    def showProgress(self, request):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            all_habits = Habit.objects.filter(user=user)
            all_progress = HabitProgress.objects.filter(habit__in=all_habits)
            serializer = HabitProgressSerializer(all_progress, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            })
    @action(detail=True, methods=['get'])
    def idProgress(self, request, id):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            habit = Habit.objects.get(id=id, user=user)
            progress =  HabitProgress.objects.get(habit=habit)
            serializer = HabitProgressSerializer(progress)
            return Response({
                "status" : True,
                "data" : serializer.data
            })

class CalenderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    def authorize(self, request):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("token "):
            return 1
        
        token_key = auth_header.split(" ")[1]
        
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return 2
        else:
            return user
    
    @action(detail=True, methods=['get'])
    def showCalender(self, request):
        user = self.authorize(request)
        if user == 1:
            return Response({"error": "Invalid or missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)
        elif user == 2:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            all_habits = Habit.objects.filter(user=user)
            input_date = request.data['date']
