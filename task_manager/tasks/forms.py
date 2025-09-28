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
            "name": forms.TextInput(attrs={"class": "form-control", "aria-label": "Имя"}),
            "description": forms.Textarea(attrs={"class": "form-control", "aria-label": "Описание"}),
            "status": forms.Select(attrs={"class": "form-select", "aria-label": "Статус"}),
            "executor": forms.Select(attrs={"class": "form-select", "id": "id_executor", "aria-label": "Исполнитель"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-select", "aria-label": "Метки"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""                           # <— важное
        self.fields["executor"].label_from_instance = lambda u: u.username
        self.fields["executor"].required = False
