from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executed_tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
