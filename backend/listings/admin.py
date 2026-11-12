from django.contrib import admin
from .models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'price_per_day', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'renter', 'start_date', 'end_date', 'status', 'total_price']
    list_filter = ['status']