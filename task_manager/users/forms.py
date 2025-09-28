from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя пользователя",
            "aria-label": "Имя пользователя",
            "autofocus": True,
        })
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль",
            "aria-label": "Пароль",
        })
    )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя', required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'aria-label': 'Имя',
        })
    )
    last_name = forms.CharField(
        label='Фамилия', required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'aria-label': 'Фамилия',
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'aria-label': 'Имя пользователя',
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'aria-label': 'Пароль',
            'minlength': 8,
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'aria-label': 'Подтверждение пароля',
            'minlength': 8,
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"})
    )
    last_name = forms.CharField(
        label="Фамилия",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Фамилия"})
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"})
    )
    password1 = forms.CharField(
        label="Пароль",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтверждение пароля"})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1") or ""
        p2 = cleaned.get("password2") or ""
        if p1 or p2:
            if len(p1) < 8:
                self.add_error("password1", "Пароль должен быть не менее 8 символов.")
            if p1 != p2:
                self.add_error("password2", "Пароли не совпадают.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("password1")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user