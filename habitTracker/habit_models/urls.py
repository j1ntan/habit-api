from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/logout', logoutAPI.as_view())
]

