import uuid
from django.db import models


# Create your models here.
class Card(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    name = models.CharField(max_length=150, blank=False)
    edition = models.CharField(max_length=10, blank=False)
    foil = models.BooleanField(blank=False)


class Sold(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    quantity = models.IntegerField(blank=False)
    profit = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class Bag(models.Model):
    bag_id = models.CharField(max_length=150, primary_key=True, editable=False)
    id = models.CharField(max_length=100, editable=False)
    bag_number = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False)


class MarketEvaluation(models.Model):
    time_stamp = models.DateTimeField(blank=False)
    cards_quantity = models.IntegerField(blank=False)
    card_evaluation = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
