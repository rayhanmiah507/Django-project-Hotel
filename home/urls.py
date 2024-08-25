from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name='home'),
    path('login/',login_page, name='login'),
    path('register/',register_page, name='register'),
    path('logout', logout, name='logout'),
    path('hotel-detail/<uid>/', hotel_detail, name='hotel_detail'),
    path('booking/', check_booking, name='check_booking'),
    path('search/', search_hotels, name='search_hotels'),
]
