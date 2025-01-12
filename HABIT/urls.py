from . import views

from django.http import HttpRequest

def index(request):
    return HttpRequest('Test message')

