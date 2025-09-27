from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

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
        label='Имя', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        label='Фамилия', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''