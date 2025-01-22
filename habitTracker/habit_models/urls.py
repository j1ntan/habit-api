from django.urls import path
from .views import *

urlpatterns = [
    path('auth/signup', signup),
    path('auth/login', login)
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # For Token Auth
    ],
}