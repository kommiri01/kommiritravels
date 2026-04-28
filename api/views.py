from rest_framework import generics
from .models import Review, Booking
from .serializers import ReviewSerializer, BookingSerializer

# Existing Review Logic
class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(is_approved=True).order_by('-created_at')
    def perform_create(self, serializer):
        from django.contrib.auth.models import User
        first_user = User.objects.first() 
        serializer.save(user=first_user, is_approved=False)

# NEW: Booking Logic
# Change CreateAPIView to ListCreateAPIView
class BookingListCreate(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    # 1. This handles fetching the history
    def get_queryset(self):
        # Fetch bookings, newest first
        return Booking.objects.all().order_by('-created_at')

    # 2. This handles creating a new booking
    def perform_create(self, serializer):
        from django.contrib.auth.models import User
        first_user = User.objects.first()
        serializer.save(user=first_user)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile

class UpdateProfile(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        phone = request.data.get('phone')
        address = request.data.get('address')

        if not email:
            return Response({"error": "Email is required"}, status=400)

        # 1. Find or Create the core User by their Email
        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        user.first_name = name
        user.save()

        # 2. Find or Create their attached Profile and save the extra details
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = phone
        profile.address = address
        profile.save()

        return Response({"message": "Profile saved successfully!"})