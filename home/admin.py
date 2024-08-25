from django.contrib import admin
from .models import BaseModel, Amenities, Hotel,HotelImage,HotelBooking

admin.site.register(BaseModel)
admin.site.register(Amenities)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(HotelBooking)
