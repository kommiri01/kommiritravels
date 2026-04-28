from django.contrib import admin
from .models import UserProfile, Review, Booking, Driver # <--- Import Driver

admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(Driver) # <--- Register it