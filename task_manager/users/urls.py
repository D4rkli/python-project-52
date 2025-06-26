from django.urls import path, include
from django.contrib import admin
from task_manager.users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.urls')),
    path('', include('django.contrib.auth.urls')),
]