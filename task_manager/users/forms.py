from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, ValidationError
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

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
    def clean_password1(self):
        p1 = self.cleaned_data.get('password1') or ''
        if len(p1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        return p1
