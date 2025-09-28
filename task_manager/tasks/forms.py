from django import forms
from .models import Task

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
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Описание"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "executor": forms.Select(attrs={"class": "form-select"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
