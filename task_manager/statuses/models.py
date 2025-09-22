from django.db import models

class Status(models.Model):
    # имя поля формы будет "name", id="id_name" — как требует задание
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
