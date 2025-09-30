from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.labels.models import Label

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        label="Исполнитель",
        required=False,
        queryset=User.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_executor",
            "aria-label": "Исполнитель",
        }),
    )

    labels = forms.ModelMultipleChoiceField(
        label="Метки",
        required=False,
        queryset=Label.objects.none(),
        widget=forms.SelectMultiple(attrs={
            "class": "form-select",
            "aria-label": "Метки",
        }),
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

        self.fields["executor"].queryset = User.objects.order_by("id")
        self.fields["labels"].queryset = Label.objects.order_by("id")

        def user_label(u: User) -> str:
            full = (u.get_full_name() or "").strip()
            return full or u.username

        self.fields["executor"].label_from_instance = user_label
        self.fields["executor"].empty_label = "---------"