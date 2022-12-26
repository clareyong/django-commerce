from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey("User", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=64)
    description = models.CharField(max_length=100, null=True)
    price = models.BigIntegerField()
    image_name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.item_name}"

# class Listing():
#     pass

# class Bids():
#     pass
