from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.labels.models import Label

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.order_by("id"),
        required=False,
        label="Исполнитель",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_executor",
                "aria-label": "Исполнитель",
            }
        ),
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.order_by("id"),
        required=False,
        label="Метки",
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
            "name": forms.TextInput({"class": "form-control", "aria-label": "Имя"}),
            "description": forms.Textarea({"class": "form-control", "aria-label": "Описание"}),
            "status": forms.Select({"class": "form-select", "aria-label": "Статус"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        def user_label(u: User) -> str:
            full = (u.get_full_name() or "").strip()
            return full if full else u.username

        self.fields["executor"].label_from_instance = user_label