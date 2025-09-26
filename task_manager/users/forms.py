from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, UsernameField
)
from django.core.validators import MinLengthValidator

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "placeholder": "Имя пользователя",
            "class": "form-control",
        })
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Пароль",
            "class": "form-control",
        })
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя', required=False,
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label='Фамилия', required=False,
        widget=forms.TextInput()
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput()
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
