from django.contrib import admin

from .models import Auction_listings,Category,Bids,Comment

# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Category)
admin.site.register(Bids)
admin.site.register(Comment)