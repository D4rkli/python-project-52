from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Status
from .forms import StatusForm

class StatusListView(ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    ordering = ["id"]

class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_index")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)

class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_index")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)

class StatusDeleteView(DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_index")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            messages.success(request, "Статус успешно удален")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется",
            )
            return redirect("statuses_index")
