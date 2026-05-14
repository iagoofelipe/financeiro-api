from django.db import models

from ..users.models import User

__all__ = ('Card', )

class Card(models.Model):
    name = models.CharField(max_length=20)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)