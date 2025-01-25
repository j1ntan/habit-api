from .models import *
from rest_framework import serializers

class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=False)