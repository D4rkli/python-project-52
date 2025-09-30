from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .filters import TaskFilter
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    ordering = ["id"]
    paginate_by = 20

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
        )
        only_self = self.request.GET.get("self_tasks")
        if only_self in {"1", "true", "True", "on", "yes", "y"}:
            qs = qs.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flt = context.get("filter")
        if flt is not None:
            context["form"] = flt.form
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class AuthorOnlyDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этой задачи")
        return redirect("tasks_index")


class TaskDeleteView(LoginRequiredMixin, AuthorOnlyDeleteMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_index")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Задача успешно удалена")
        return response
