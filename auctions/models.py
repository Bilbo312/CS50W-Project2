from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import CATEGORY_CHOICES

class User(AbstractUser):
    pass

#Model for the listings
class Auction_listings(models.Model):
    name = models.CharField(max_length=64)
    body_text = models.TextField()
    init_price = models.DecimalField(decimal_places=2, max_digits=9)
    picture = models.URLField(null = True, blank=True)
    category = models.CharField(default= "Fashion", max_length=16)
    status = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, default = 2, related_name="owner")
    winner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name="winner")


    watching = models.ManyToManyField(User, blank = True, related_name="watchlist")

    def __str__(self):
        return f"{self.name}"


#Model for all bids on Auction listings
class Bids(models.Model):
    bidding_user = models.ForeignKey(User, on_delete = models.CASCADE)
    selling_item = models.ForeignKey(Auction_listings, on_delete = models.CASCADE, related_name="item")
    bid_value = models.DecimalField(decimal_places=2, max_digits=9)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"This bid of ${self.bid_value} on {self.selling_item} was made by {self.bidding_user} at {self.created}"

#Model for comments
class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "my_comments")
    item = models.ForeignKey(Auction_listings, on_delete = models.CASCADE, related_name="comments")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} commented {self.comment} on {self.item} at {self.created}"
