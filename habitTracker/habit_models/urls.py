from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'habits', HabitProgressViewSet, basename='habit-progress')
router.register(r'habits', CalenderViewSet, basename='calender')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/logout', logoutAPI.as_view()),
    path('habits/', HabitViewSet.as_view({'get': 'fetchHabits'})),
    path('habits/create', HabitViewSet.as_view({'post': 'createHabit'})),
    path('habits/<int:id>', HabitViewSet.as_view({'get':'fetchById'})),
    path('habits/<int:id>/update', HabitViewSet.as_view({'put':'updateHabit'})),
    path('habits/<int:id>/delete', HabitViewSet.as_view({'delete':'deleteHabit'})),
    path('habits/<int:id>/track', HabitProgressViewSet.as_view({'post':'trackHabit'})),
    path('habits/progress', HabitProgressViewSet.as_view({'get':'showProgress'})),
    path('habits/<int:id>/progress', HabitProgressViewSet.as_view({'get' : 'idProgress'})),
    path('habits/calendar', CalenderViewSet.as_view({'post':'showCalender'})),
    path('habits/analytics', AnalyticsViewSet.as_view({'get':'getAnalyticsData'}))
]