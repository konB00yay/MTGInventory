import csv
import io

from django.contrib import messages
from django.shortcuts import render
from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.db.models import F

from .models import Card, Sold
from .tables import CardTable, SoldTable


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

    def post(self, request):
        # declaring template
        template = 'card.html'
        data = Card.objects.all()
        # prompt is a context variable that can have different values      depending on their context
        prompt = {
            'order': 'name, edition, foil, quantity, bag',
            'profiles': data
        }
        if request.method == "GET":
            return render(request, template, prompt)
        csv_file = request.FILES.get('upload')

        if csv_file is not None:
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8-SIG')

            io_string = io.StringIO(data_set)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Card.objects.update_or_create(
                    name=(column[0].replace(';', ',')),
                    edition=column[1],
                    foil=column[2],
                    quantity=column[3],
                    bag=column[4]
                )

        context = {'table': Card.objects.all()}
        return render(request, template, context)


class SoldTableView(SingleTableMixin, FilterView):
    model = Sold
    table_class = SoldTable
    template_name = 'upload.html'

    def post(self, request):
        # declaring template
        template = 'upload.html'
        data = Sold.objects.all()
        # prompt is a context variable that can have different values      depending on their context
        prompt = {
            'order': 'name, edition, foil, quantity, profit',
            'profiles': data
        }
        context = {}

        if request.method == "GET":
            return render(request, template, prompt)
        delete_csv_file = request.FILES.get('delete')

        if delete_csv_file is not None:
            if not delete_csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = delete_csv_file.read().decode('UTF-8-SIG')

            io_string = io.StringIO(data_set)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                card = Card.objects.filter(
                    name=(column[0].replace(';', ',')),
                    edition=column[1],
                    foil=column[2],
                    bag=column[4]
                )
                if card.count() > 0:
                    selected_card = card[0]
                    if selected_card.quantity <= int(column[3]):
                        selected_card.delete()
                    else:
                        selected_card.quantity = F('quantity') - column[3]
                        selected_card.save()
                    _, created = Sold.objects.update_or_create(
                        id=selected_card.id,
                        name=selected_card.name,
                        edition=selected_card.edition,
                        foil=selected_card.foil,
                        quantity=column[3],
                        profit=column[5]
                    )
        context = {'tables': Sold.objects.all()}
        return render(request, template, context)