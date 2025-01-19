from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Habit)
admin.site.register(HabitProgress)
admin.site.register(Streak)
admin.site.register(Analytics)
admin.site.register(Calender)