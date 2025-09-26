from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Имя пользователя",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        help_texts = {
            "username": "Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_ .",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            "class": "form-control", "placeholder": "Имя"
        })
        self.fields["last_name"].widget.attrs.update({
            "class": "form-control", "placeholder": "Фамилия"
        })
        self.fields["username"].widget.attrs.update({
            "class": "form-control", "placeholder": "Имя пользователя"
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control", "placeholder": "Пароль", "minlength": 8
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control", "placeholder": "Подтверждение пароля", "minlength": 8
        })


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"})
    )
