from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('regular', 'Обычный пользователь'),
        ('manager', 'Менеджер'),
        ('admin', 'Админ'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authored_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executed_tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
