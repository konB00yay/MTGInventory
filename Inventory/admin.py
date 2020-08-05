from django.contrib import admin

from .models import Card, Sold, Bag, MarketEvaluation

admin.site.register(Card)
admin.site.register(Sold)
admin.site.register(Bag)
admin.site.register(MarketEvaluation)