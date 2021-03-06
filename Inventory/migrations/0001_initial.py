# Generated by Django 2.0 on 2020-08-10 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('bag_id', models.CharField(editable=False, max_length=150, primary_key=True, serialize=False)),
                ('bag_number', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('edition', models.CharField(max_length=10)),
                ('foil', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MarketCard',
            fields=[
                ('id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('market_value', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='MarketEvaluation',
            fields=[
                ('time_stamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('cards_quantity', models.IntegerField(default=0)),
                ('card_evaluation', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Sold',
            fields=[
                ('id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.AddField(
            model_name='marketcard',
            name='evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.MarketEvaluation'),
        ),
        migrations.AddField(
            model_name='bag',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.Card'),
        ),
        migrations.AddIndex(
            model_name='bag',
            index=models.Index(fields=['card'], name='Inventory_b_card_id_9a88df_idx'),
        ),
    ]
