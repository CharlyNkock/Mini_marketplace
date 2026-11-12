from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'category', 'price_per_day',
            'location_name', 'latitude', 'longitude', 'created_at',
            'owner', 'owner_username',
        ]
        read_only_fields = ['owner', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    renter_username = serializers.CharField(source='renter.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'renter', 'renter_username',
            'start_date', 'end_date', 'status', 'total_price', 'created_at',
        ]
        read_only_fields = ['renter', 'status', 'total_price', 'created_at']

    def validate(self, data):
        listing = data['listing']
        start = data['start_date']
        end = data['end_date']
        user = self.context['request'].user

        if end < start:
            raise serializers.ValidationError("La date de fin doit être après la date de début.")
        if start < timezone.localdate():
            raise serializers.ValidationError("La date de début ne peut pas être dans le passé.")
        if listing.owner == user:
            raise serializers.ValidationError("Tu ne peux pas réserver ta propre annonce.")

        overlapping = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],
            start_date__lte=end,
            end_date__gte=start,
        ).exists()
        if overlapping:
            raise serializers.ValidationError(
                "Cet objet est déjà réservé sur tout ou partie de ces dates."
            )
        return data