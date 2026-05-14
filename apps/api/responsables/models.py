from django.db import models
from django.conf import settings

__all__ = ('Responsable', )

class Responsable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)