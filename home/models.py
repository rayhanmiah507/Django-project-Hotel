from django.db import models
import uuid
from django.contrib.auth.models import User 


class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at= models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    
 
    

class Amenities(BaseModel):
    amenities_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.amenities_name

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    hotel_price=models.IntegerField()
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)
    
    def __str__(self):
        return self.hotel_name
    
class HotelImage(BaseModel):
    hotels = models.ForeignKey(Hotel, on_delete = models.CASCADE,  related_name='hotels_name')
    image= models.ImageField(upload_to='hotels')
    

class HotelBooking(BaseModel):
    hotels=models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotels_booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_booking')
    start_date = models.DateField()
    end_date = models.DateField()
  
    booking_type = models.CharField(max_length=20, choices=(('Pre Paid', 'Pre Paid'), ('Post Paid', 'Post Paid')))