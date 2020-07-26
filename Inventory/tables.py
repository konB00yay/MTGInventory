import django_tables2 as tables
from .models import Card, Sold


class CardTable(tables.Table):
    class Meta:
        model = Card
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "edition", "foil", "quantity", "bag")


class SoldTable(tables.Table):
    class Meta:
        model = Sold
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "edition", "foil", "quantity", "profit")
