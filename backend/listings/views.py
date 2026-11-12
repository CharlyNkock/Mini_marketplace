from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, permissions, generics, mixins
from .models import Listing, Booking
from .serializers import ListingSerializer, RegisterSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Listing.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(
            Q(renter=user) | Q(listing__owner=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        start = serializer.validated_data['start_date']
        end = serializer.validated_data['end_date']
        days = (end - start).days + 1
        serializer.save(
            renter=self.request.user,
            total_price=listing.price_per_day * days,
        )