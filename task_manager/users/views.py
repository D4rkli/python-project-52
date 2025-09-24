from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.deletion import ProtectedError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import LoginForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


User = get_user_model()

class AuthLoginView(LoginView):
    template_name = "users/login.html"
    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("home")

class AuthLogoutView(LogoutView):
    next_page = reverse_lazy("home")
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["id"]

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "User was registered successfully")
        return super().form_valid(form)

class SelfOnlyMixin(UserPassesTestMixin):
    """Разрешаем update/delete только самому себе."""
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.pk == self.request.user.pk

    def handle_no_permission(self):
        messages.error(self.request, "You have no rights to modify another user")
        from django.shortcuts import redirect
        return redirect("users_index")

class UserUpdateView(LoginRequiredMixin, SelfOnlyMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "email"]
    template_name = "users/update.html"
    success_url = reverse_lazy("users_index")

    def form_valid(self, form):
        messages.success(self.request, "User was updated successfully")
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, SelfOnlyMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_index")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(self.request, "User was deleted successfully")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, "Cannot delete user because it is in use")
            return redirect("users_index")