from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    days = models.CharField(max_length=50, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ], default='Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday')
    good_habit = models.BooleanField(default=True)
    goal = models.CharField(max_length=250, blank=True)

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="progress_track")
    completion_dates = models.JSONField(default=dict)

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
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default = False)