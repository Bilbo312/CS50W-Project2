from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:Auction_listings_id>", views.listing, name="listing"),
    path("listing/<int:Auction_listings_id>/new_bid", views.new_bid, name="new_bid")
]
