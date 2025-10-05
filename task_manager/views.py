from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.http import HttpResponse


User = get_user_model()


def home(_request):
    return HttpResponse("Hello from Task Manager! 👋")


class HomeView(TemplateView):
    template_name = 'index.html'


def rollbar_test_view(_request):
    raise RuntimeError("Rollbar test: boom from production!")