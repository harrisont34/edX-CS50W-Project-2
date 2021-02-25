from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms


class User(AbstractUser):
    pass

# Auction Listing Model
class Listing(models.Model):
    CATEGORY = [
        ("CA", "Collectibles & Art"),
        ("E", "Electronics"),
        ("EM", "Entertainment Memorabilia"),
        ("F", "Fashion"),
        ("Hg", "Home & Garden"),
        ("M", "Motors"),
        ("SG", "Sporting Goods"),
        ("TH", "Toys & Hobbies"),
        ("OC", "Other Categories")
    ]

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=100)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.URLField(blank=True)
    category = models.CharField(blank=True,choices=CATEGORY,max_length=30)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.title}"

# Watchlist Model
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False)


# Comments Model
class ListComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False)
    comment = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"Comment for {self.item_id}"


# Bid Model
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False)
    bid = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid for {self.item_id}"
    