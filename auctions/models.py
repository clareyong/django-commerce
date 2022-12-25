from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey("User", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=64)
    price = models.BigIntegerField()

    def __str__(self):
        return f"{self.item_name}"

# class Listing():
#     pass

# class Bids():
#     pass
