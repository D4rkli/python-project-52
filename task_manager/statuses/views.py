from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Status created successfully.')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Status updated successfully.')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses:list')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'Status deleted successfully.')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Cannot delete status because it is in use.')
            return self.get(request, *args, **kwargs)
