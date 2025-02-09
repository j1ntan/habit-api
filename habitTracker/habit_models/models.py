from django.db import models
from django.contrib.auth.models import User

class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    days = models.ManyToManyField(Day)
    good_habit = models.BooleanField(default=True)
    goal = models.CharField(max_length=250, blank=True)

class HabitProgress(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="progress_track")
    completion_dates = models.JSONField(default=list)

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    streak_count = models.IntegerField(default = 0)
    last_completed = models.DateField(auto_now = True)

class Analytics(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE)
    habit_completion_rate = models.FloatField(default = 0)
   
class Calender(models.Model):
    habit = models.ForeignKey(Habit, on_delete = models.CASCADE, null=True, blank=True)
    date = models.DateField()
    completed = models.BooleanField(default = False)

def create_days():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        Day.objects.get_or_create(name=day)
    for day in Day.objects.all():
        print(day.name)