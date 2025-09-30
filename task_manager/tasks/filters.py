import django_filters
from django import forms
from django.contrib.auth import get_user_model

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
        field_name="self_tasks",
        widget=forms.CheckboxInput(attrs={
            "id": "id_self_tasks",
            "class": "form-check-input",
        }),
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all().order_by("id"),
        label="Статус",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all().order_by("id"),
        label="Исполнитель",
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all().order_by("id"),
        label="Метка",
    )


    class Meta:
        model = Task
        fields = ("status", "executor", "labels", "self_tasks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def user_label(u: User) -> str:
            full = (u.get_full_name() or "").strip()
            return full or u.username
        self.form.fields["executor"].label_from_instance = user_label

        self.form.fields["self_tasks"].required = False

    def filter_self_tasks(self, queryset, name, value):
        return queryset.filter(author=self.request.user) if value else queryset
