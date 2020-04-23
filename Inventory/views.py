from django.shortcuts import render
from django_filters.views import FilterView
from django_filters import FilterSet
from django_tables2.views import SingleTableMixin
import csv, io
from django.contrib import messages
from .models import Card
from .tables import CardTable


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


def upload(request):
    # declaring template
    template = 'upload.html'
    data = Card.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'name, edition, foil, quantity, bag',
        'profiles': data
    }

    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES.get('upload')
    delete_csv_file = request.FILES.get('delete')

    if csv_file is not None:
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')

        io_string = io.StringIO(data_set)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Card.objects.update_or_create(
                name=column[0],
                edition=column[1],
                foil=column[2],
                quantity=column[3],
                bag=column[4]
            )

    if delete_csv_file is not None:
        if not delete_csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = delete_csv_file.read().decode('UTF-8')

        io_string = io.StringIO(data_set)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            Card.objects.filter(
                name=column[0],
                edition=column[1],
                foil=column[2]
            ).delete()

    context = {}
    return render(request, template, context)