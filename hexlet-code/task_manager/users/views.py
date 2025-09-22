from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

User = get_user_model()

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["id"]  # чтобы стабильно

class UserCreateView(CreateView):
    form_class = UserCreationForm  # стандартная форма => name="username", id="id_username"
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
        # редиректим на список пользователей
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