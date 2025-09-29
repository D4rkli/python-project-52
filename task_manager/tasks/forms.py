# forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.labels.models import Label

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
            "executor": forms.Select(attrs={"class": "form-select", "id": "id_executor"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select", "aria-label": "Метки"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        exec_field = self.fields["executor"] = forms.ModelChoiceField(
            queryset=User.objects.order_by("id"),
            required=False,
            label="Исполнитель",
            widget=self.Meta.widgets["executor"],
        )
        exec_field.label_from_instance = (
            lambda u: (u.get_full_name().strip() or u.username)
        )
        exec_field.empty_label = "---------"
        exec_field.to_field_name = "username"

        if "labels" in self.fields:
            self.fields["labels"].queryset = Label.objects.order_by("id")