from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic import ListView
from django_tables2 import SingleTableView
import csv, io
from django.contrib import messages
from .models import Card
from .tables import CardTable


class CardTableView(SingleTableView):
    model = Card
    table_class = CardTable
    template_name = 'card.html'


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
    csv_file = request.FILES['file']

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
        print(created)
    context = {}
    return render(request, template, context)