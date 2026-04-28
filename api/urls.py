from django.urls import path
from .views import ReviewListCreate, BookingListCreate, UpdateProfile # <--- Import it

urlpatterns = [
    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('bookings/', BookingListCreate.as_view(), name='booking-list-create'),
    path('profile/update/', UpdateProfile.as_view(), name='profile-update'), # <--- Add this route
]