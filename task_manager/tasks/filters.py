import django_filters
from django import forms
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field("status").remote_field.model.objects.all().order_by("id"),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field("executor").remote_field.model.objects.all().order_by("id"),
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Task._meta.get_field("labels").remote_field.model.objects.all().order_by("id"),
        label="Метка",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_self_tasks"})
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]

    # показ только своих задач
    def filter_self(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
