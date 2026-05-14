from django.db import models
from django.conf import settings

__all__ = ('Card', )

class Card(models.Model):
    name = models.CharField(max_length=20)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)