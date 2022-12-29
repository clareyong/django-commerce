from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Listing, Watchlist


def index(request):
    listings = Listing.objects.all()[::-1]
    context = {
        "listings": listings
    }
    return render(request, "auctions/index.html", context)


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


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    if request.method == "POST":
        item_name = request.POST.get("name", "")
        price = request.POST.get("price", "")
        description = request.POST.get("description", "")
        file_object = request.FILES['listing-image']
        file_bytes = file_object.file.getvalue()
        file_name = file_object.name
        number_of_bids = 0
        current_bid = price
        with open("auctions/static/auctions/media/" + file_name, "wb") as f:
            f.write(file_bytes)
        context = {}
        if item_name == "":
            context = {
                "message": "Please include item name"
            }
        if price == "":
            context = {
                "message": "Please include auction price"
            }
        Listing.objects.create(seller=request.user, item_name=item_name, description=description, price=price,
                               image_name=file_name, number_of_bids=number_of_bids, current_bid=current_bid)
        return render(request, "auctions/detail_and_bid.html", context)


def detail_and_bid(request, item_id):
    if not request.user.is_authenticated:
        return redirect(login_view)
    listing = Listing.objects.get(id=item_id)
    if request.method == 'GET':
        context = {
            "listing": listing,
        }
        return render(request, "auctions/detail_and_bid.html", context)
    elif request.method == 'POST':
        current_bid = request.POST.get("current_bid", 0)
        current_bid = int(current_bid)
        if current_bid > listing.current_bid and current_bid >= listing.price:
            listing.number_of_bids += 1
            listing.bidder = request.user
            listing.current_bid = current_bid
            listing.save()
            if not Watchlist.objects.filter(bidder=request.user, item=listing).count():
                Watchlist.objects.create(bidder=request.user, item=listing)
            return redirect(detail_and_bid, item_id)
        else:
            if current_bid < listing.price:
                context = {
                    "listing": listing,
                    "message": "Please bid higher than the current price.",
                }
            else:
                context = {
                    "listing": listing,
                    "message": "Please bid higher than previous current bid"
                }
            return render(request, "auctions/detail_and_bid.html", context)
    else:
        return HttpResponseForbidden()


def delete(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if listing.is_active:
        listing.delete()
        return redirect(index)
    else:
        return HttpResponseForbidden()


def edit(request, item_id):
    listing = Listing.objects.get(id=item_id)
    if request.method == "GET":
        context = {
            "listing": listing,
        }
        return render(request, "auctions/edit.html", context)
    if request.method == "POST":
        item_name = request.POST.get("name", "")
        price = request.POST.get("price", "")
        description = request.POST.get("description", "")
        file_object = request.FILES.get('listing-image', None)
        file_name = ""
        if file_object is not None:
            file_bytes = file_object.file.getvalue()
            file_name = file_object.name
            with open("auctions/static/auctions/media/" + file_name, "wb") as f:
                f.write(file_bytes)
        if item_name == "":
            return HttpResponse("Please add item name")
        if description == "":
            return HttpResponse("Please add descriptions")
        listing.item_name = item_name
        listing.description = description
        listing.price = price
        if file_name != '':
            listing.image_name = file_name
        listing.save()
        return redirect(detail_and_bid, item_id)
    else:
        return HttpResponseForbidden()


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    watchlists = Watchlist.objects.filter(bidder=request.user)[::-1]
    context = {
        "watchlists": watchlists
    }
    return render(request, "auctions/watchlist.html", context)


def close(request, item_id):
    listing = Listing.objects.get(id=item_id)
    listing.is_active = False
    listing.save()
    return redirect(detail_and_bid, item_id)


