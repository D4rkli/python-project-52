from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.views.generic import TemplateView

def index(request):
    return HttpResponse("Hello, it works!")

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]

