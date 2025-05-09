from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from django.core.mail import send_mail
from django.conf import settings

from django.views.decorators.cache import never_cache




# Create your views here.

def index(request):
    return render(request,'index.html')

def Events(request):
    return render(request,'events.html')

def about(request):
    band_members = [
        {"name": "Arjun", "role": "Lead Vocalist", "image": "images/singer1.png"},
        {"name": "Sneha", "role": "Keyboardist", "image": "images/singer2.png"},
        {"name": "Ravi", "role": "Drummer", "image": "images/singer3.png"},
        {"name": "Nikita", "role": "Bassist", "image": "images/singer4.png"},
        {"name": "Manoj", "role": "Guitarist", "image": "images/singer5.png"},
        {"name": "Priya", "role": "DJ & FX", "image": "images/singer6.png"},
    ]
    return render(request, "about.html", {"band_members": band_members})


# def booking_form(request):
#     if 'user_id' in request.session:
#         if request.method == 'POST':
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             event_date = request.POST.get('event_date')
#             event_type = request.POST.get('event_type')
#             location = request.POST.get('location')
#             message = request.POST.get('message')

#             BookingRequest.objects.create(
#                 name=name,
#                 email=email,
#                 event_date=event_date,
#                 event_type=event_type,
#                 location=location,
#                 message=message
#             )
#             return redirect('booking_confirmation')

#         return render(request, 'booking_form.html')
#     else:
#         return redirect('login')

@never_cache
def booking_form(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            event_date = request.POST.get('event_date')
            event_type = request.POST.get('event_type')
            location = request.POST.get('location')
            message = request.POST.get('message')

            booking = BookingRequest.objects.create(
                name=name,
                email=email,
                event_date=event_date,
                event_type=event_type,
                location=location,
                message=message
            )

            # Send email notification to customer
            subject = "Event Booking Received"
            customer_message = f"""
Hi {name},

Thank you for booking your event with us!

Here are your booking details:
- Event Type: {event_type}
- Event Date: {event_date}
- Location: {location}

Our team will review your request and update you shortly.

Best Regards,
Your Event Team
"""

            send_mail(
                subject,
                customer_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect('booking_confirmation')

        return render(request, 'booking_form.html')
    else:
        return redirect('login')

@never_cache
def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        user = Register(
            name=username,
            email=email,
            password=make_password(password)
        )
        user.save()
        messages.success(request, f"Registered successfully! Your User ID is {user.id}.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(name=username)
            if check_password(password, user.password):  
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                messages.success(request, "Login successful!")
                return redirect('/')
            else:
                messages.error(request, "Invalid password.")
        except Register.DoesNotExist:
            messages.error(request, "Username not found.")

    return render(request, 'login.html')


# def logout_view(request):
#     request.session.flush()
#     messages.success(request, "Logged out successfully.")
#     return redirect('login')

def logout_view(request):
    request.session.flush()  # Clears all session data
    messages.success(request, "Logged out successfully.")
    return redirect('login')