from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


#Model for the categories
'''class Category(models.Model):
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
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home'),
        (GARDEN, 'Garden'),
        (VEHICLES, 'Vehicles'),
        (MUSIC, 'Music'),
        (ART, 'Art'),
        (SPORTS, 'Sports')
    ]
    category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default= FASHION,
        null = True
    )

    def __str__(self):
        return f"{self.category}"'''


#Model for the listings
class Auction_listings(models.Model):
    name = models.CharField(max_length=64)
    body_text = models.TextField()
    init_price = models.FloatField(max_length=16)
    picture = models.URLField(null = True, blank=True)
    category = models.CharField(default= "Fashion", max_length=16)
    status = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, default = 2, related_name="owner")
    winner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name="winner")

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

class WatchList(models.Model):
    Watchuser = models.ForeignKey(User, on_delete = models.CASCADE, related_name="watchuser")
    Watchitem = models.ForeignKey(Auction_listings, on_delete = models.CASCADE, related_name="watchitem")

    def __str__(self):
        return f"this item is {self.Watchitem} and it is being watched by {self.Watchuser}"