from django.contrib.auth.forms import UserCreationForm
from django import forms
from task_manager.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'user_type')
