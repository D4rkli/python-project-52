import django_filters
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .models import Task

User = get_user_model()

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        field_name="status",
        queryset=Status.objects.all(),
        label="Status",
    )
    executor = django_filters.ModelChoiceFilter(
        field_name="executor",
        queryset=User.objects.all(),
        label="Executor",
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        method="filter_by_label",
        label="Label",
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Only my tasks",
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def filter_by_label(self, qs, name, value):
        return qs.filter(labels=value) if value else qs

    def filter_self_tasks(self, qs, name, value):
        if value and self.request.user.is_authenticated:
            return qs.filter(author=self.request.user)
        return qs
