from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from .forms import SignUpForm, UserUpdateForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


User = get_user_model()


class AuthLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm

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


def username_to_full(username: str) -> str:
    if not username:
        return ""
    parts = username.replace("-", " ").replace("_", " ").split()
    return " ".join(p.capitalize() for p in parts)

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset().order_by("id")
        for u in qs:
            full = f"{(u.first_name or '').strip()} {(u.last_name or '').strip()}".strip()
            u.display_full_name = full if full else username_to_full(u.username)
        return qs


class UserCreateView(CreateView):
    form_class = SignUpForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class SelfOnlyMixin(UserPassesTestMixin):

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.pk == self.request.user.pk

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя")
        return redirect("users_index")


class UserUpdateView(LoginRequiredMixin, SelfOnlyMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users_index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно изменен")
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users_index")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # запрет удаления чужого пользователя + сообщение
        if self.object.pk != request.user.pk:
            messages.error(request, "У вас нет прав для изменения")
            return redirect("users_index")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Пользователь успешно удалён")
        return response