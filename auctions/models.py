from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    FASHION = 'FA'
    TOYS = 'TY'
    ELECTRONICS = 'EL'
    HOME = 'HM'
    GARDEN = 'GA'
    VEHICLES = 'VH'
    MUSIC = 'MU'
    ART = 'AT'
    SPORTS = 'SP'
    
    CATEGORY_CHOICES = [
        (FASHION, "Fashion"),
        (TOYS, "Toys"),
        (ELECTRONICS, "Electronics"),
        (HOME, "Home"),
        (GARDEN, "Garden"),
        (VEHICLES, "Vehicles"),
        (MUSIC, "Music"),
        (ART, "Art"),
        (SPORTS, "Sports")
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default= FASHION,
        null = True
    )

    def __str__(self):
        return f"{self.category}"


class Auction_listings(models.Model):
    name = models.CharField(max_length=64)
    body_text = models.TextField()
    init_price = models.FloatField(max_length=16)
    picture = models.URLField(null = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=16, null = True)

    def __str__(self):
        return f"{self.name}, {self.body_text} and the start price is {self.init_price}"