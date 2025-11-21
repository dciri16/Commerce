from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid 

@login_required
def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def category_details(request, category_name):
    listings = Listing.objects.filter(category=category_name)
    return render(request, "auctions/category_details.html", {
        "category_name": category_name,
        "listings": listings
    })


@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment:
            Comment.objects.create(
                comment = comment,
                user = request.user,
                listing = listing
                )
        return render(request, "auctions/listing_detail.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "message": "Comment added"
        })



def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
                "listings": listings
            })

@login_required
def listing_detail(request, listing_id):
    if request.method == "POST":
        bid = Decimal(request.POST["bid"])
        listing = Listing.objects.get(pk=listing_id)
        starting_bid = listing.bid
        if bid <= starting_bid:
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                "message": "Bid lower than starting bid",
            })
        else:
            listing.bid = bid
            listing.save()
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                "message": "Bid successfully updated!",
            })

    else:
        try:
            listing = Listing.objects.get(pk=listing_id)
            return render(request, "auctions/listing_detail.html", {
                "listing": listing,
                "comments": listing.comments.all()
            })
        except Listing.DoesNotExist:
            raise Http404("Listing not found")

    
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

@login_required
def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST.get("description")
        bid = request.POST["bid"]
        image = request.FILES.get("image")
        category = request.POST["category"]

        errors =[]
        
        if not title:
            errors.append("Title is required.")
        
        if not bid:
            errors.append("Starting bid is required.")
        
        if errors:
            return render(request, "auctions/new_listing.html", {
                "errors": errors,
                "title": title,
                "description": description,
                "bid": bid,
                "category": category,
            })

        bid_decimal = Decimal(bid)
        
        created_listing = Listing.objects.create(
            title=title,
            description=description,
            bid=bid_decimal,
            image=image,
            owner = request.user,
            category=category,
        )
        created_listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html")


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
    
@login_required
def remove_from_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.remove(listing)
        return render (request,"auctions/watchlist.html", {
                "message": "Removed from Watchlist"
            })
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
                "listings": listings,
            })


@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        if listing in request.user.watchlist.all():
            message = "Already Added to Watchlist"
        else: 
            request.user.watchlist.add(listing)
            message = "Added to Watchlist"
        
        listings = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "listings": listings,
            "message": message
        })

    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })