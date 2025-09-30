from django.conf import settings
from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,          # защита от удаления
        related_name='tasks',
        verbose_name='Статус',
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='executed_tasks',
        verbose_name='Исполнитель',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name='Автор',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
