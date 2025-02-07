from .models import *
from rest_framework import serializers

class HabitSerializer(serializers.ModelSerializer):
    days = serializers.PrimaryKeyRelatedField(queryset=Day.objects.all(), many=True)
    class Meta:
        model = Habit
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=False)

class HabitProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitProgress
        fields = '__all__'

class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = '__all__'