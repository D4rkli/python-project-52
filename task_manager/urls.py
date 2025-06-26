from task_manager.users.views import UserListView
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", UserListView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('', include('django.contrib.auth.urls')),
]

class HomePageView(TemplateView):
    template_name = 'index.html'
