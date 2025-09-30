from django.db import models


class Status(models.Model):
    name = models.CharField('Имя', max_length=255, unique=True)

    def __str__(self):
        return self.name
