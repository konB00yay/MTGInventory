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
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    bag_number = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False)

    class Meta:
        indexes = [
            models.Index(fields=['card'])
        ]


class MarketEvaluation(models.Model):
    time_stamp = models.DateTimeField(blank=False, primary_key=True)
    cards_quantity = models.IntegerField(blank=False, default=0)
    card_evaluation = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        if self.card_evaluation == 0:
            return "Market data collected at: " + str(self.time_stamp)
        else:
            return "Evaluation at " + str(self.time_stamp) + " resulted in $" + str(self.card_evaluation)


class MarketCard(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False)
    evaluation = models.ForeignKey(MarketEvaluation, on_delete=models.CASCADE)
    market_value = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    bag = models.ManyToManyField(Bag, blank=True)

    def profit(self):
        profit = 0
        for b in self.bag.all():
            profit += b.quantity * self.market_value
        return profit
