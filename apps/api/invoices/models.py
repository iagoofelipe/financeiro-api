from django.db import models

from ..cards.models import Card

class Invoice(models.Model):
    date_reference = models.DateField()
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    limit = models.FloatField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)