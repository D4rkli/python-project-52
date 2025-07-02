from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/registration_form.html'
    success_url = reverse_lazy('login')

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk