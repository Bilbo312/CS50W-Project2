# Generated by Django 3.0.8 on 2020-09-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction_listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('body_text', models.TextField()),
                ('init_price', models.IntegerField(max_length=16)),
            ],
        ),
        migrations.DeleteModel(
            name='Auction_listing',
        ),
    ]
