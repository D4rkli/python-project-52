from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="Тип пользователя")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


