from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
     watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchers')

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    comment = models.CharField(max_length = 256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comments")

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 256)
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    category = models.CharField(max_length = 64)



