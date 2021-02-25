from django.contrib import admin
from .models import Listing, Watchlist, User, ListComment, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "starting_bid", "category")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item_id")

class ListCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item_id", "timestamp")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item_id", "bid", "timestamp")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(ListComment, ListCommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(User)
