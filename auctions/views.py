from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing


def index(request):
    listings = Listing.objects.all()[::-1]
    context =  {
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
        with open("auctions/static/auctions/media/"+file_name, "wb") as f:
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
        Listing.objects.create(seller=request.user, item_name=item_name, description=description, price=price, image_name=file_name)
        return render(request, "auctions/create.html", context)


def detail(request, item_id):
    listing = Listing.objects.get(id=item_id)
    context = {
        "listing": listing,
    }
    return render(request, "auctions/detail.html", context)

def delete(request, item_id):
    Listing.objects.get(id=item_id).delete()
    return redirect(index)

