# Generated by Django 3.0.8 on 2020-09-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_auction_listings_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
