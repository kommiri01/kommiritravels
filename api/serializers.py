from rest_framework import serializers
from .models import Review, Booking

# Existing Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'username', 'trip_type', 'rating', 'review_text', 'created_at']

# NEW: Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'pickup_location', 'drop_location', 'travel_date', 'cab_type', 'status', 'created_at']