from django.db import models
from django.contrib.auth.models import User

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

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="progress_track")
    date = models.DateField()
    completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    streak_count = models.IntegerField(default = 0)
    last_completed = models.DateField(auto_now = True)

class Analytics(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    weekly_completion_rate = models.FloatField(default = 0)
    monthly_completion_rate = models.FloatField(default = 0)
    best_habit = models.ForeignKey(Habit, null = True, blank = True, on_delete = models.SET_NULL, related_name = "best_habit_analytics")
    worst_habit = models.ForeignKey(Habit, null = True, blank = True, on_delete = models.SET_NULL, related_name = "worst_habit_analytics")

class Calender(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateField()
    completed_habits = models.ManyToManyField(Habit)