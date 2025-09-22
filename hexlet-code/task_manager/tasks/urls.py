from .views import TaskListView
from django.urls import path

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
]