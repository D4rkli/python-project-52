from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, UsernameField,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.common import labels as L

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=L.USERNAME,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.USERNAME,
            "aria-label": L.USERNAME,
            "autofocus": True,
        })
    )
    password = forms.CharField(
        label=L.PASSWORD,
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": L.PASSWORD,
            "aria-label": L.PASSWORD,
        })
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label=L.FIRST_NAME,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.FIRST_NAME,
            "aria-label": L.FIRST_NAME,
        })
    )
    last_name = forms.CharField(
        label=L.LAST_NAME,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.LAST_NAME,
            "aria-label": L.LAST_NAME,
        })
    )
    username = forms.CharField(
        label=L.USERNAME,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.USERNAME,
            "aria-label": L.USERNAME,
        })
    )
    password1 = forms.CharField(
        label=L.PASSWORD,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": L.PASSWORD,
            "aria-label": L.PASSWORD,
            "minlength": 8,
        })
    )
    password2 = forms.CharField(
        label=L.PASSWORD_CONFIRM,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": L.PASSWORD_CONFIRM,
            "aria-label": L.PASSWORD_CONFIRM,
            "minlength": 8,
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label=L.FIRST_NAME,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.FIRST_NAME,
        }),
    )
    last_name = forms.CharField(
        label=L.LAST_NAME,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.LAST_NAME,
        }),
    )
    username = forms.CharField(
        label=L.USERNAME,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": L.USERNAME,
        }),
    )
    password1 = forms.CharField(
        label=L.PASSWORD,
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": L.PASSWORD,
        }),
    )
    password2 = forms.CharField(
        label=L.PASSWORD_CONFIRM,
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": L.PASSWORD_CONFIRM,
        }),
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
                self.add_error("password1",
                               _("Пароль должен быть не менее 8 символов."))
            if p1 != p2:
                self.add_error("password2",
                               _("Пароли не совпадают."))
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("password1")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user