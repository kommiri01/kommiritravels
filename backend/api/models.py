from django.db import models
from django.contrib.auth.models import User

# 1. User Profile (Expands the default Django User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferred_language = models.CharField(max_length=50, default="English")

    def __str__(self):
        return self.user.username

# 2. Customer Reviews
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_type = models.CharField(max_length=100) # e.g., "Tirupati Darshan"
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) # False so you can approve them first!

    def __str__(self):
        return f"{self.user.username} - {self.trip_type} ({self.rating} Stars)"

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=100) # e.g., "Innova Crysta"
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.vehicle_type})"

# 3. Cab Bookings
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    travel_date = models.DateField()
    
    # NEW: The precise time they want the cab
    pickup_time = models.TimeField(null=True, blank=True) 
    
    cab_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # NEW: Connects the booking to a specific driver!
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} | {self.pickup_location} to {self.drop_location}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client

# This function runs automatically EVERY TIME a booking is saved
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client

@receiver(post_save, sender=Booking)
def notify_driver_on_assignment(sender, instance, created, **kwargs):
    # If the booking is NOT new, AND it has a driver, AND it is Confirmed
    if not created and instance.driver and instance.status == 'Confirmed':
        
        # 1. Format the phone number (Twilio STRICTLY requires the country code)
        driver_phone = "+91" + instance.driver.phone_number[-10:] 
        
        # 2. Your Twilio Credentials
        account_sid = "AC34661e22b862d96452605decf6c709dc"
        auth_token = "8397dc748ba6295a0c60444cc0635611"
        twilio_number = "+1 947 957 5070" # e.g., "+1234567890"
        
        # 3. Send the text via Twilio
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"Kommiri Travels: NEW TRIP! Pickup at {instance.pickup_location} on {instance.travel_date} at {instance.pickup_time}. Drop: {instance.drop_location}.",
                from_=twilio_number,
                to=driver_phone
            )
            print(f"\n✅ TWILIO SUCCESS! Message ID: {message.sid}")
        except Exception as e:
            print("\n❌ TWILIO ERROR:", str(e))
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True) # <--- Make sure you have this!

    def __str__(self):
        return f"{self.user.first_name} ({self.user.email})"