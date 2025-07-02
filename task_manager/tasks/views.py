from django_filters.views import FilterView
from .models import Task
from .filters import TaskFilter

class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
