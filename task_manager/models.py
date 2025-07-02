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

    def __str__(self):
        return self.name
