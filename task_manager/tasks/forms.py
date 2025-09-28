from django import forms
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "aria-label": "Имя"}),
            "description": forms.Textarea(attrs={"class": "form-control", "aria-label": "Описание"}),
            "status": forms.Select(attrs={"class": "form-select", "aria-label": "Статус"}),
            "executor": forms.Select(attrs={"class": "form-select", "id": "id_executor", "aria-label": "Исполнитель"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select", "aria-label": "Метки"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        # Исполнитель: гарантируем набор опций и их порядок
        self.fields["executor"].queryset = User.objects.order_by("id")
        self.fields["executor"].label_from_instance = lambda u: u.username
        self.fields["executor"].required = False
        self.fields["executor"].empty_label = "---------"

        if "labels" in self.fields:
            self.fields["labels"].queryset = self.fields["labels"].queryset.order_by("id")
        if "status" in self.fields:
            self.fields["status"].queryset = self.fields["status"].queryset.order_by("id")
