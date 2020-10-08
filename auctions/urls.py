from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<slug:category>", views.category_page, name="category_page"),
    path("listing/<int:Auction_listings_id>", views.listing, name="listing"),
    path("listing/<int:Auction_listings_id>/new_bid", views.new_bid, name="new_bid"),
    path("listing/<int:Auction_listings_id>/watchlist", views.add_watch, name="add_watch"),
    path("watchlist", views.go_watch, name="go_watch"),
    path("watchlist/delete/<int:Watchitem_id>", views.del_watch, name="del_watch"),
    path("listing/<int:Auction_listings_id>/new_comment", views.new_comment, name="new_comment"),
    path("listing/<int:Auction_listings_id>/delist", views.delist, name="delist"),
]
