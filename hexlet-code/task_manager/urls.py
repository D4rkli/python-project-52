from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import HomeView, rollbar_test_view
from .users import views as uviews
from .statuses import views as sviews
from .tasks import views as tviews
from .labels import views as lviews

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", HomeView.as_view(), name="home"),
    path("rollbar/test/", rollbar_test_view, name="rollbar_test"),

    path("login/",  auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("users/", uviews.UserListView.as_view(), name="users_index"),
    path("users/create/", uviews.UserCreateView.as_view(), name="users_create"),
    path("users/<int:pk>/update/", uviews.UserUpdateView.as_view(), name="users_update"),
    path("users/<int:pk>/delete/", uviews.UserDeleteView.as_view(), name="users_delete"),

    path("statuses/", sviews.StatusListView.as_view(), name="statuses_index"),
    path("statuses/create/", sviews.StatusCreateView.as_view(), name="statuses_create"),
    path("statuses/<int:pk>/update/", sviews.StatusUpdateView.as_view(), name="statuses_update"),
    path("statuses/<int:pk>/delete/", sviews.StatusDeleteView.as_view(), name="statuses_delete"),
]