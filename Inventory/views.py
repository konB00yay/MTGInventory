import csv
import io
import re

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.utils import timezone
from django.db.models import F
from django.shortcuts import render
from django.views.generic import TemplateView
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Card, Sold, Bag, MarketEvaluation, MarketCard
from .tables import CardTable, SoldTable


class SetCodes:
    SET_KEYS = {}
    SET_NAMES = {}
    URL = "https://mtg.gamepedia.com/Template:List_of_Magic_sets"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.find('table', class_='wikitable')
    row_columns = cards.find_all('tr')
    for row in row_columns[1:]:
        row_values = row.find_all('td')
        set_name = re.sub("[\(\[].*?[\)\]]", "", row_values[1].text).rstrip()
        set_abbrev = re.sub("[\(\[].*?[\)\]]", "", row_values[3].text).rstrip()
        if set_abbrev != '':
            SET_KEYS[set_abbrev] = set_name
            SET_NAMES[set_name] = set_abbrev


class CardFilter(FilterSet):
    class Meta:
        model = Card
        fields = {
            'name': ['contains'],
            'edition': ['contains'],
        }


class CardTableView(SingleTableMixin, FilterView):
    model = Card
    table_class = CardTable
    template_name = 'card.html'
    filterset_class = CardFilter

    def get(self, request):
        template = 'card.html'
        data = Card.objects.all()
        # prompt is a context variable that can have different values      depending on their context
        prompt = {
            'order': 'name, edition, foil, quantity, bag',
            'table': data,
            'set_keys': SetCodes.SET_KEYS
        }
        return render(request, template, prompt)

    def post(self, request):
        # declaring template
        template = 'card.html'
        csv_file = request.FILES.get('upload')

        if csv_file is not None:
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8-SIG')

            io_string = io.StringIO(data_set)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                name = (column[0].replace(';', ','))
                edition = column[1]
                foil = column[2]
                quantity = column[3]
                bag = column[4]
                card_id = name + '_' + edition + '_' + foil
                bag_id = card_id + '_' + bag
                _, created = Card.objects.update_or_create(
                    id=card_id,
                    defaults={
                        'name': name,
                        'edition': edition,
                        'foil': foil
                    }
                )
                bags = Bag.objects.filter(bag_id=bag_id)
                if bags.count() == 0:
                    Bag.objects.update_or_create(
                        bag_id=bag_id,
                        defaults={
                            'card': _,
                            'bag_number': bag,
                            'quantity': quantity
                        }
                    )
                else:
                    selected_bag = bags[0]
                    selected_bag.quantity = F('quantity') + quantity
                    selected_bag.save()

        context = {'table': Card.objects.all()}
        return render(request, template, context)


class SoldTableView(SingleTableMixin, FilterView):
    model = Sold
    table_class = SoldTable
    template_name = 'upload.html'

    def get(self, request):
        template = 'upload.html'
        data = Sold.objects.all()
        total_profit = 0
        for sold in data:
            total_profit += sold.profit

        prompt = {
            'order': 'name, edition, foil, quantity, profit',
            'table': data,
            'total': total_profit
        }
        return render(request, template, prompt)

    def post(self, request):
        # declaring template
        template = 'upload.html'
        data = Sold.objects.all()
        total_profit = 0
        context = {}
        delete_csv_file = request.FILES.get('delete')

        if delete_csv_file is not None:
            if not delete_csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = delete_csv_file.read().decode('UTF-8-SIG')

            io_string = io.StringIO(data_set)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                name = (column[0].replace(';', ','))
                edition = column[1]
                foil = column[2]
                quantity = column[3]
                card_id = name + '_' + edition + '_' + foil
                card = Card.objects.filter(id=card_id)
                card_bag = Bag.objects.filter(card__id=card_id)
                if card_bag.count() > 0 and card.count() > 0:
                    selected_card_bag = card_bag[0]
                    selected_card = card[0]
                    if selected_card_bag.quantity <= int(quantity):
                        selected_card_bag.delete()
                        # selected_card.delete()
                    else:
                        selected_card_bag.quantity = F('quantity') - column[3]
                        selected_card_bag.save()
                    _, created = Sold.objects.update_or_create(
                        id=selected_card.id,
                        defaults={
                            'quantity': quantity,
                            'profit': column[5]
                        }
                    )
                    total_profit += column[5]
        context = {'table': Sold.objects.all(), 'total': total_profit}
        return render(request, template, context)


class MarketAnalysis(TemplateView):
    template_name = 'market.html'

    def market_dict(self):
        market_dict = []
        for market_card in MarketCard.objects.exclude(bag=None):
            print(market_card)
            profit = market_card.profit()
            bags = []
            for bag in market_card.bag.all():
                bags.append(bag.bag_number)

            card_entry = {'name': market_card.id, 'bags': bags, 'profit': profit}
            market_dict.append(card_entry)
        return market_dict

    def get(self, request):
        template = 'market.html'
        return render(request, template, {'market_dict': MarketAnalysis.market_dict(self),
                                          'market_eval': MarketEvaluation.objects.order_by('-time_stamp')
                      .first().__str__})

    def post(self, request):
        if 'gather_market_data' in request.POST:
            # MarketCard.objects.all().delete()
            print(len(list(MarketCard.objects.all())))
            URL = "https://cardkingdom.com/purchasing/mtg_singles?filter%5Bipp%5D=100&filter%5Bsort%5D=" \
                  "name&filter%5Bnonfoil%5D=1&filter%5Bfoil%5D=1"
            page = requests.get(URL)
            curr_time = timezone.now()
            market_eval, created = MarketEvaluation.objects.update_or_create(
                time_stamp=curr_time
            )
            soup = BeautifulSoup(page.content, 'html.parser')
            bags = []
            # pages = soup.find('ul', class_='pagination').find_all('a')
            # page_list = list(range(1, int(pages[len(pages) - 1].text) + 1))
            page_list = [1, 2]
            for p in page_list:
                page_url = 'https://cardkingdom.com/purchasing/mtg_singles?filter%%5Bipp%%5D=100&filter%%5Bsort%%5D=' \
                           'name&filter%%5Bnonfoil%%5D=1&filter%%5Bfoil%%5D=1&page=%s' % (p)
                next_page = requests.get(page_url)
                soup = BeautifulSoup(next_page.content, 'html.parser')
                cards = soup.find_all('div', class_='itemContentWrapper')
                for card in cards:
                    card_name = re.sub("[\(\[].*?[\)\]]", "", card.find('span', class_='productDetailTitle').text) \
                        .rstrip()
                    card_edition = re.sub("[\(\[].*?[\)\]]", "",
                                          card.find('div', class_='productDetailSet').find('a').text).rstrip()
                    card_foil = card.find('div', class_='foil') is not None
                    if "FOIL" in card_edition:
                        card_foil = 'true'
                        card_edition = card_edition.replace('FOIL', '').rstrip()
                    card_edition_key = card_edition
                    if card_edition in SetCodes.SET_NAMES.keys():
                        card_edition_key = SetCodes.SET_NAMES[card_edition]
                    card_profit_dollar = float(card.find('span', class_='sellDollarAmount').text)
                    card_profit_cents = float(card.find('span', class_='sellCentsAmount').text) / 100
                    card_profit = card_profit_dollar + card_profit_cents
                    card_id = card_name + '_' + card_edition_key + '_' + str(int(card_foil == 'true'))
                    curr_market_card, created_card = MarketCard.objects.update_or_create(
                        id=card_id,
                        defaults={
                            'evaluation': market_eval,
                            'market_value': card_profit
                        }
                    )
            template = 'market.html'
            return render(request, template, {'market_dict': [], 'market_eval': market_eval.__str__})
        elif 'apply_market_data' in request.POST:
            # Need to factor in existing evaluations and resetting bags
            latest_eval = MarketEvaluation.objects.order_by('-time_stamp').first()
            if latest_eval.card_evaluation == 0:
                card_quantity = 0
                card_eval = 0
                for market_card in MarketCard.objects.all():
                    bags = Bag.objects.filter(card__id=market_card.id)
                    if bags:
                        market_card.bag.add(*list(bags))
                        market_card.save()
                        card_quantity += sum(bags.values_list('quantity', flat=True))
                        card_eval += market_card.profit()
                    else:
                        market_card.bag.set([])
                        market_card.save()
                latest_eval.card_evaluation = card_eval
                latest_eval.cards_quantity = card_quantity
                latest_eval.save()

            return render(request, self.template_name, {'market_dict': MarketAnalysis.market_dict(self),
                                                        'market_eval': MarketEvaluation.objects.order_by('-time_stamp')
                          .first().__str__})
