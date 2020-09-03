from django.contrib import admin

from .models import Auction_listings, Category

# Register your models here.
admin.site.register(Auction_listings)
admin.site.register(Category)