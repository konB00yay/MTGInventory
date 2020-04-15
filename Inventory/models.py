from django.db import models


# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=150, blank=False)
    edition = models.CharField(max_length=10, blank=False)
    foil = models.BooleanField(blank=False)
    quantity = models.IntegerField(blank=False)
    bag = models.IntegerField(blank=False)

    def __str__(self):
        return self.name
