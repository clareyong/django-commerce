from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey("User", on_delete=models.CASCADE, related_name="possessions")
    item_name = models.CharField(max_length=64)
    description = models.CharField(max_length=100, null=True)
    price = models.BigIntegerField()
    image_name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)
    number_of_bids = models.IntegerField(default=0)
    current_bid = models.BigIntegerField(default=0)
    bidder = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, related_name="winning_bids")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name}"


class Watchlist(models.Model):
    bidder = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey("Listing", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.bidder}: {self.item}"


# class Bids():
#     pass
