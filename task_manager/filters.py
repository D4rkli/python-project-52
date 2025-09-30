import django_filters
from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Task
from statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=Status.objects.all().order_by("id"),
        label="Статус",
        widget=forms.Select
            (attrs={
            "class": "form-select",
            "aria-label": "Статус",
            },
        ),
    )

    executor = django_filters.ModelChoiceFilter(
        field_name="executor",
        queryset=User.objects.all().order_by("id"),
        label="Исполнитель",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": "Исполнитель",
            },
        ),
    )

    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all().order_by("id"),
        label="Метка",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "aria-label": "Метка",
            },
        ),
    )

    self_tasks = django_filters.BooleanFilter(
        method="filter_self",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
            "id": "id_self_tasks",
        }),
    )

    class Meta:
        model = Task
        fields = ("status", "executor", "labels")

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(
            data=data,
            queryset=queryset,
            request=request,
            prefix=prefix
        )
        self.form.label_suffix = ""

    def filter_self(self, qs, name, value):
        if value and self.request.user.is_authenticated:
            return qs.filter(author=self.request.user)
        return qs
