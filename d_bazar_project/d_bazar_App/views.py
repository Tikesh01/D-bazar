from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Item, User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from .decorators import admin_required
import random

import os

User = get_user_model()

class web:
    def __init__(self):
        self.pages = (page.replace('.html', '') for page in os.listdir('d_bazar_App/templates/d_bazar_App') if page.endswith('.html'))
        self.pagesNotToView = ('admin','base')
        self.pagesToView = [page for page in self.pages if page not in self.pagesNotToView]
        self.items = Item.objects.all()
        self.items_sorted = self.items.order_by('pos')
w = web()
context = {'web':w}

def send_otp_email(email, otp):
    """Sends an OTP to the user's email."""
    subject = 'Your D-Bazar Account Verification Code'
    message = f'Hi there,\n\nYour One-Time Password (OTP) for account verification is: {otp}\n\nThank you for joining D-Bazar!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    
def home(request):
    return render(request,'d_bazar_App/home.html', context)

def signup(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Validation
        if not all([mobile, email, pass1, pass2]):
            messages.warning(request, "All fields are required")
            return redirect('home')

        if pass1 != pass2:
            messages.warning(request, "Passwords do not match")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return redirect('home')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        try:
            # Send OTP via email
            send_otp_email(email, otp)
            
            # Create inactive user
            User.objects.create_user(
                email=email, 
                password=pass1,
                mobile_number=mobile,
                otp=otp,
                is_active=False
            )
            
            # Store email in session
            request.session['signup_email'] = email

            messages.success(request, "An OTP has been sent to your email. Please verify.")
            print(f"OTP for {email}: {otp}")  # For debugging
            return render(request, "d_bazar_App/otp_verification.html", context)
            
        except Exception as e:
            messages.warning(request, f"We could not send an OTP. Error: {str(e)}")
            return redirect('home')

    return HttpResponse("404 - Not Found")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        email = request.session.get('signup_email')
        
        if not email:
            messages.warning(request, "Session expired. Please sign up again.")
            return redirect('home')

        try:
            user = User.objects.get(email=email)
            
            # Check against both session and user OTP
            if entered_otp == user.otp:
                user.is_active = True
                user.otp = "" # Clear OTP after use
                user.save()
                
                # Clean up session
                del request.session['signup_email']
                    
                messages.success(request, "Account verified successfully! You can now log in.")
            else:
                messages.warning(request, "Invalid OTP.")
                
        except User.DoesNotExist:
            messages.warning(request, "User not found. Please sign up again.")
            
        return redirect('home')
        
    return HttpResponse("404 - Not Found")

def handlelogin(request):
    if request.method == 'POST':
        loginemail = request.POST.get('email')
        loginpass = request.POST.get('password')
        user = authenticate(request, email=loginemail, password=loginpass)

        if user is not None:
            login(request, user)
            # Check if the user is a staff member (admin)
            if user.is_staff:
                messages.success(request, f"Welcome Admin, {user.email}!")
                return redirect('admin_dashboard')
                
            else:
                messages.success(request, "Successfully Logged In")
                return redirect('home')
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect('home')

    return HttpResponse("404- Not Found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

@admin_required
def admin_dashboard(request):
    return render(request,'d_bazar_App/admin.html', context)

@require_http_methods(["POST"])
@admin_required
def add_items(request):
    try:
        Item.objects.create(
            pos=request.POST.get('pos'),
            image=request.FILES.get('image'),
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            amount=request.POST.get('amount'),
            special=request.POST.get('special') or None 
        )
        w.items = Item.objects.all()
        messages.success(request,'Item added successfuly!')
    except Exception as e:
        messages.warning(request, f'Failed to add item. Error: {e}')
    return redirect('admin_dashboard')

@require_http_methods(["POST"])
@admin_required
def delete_items(request):
    item_id = request.POST.get('item_id')
    if item_id:
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            w.items = Item.objects.all()
            
            messages.success(request,'Item Deleted successfuly!')
        except ObjectDoesNotExist:
            messages.warning(request, 'Item not found.')
        except Exception as e:
            messages.warning(request, f'Error deleting item: {e}')
    else:
        messages.error(request, 'No item ID provided.')
    return redirect('admin_dashboard')

@require_http_methods(["POST"])
@admin_required
def edit_items(request):
    try:
        item_id =  request.POST.get('item_id')
        item = Item.objects.get(id=item_id)

        item.pos = request.POST.get('pos', item.pos)
        item.title = request.POST.get('title', item.title)
        item.description = request.POST.get('description', item.description)
        item.price = request.POST.get('price', item.price)
        item.amount = request.POST.get('amount', item.amount)
        item.special = request.POST.get('special', item.special)

        new_image = request.FILES.get('image')
        if new_image:
            item.image = new_image

        item.save()
        w.items = Item.objects.all()
        messages.success(request,'Item edited successfuly!')
    except ObjectDoesNotExist:
        messages.warning(request, 'Item not found.')
    except Exception as e:
        messages.warning(request, f'Failed to edit item. Error: {e}')
    return redirect('admin_dashboard')
        
