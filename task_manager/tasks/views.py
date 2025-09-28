from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .filters import TaskFilter
from django.db.models import Prefetch
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

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
        qs = super().get_queryset().select_related(
            "status", "author", "executor"
        ).prefetch_related("labels")
        v = self.request.GET.get("self_tasks")
        if v in {"1", "true", "True", "on", "yes", "y"}:
            qs = qs.filter(author=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        flt = ctx.get("filter")
        if flt is not None:
            ctx["form"] = flt.form
        return ctx

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
        messages.success(self.request, "Task created successfully")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_index")

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully")
        return super().form_valid(form)

class AuthorOnlyDeleteMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, "You have no rights to delete this task")
        return redirect("tasks_index")

class TaskDeleteView(LoginRequiredMixin, AuthorOnlyDeleteMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_index")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully")
        return super().delete(request, *args, **kwargs)

