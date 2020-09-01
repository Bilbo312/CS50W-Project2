from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    name = models.CharField(max_length=64)
    body_text = models.TextField()
    price = models.IntegerField(max_length=16)

    '''def __str__(self):
        return f"{self.city} ({self.code})"'''