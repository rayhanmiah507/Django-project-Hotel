from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib import messages 
from .models import Amenities, Hotel,HotelBooking
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.

def home(request):
    amenities=Amenities.objects.all()
    hotels = Hotel.objects.all()
    
    sort_by = request.GET.get('sort_by')
    # search = request.GET.get('search')
    amenitiess = request.GET.getlist('amenities')
    
    if sort_by:
        if sort_by == 'ASC':
            hotels = hotels.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels = hotels.order_by('-hotel_price')
    
    # if search:
    #     hotels = hotels.filter(
    #         Q(hotel_name__icontains = search) | Q(description__icontains = search) )
        
    
    if len(amenitiess):
        hotels = hotels.filter(amenities__amenities_name__in = amenitiess).distinct()
        
    context = {
        'amenities':amenities, 'hotels':hotels, 'sort_by':sort_by, 'amenitiess':amenitiess,
        }
    
    # Checkin Checkout
    
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        uid= request.POST.get('uid')
        
        booking_hotel_uids = HotelBooking.objects.filter(
            Q(start_date__lte=checkout, end_date__gte=checkin)|
            Q(start_date__range=[checkin,checkout])|
            Q(end_date__range=[checkin,checkout])
            
        ).values_list('hotels__uid', flat=True)
        
        hotels = hotels.exclude(uid__in=booking_hotel_uids)
        context['hotels'] = hotels
   
    return render(request,'home.html',context)


# search

def search_hotels(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        # Perform a case-insensitive search across multiple fields
        hotels = Hotel.objects.filter(
            Q(hotel_name__icontains=search_query) | 
            Q(description__icontains=search_query) 
            # Add more fields as needed
        )
        # Generate HTML markup for search results
        search_results_html = ''
        for hotel in hotels:
            # Extract portion of hotel data containing the search query
            highlighted_text = ''
            if search_query.lower() in hotel.hotel_name.lower():
                highlighted_text += f'Hotel Name: {hotel.hotel_name}'
            if search_query.lower() in hotel.description.lower():
                # Highlight the search query within the description
                highlighted_description = hotel.description.replace(search_query, f'<mark>{search_query}</mark>')
                highlighted_text += f'<br>Description: {highlighted_description}'
            # Add more fields as needed
            if highlighted_text:
                search_results_html += f'<div>{highlighted_text}</div>'
        return JsonResponse({'search_results_html': search_results_html})
    else:
        return JsonResponse({'search_results_html': ''})
    
    # login

def login_page(request):
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            
            return redirect('/')
        else:
             messages.info(request,"Invalid credentials")
             return redirect('login')
    return render(request,'login.html')

def register_page(request):
    
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        
        if password1 == password2:
            
            if User.objects.filter(email=email).exists():
              messages.success(request,"Email already taken")
              return redirect('register')
            
            elif User.objects.filter(username=username).exists():
                 messages.success(request,"Username already taken")
                 return redirect('register')
            else:   
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username, password=password1,email=email)
                user.save()
                print('User created')
                return redirect('/login')
        else:
            messages.success(request," Password not maching ")
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def hotel_detail(request, uid):
    hotel = get_object_or_404(Hotel, uid=uid)
    hotel_images = hotel.hotels_name.all()
    
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        hotels = Hotel.objects.get(uid=uid)
        if not check_booking(checkin,checkout, uid, hotels.room_count):
            messages.warning(request,"Hotel is already booked in these days")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        HotelBooking.objects.create(hotels=hotels, user=request.user, start_date=checkin, end_date=checkout,booking_type='Pre Paid' )
        messages.success(request,"Hotel booking has been saved")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'hotel_images': hotel_images})

def check_booking(start_date,end_date,uid,room_count  ):
    
    qs = HotelBooking.objects.filter(
        start_date__lte= start_date,
        end_date__gte = end_date,
         hotels__uid = uid
    )
    
    if len(qs) >= room_count:
        return False
    return True
    
   
   

