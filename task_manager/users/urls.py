from django.urls import path
from django.http import HttpResponse
from .views import UserUpdateView, UserDeleteView, UserCreateView

def profile_view(request):
    return HttpResponse("Это профиль пользователя!")

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('accounts/profile/', profile_view, name='profile'),
]

urlpatterns += [
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]