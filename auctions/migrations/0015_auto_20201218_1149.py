# Generated by Django 3.0.8 on 2020-12-18 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201008_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='init_price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
