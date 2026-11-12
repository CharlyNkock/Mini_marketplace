from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('bricolage', 'Bricolage'),
    ('camping', 'Camping & Plein air'),
    ('photo_audio', 'Photo & Audio'),
    ('sport', 'Sport'),
    ('autre', 'Autre'),
]

STATUS_CHOICES = [
    ('pending', 'En attente'),
    ('confirmed', 'Confirmée'),
    ('cancelled', 'Annulée'),
]


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='autre')
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    location_name = models.CharField(max_length=150, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} ({self.start_date} → {self.end_date})"