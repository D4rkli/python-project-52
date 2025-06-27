from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет, мир! Ваш Django-проект работает.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]

