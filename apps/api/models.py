from django.db import models
from django.conf import settings


class Card(models.Model):
    name = models.CharField(max_length=20)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



class Invoice(models.Model):
    date_ref = models.DateField()
    closing_date = models.DateField()
    due_date = models.DateField()
    limit = models.FloatField()
    card = models.ForeignKey(Card, on_delete=models.CASCADE)



class Responsable(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)