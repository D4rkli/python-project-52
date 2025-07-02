from django.db import models

from task_manager.labels.models import Label
from task_manager.models import Status, User


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executed_tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, blank=True, related_name='tasks')

    def __str__(self):
        return self.name
