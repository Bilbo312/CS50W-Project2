# Generated by Django 3.0.8 on 2020-12-28 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20201218_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='watching',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]