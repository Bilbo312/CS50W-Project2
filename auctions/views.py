from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auction_listings, Bids, WatchList, Comment
from .forms import NewListingForm, NewBidForm, NewCommentForm


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

@login_required(login_url = '/login')
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Listing_title"]
            content = form.cleaned_data["Listing_content"]
            init_price = form.cleaned_data["init_price"]
            picture = form.cleaned_data["picture"]
            category = form.cleaned_data["category"]
            bidder = request.user
            
            new_listing = Auction_listings(
                name = title,
                body_text = content,
                init_price = init_price,
                owner = bidder,
                picture = picture,
                category = category
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
    
@login_required(login_url = '/login')
def categories(request):
    categories = Auction_listings.objects.values('category').distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required(login_url = '/login')
def category_page(request, category):
    listings = Auction_listings.objects.filter(category = category)
    return render(request, "auctions/category_page.html", {
        "category": category,
        "listings": listings
    })

def listing(request, Auction_listings_id):
    all_listings = Auction_listings.objects.order_by().values_list('id', flat=True).distinct()
    valid = Auction_listings.objects.filter(id = Auction_listings_id).get().status
    listing = Auction_listings.objects.get(id = Auction_listings_id)
    bids = Bids.objects.filter(selling_item = Auction_listings_id).order_by('bid_value')
    comments = Comment.objects.filter(item = listing)
    no_bids = Bids.objects.filter(selling_item = Auction_listings_id).count()
    no_comments = Comment.objects.filter(item = Auction_listings_id).count()
    user = request.user
    lister = listing.owner
    if Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first() is not None:
        highest_bid_2 = Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first()  #if no preexisting need to get starting
        highest_bid = highest_bid_2.bid_value
    else:
        highest_bid = listing.init_price
    
    if listing.winner != None:
        winner = listing.winner
    elif listing.winner == None and valid == False:
        winner = "No one"
    else:
        winner = None

    if 'message' not in locals() :
        message = "No message here"

    if Auction_listings_id not in all_listings:
        return render(request, "auctions/error_message.html", {
            "message": "This page does not exist" + str(all_listings) #Just to check which values are in all_listings
        })
    else: 
        form = NewBidForm(request.POST)
        form_2 = NewCommentForm(request.POST)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bids": bids,
            "form": form,
            "comment_form": form_2,
            "comments": comments,
            "no_comments": no_comments,
            "no_bids": no_bids,
            "valid": valid,
            "user": user,
            "lister":lister,
            "highest_bid":highest_bid,
            "message": message,
            "winner": winner
        })

@login_required(login_url = '/login')
def new_bid(request, Auction_listings_id):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        listing = Auction_listings.objects.get(id = Auction_listings_id)
        bids = Bids.objects.filter(selling_item = Auction_listings_id).order_by('bid_value')
        user = request.user
        if Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first() is not None:
            highest_bid_2 = Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first()  #if no preexisting need to get starting
            highest_bid = highest_bid_2.bid_value        
        else:
            highest_bid = listing.init_price

        if form.is_valid():
            new_bid = form.cleaned_data["new_bid"]
            if new_bid > highest_bid:
                newBid = Bids(
                    bidding_user = user,
                    selling_item = listing,
                    bid_value = new_bid,
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
                return HttpResponseRedirect('/listing/%s' % Auction_listings_id)

@login_required(login_url = '/login')
def go_watch(request):
    user = request.user
    Listitems = WatchList.objects.filter(Watchuser = user)
    return render(request, "auctions/watchlist.html", { 
        "user": user,
        "listitems": Listitems
    })

@login_required(login_url = '/login')
def add_watch(request, Auction_listings_id):
    listing = Auction_listings.objects.get(id = Auction_listings_id)
    form = NewBidForm(request.POST)
    bids = Bids.objects.filter(selling_item = Auction_listings_id).order_by('bid_value')
    user = request.user
    if WatchList.objects.filter(Watchuser = user, Watchitem=listing).exists():
        return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bids": bids,
                    "form": form,
                    "message": "This item is already on the Watchlist",
                    "question": True
                })
    else:
        newWatch = WatchList(
            Watchuser = user,
            Watchitem = listing
        )
        newWatch.save()
        return HttpResponseRedirect('/watchlist')

@login_required(login_url = '/login')
def del_watch(request, Watchitem_id):
    item = WatchList.objects.filter(Watchitem_id = Watchitem_id)
    item.delete()
    return HttpResponseRedirect('/watchlist')

@login_required(login_url = '/login')
def new_comment(request, Auction_listings_id):
    if request.method == "POST":
        form_2 = NewCommentForm(request.POST)
        user = request.user
        item = Auction_listings.objects.get(id = Auction_listings_id)
        if form_2.is_valid():
            content = form_2.cleaned_data["comment_content"]

            newComment = Comment(commenter = user, item = item, comment = content)
            newComment.save()
            return HttpResponseRedirect('/listing/%s' % Auction_listings_id)

@login_required(login_url = '/login')
def delist(request, Auction_listings_id):
    listing = Auction_listings.objects.filter(id = Auction_listings_id).get()
    if Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first() is not None:
            highest_bid_2 = Bids.objects.filter(selling_item = Auction_listings_id).order_by('-bid_value').first()  #if no preexisting need to get starting
            winning_bidder = highest_bid_2.bidding_user      
    else:
        winning_bidder = None
    winner = winning_bidder
    listing.status = False
    listing.winner = winner
    listing.save()
    return HttpResponseRedirect('/listing/%s' % Auction_listings_id)