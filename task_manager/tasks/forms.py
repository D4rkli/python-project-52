from django import forms
from django.contrib.auth import get_user_model

from .models import Task
from task_manager.labels.models import Label  # ваш Label из приложения task_manager

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("id"),
        required=False,
        label="Исполнитель",
        to_field_name="username",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_executor",
                "aria-label": "Исполнитель",
            }
        ),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all().order_by("id"),
        required=False,
        label="Метки",
        to_field_name="name",
        widget=forms.SelectMultiple(
            attrs={"class": "form-select", "aria-label": "Метки"}
        ),
    )

    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "aria-label": "Имя"}),
            "description": forms.Textarea(attrs={"class": "form-control", "aria-label": "Описание"}),
            "status": forms.Select(attrs={"class": "form-select", "aria-label": "Статус"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["executor"].queryset = User.objects.all().order_by("id")
        self.fields["executor"].empty_label = "---------"
        self.fields["executor"].label_from_instance = lambda u: u.username
