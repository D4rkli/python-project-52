from django.urls import path
from django.http import HttpResponse
from .views import UserUpdateView, UserDeleteView, UserCreateView
from task_manager.users.views import AuthLoginView, AuthLogoutView

def profile_view(request):
    return HttpResponse("Это профиль пользователя!")

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('accounts/profile/', profile_view, name='profile'),

    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    path("login/",  AuthLoginView.as_view(),  name="login"),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
]