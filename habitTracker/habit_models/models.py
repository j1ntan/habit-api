from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(null=True)

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(max_length=50, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='daily')
    good_habit = models.BooleanField(default=True)
    goal = models.IntegerField()
    color = models.CharField(max_length=20, blank=True, null=True)

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)