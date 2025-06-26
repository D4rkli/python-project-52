from django.urls import path
from task_manager.views import HomePageView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
]