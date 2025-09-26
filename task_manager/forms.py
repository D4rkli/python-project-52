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


class SignUpForm(UserCreationForm):
    ...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        for name, ph in placeholders.items():
            self.fields[name].widget.attrs.update({"placeholder": ph, "class": "form-control"})

