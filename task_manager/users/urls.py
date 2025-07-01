from django.urls import path
from .views import UserCreateView
from .views import UserUpdateView, UserDeleteView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
]

urlpatterns += [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]