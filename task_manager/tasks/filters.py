import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=TaskStatus.objects.all(), label='Статус')
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    labels = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(), label='Метки')
    my_tasks = django_filters.BooleanFilter(method='filter_my_tasks', label='Только мои задачи')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
