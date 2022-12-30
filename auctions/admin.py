from django.contrib import admin

from .models import Listing, Watchlist


class ListingAdmin(admin.ModelAdmin):
    pass


class WatchlistAdmin(admin.ModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
