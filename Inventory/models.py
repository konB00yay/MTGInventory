import uuid
from django.db import models


# Create your models here.
class Card(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False)
    edition = models.CharField(max_length=10, blank=False)
    foil = models.BooleanField(blank=False)
    quantity = models.IntegerField(blank=False)
    bag = models.IntegerField(blank=False)

    def __str__(self):
        return self.name
