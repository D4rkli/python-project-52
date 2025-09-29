import django_filters
from django.contrib.auth import get_user_model

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    """Фильтр для списка задач."""
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
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
        field_name="labels",
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

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
