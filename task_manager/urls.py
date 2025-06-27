from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, it works!")

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]

