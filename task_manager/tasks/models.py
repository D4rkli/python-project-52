from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task_models(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    labels = models.ManyToManyField(Label, blank=True, related_name='tasks')

    def __str__(self):
        return self.name
