from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User

User = get_user_model()

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

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Лейблы
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        # Валидация длины пароля (если в settings не включили валидаторы)
        self.fields['password1'].validators.append(MinLengthValidator(8))
        self.fields['password2'].validators.append(MinLengthValidator(8))

        # Подсказки
        self.fields['password1'].help_text = 'Ваш пароль должен содержать как минимум 8 символов.'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'

        # Bootstrap + плейсхолдеры
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control', 'placeholder': f.label})

class SignUpForm(UserCreationForm):
    def clean_password1(self):
        p1 = self.cleaned_data.get('password1') or ''
        if len(p1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        return p1
