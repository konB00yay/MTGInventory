import django_tables2 as tables
from .models import Card, Sold


class CardTable(tables.Table):
    id = tables.Column()
    name = tables.Column()
    edition = tables.Column()
    foil = tables.Column()
    quantity = tables.Column()
    bag = tables.Column()

    class Meta:
        model = Card
        attrs = {'id': 'card_table'}
        fields = ("id", "name", "edition", "foil", "quantity", "bag")


class SoldTable(tables.Table):
    id = tables.Column()
    name = tables.Column()
    edition = tables.Column()
    foil = tables.Column()
    quantity = tables.Column()
    profit = tables.Column()

    class Meta:
        model = Sold
        attrs = {'id': 'sold_table'}
        fields = ("id", "name", "edition", "foil", "quantity", "profit")
