from django.db import models

from ..users.models import User

__all__ = ('Responsable', )

class Responsable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)