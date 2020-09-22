from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_listings, Category, Bids
from .forms import NewListingForm, NewBidForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_listings.objects.all()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Listing_title"]
            content = form.cleaned_data["Listing_content"]
            init_price = form.cleaned_data["init_price"]
            
            new_listing = Auction_listings(
                name = title,
                body_text = content,
                init_price = init_price
            )
            
            new_listing.save()
            return render(request, "auctions/New_listing.html", {
                "form":  NewListingForm()
            })

        else:
            return render(request, "auctions/New_listing.html", {
                'form': form
            })
    else:
        return render(request, "auctions/New_listing.html", {
            'form': NewListingForm()
        })

def all_listings(request):
    return render(request, "auctions/all_listing.html", {
        "listings": Auction_listings.objects.all()
    })
    

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def listing(request, Auction_listings_id):
    all_listings = Auction_listings.objects.order_by().values_list('id', flat=True).distinct()
    if Auction_listings_id not in all_listings:
        return render(request, "auctions/error_message.html", {
            "message": "This page does not exist" + str(all_listings) #Just to check which values are in all_listings
        })

    else:
        listing = Auction_listings.objects.get(id = Auction_listings_id)
        bids = Bids.objects.filter(selling_item = Auction_listings_id).order_by('bid_value')
        form = NewBidForm(request.POST)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bids": bids,
            "form": form
        })


def new_bid(request, Auction_listings_id):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        highest_bid = Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value')[0] 
        listing = Auction_listings.objects.get(id = Auction_listings_id)
        bids = Bids.objects.filter(selling_item = Auction_listings_id).order_by('bid_value')
        user = request.user
        if form.is_valid():
            new_bid = form.cleaned_data["new_bid"]
            if new_bid > highest_bid.bid_value:
                newBid = Bids(
                    bidding_user = user,
                    selling_item = listing,
                    bid_value = new_bid,
                    number_of_bids = Bids.objects.filter(selling_item = Auction_listings_id).count() #Doesn't work
                )
                newBid.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bids": bids,
                    "form": form,
                    "no_bids": Bids.objects.filter(selling_item = Auction_listings_id).count(),
                    "message": "Your bid of " + str(new_bid) + " is now the leading bid"
                })

            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bids": bids,
                    "form": form,
                    "message": "Your bid of " + str(new_bid) + " was not larger than the preexisting bid"
                })
