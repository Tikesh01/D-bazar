from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Item, User
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, get_user_model
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

def home(request):
    return render(request,'d_bazar_App/home.html', context)

def signup(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')


        username = email 

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('home')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        print(f"Generated OTP for {email}: {otp}") 

        # Create inactive user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.mobile_number = mobile
        myuser.otp = otp
        myuser.is_active = False
        myuser.save()

        # Store email in session to know who is verifying
        request.session['signup_email'] = email

        messages.success(request, "An OTP has been sent to your email. Please verify.")
        return redirect('home') # Redirect and show OTP form via JS

    else:
        return HttpResponse("404 - Not Found")

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.session.get('signup_email')
        if not email:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect('home')

        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_active = True
                user.otp = None # Clear OTP
                user.save()
                del request.session['signup_email']
                messages.success(request, "Account verified successfully! You can now log in.")
            else:
                messages.error(request, "Invalid OTP.")
        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
        return redirect('home')
    return HttpResponse("404 - Not Found")

def handlelogin(request):
    if request.method == 'POST':
        loginemail = request.POST.get('email')
        loginpass = request.POST.get('password')
        user = authenticate(request, email=loginemail, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('home')
    return HttpResponse("404- Not Found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

def admin(request):
    return render(request,'d_bazar_App/admin.html', context)

@require_http_methods(["POST"])
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
        messages.error(request, f'Failed to add item. Error: {e}')
    return redirect('admin')

@require_http_methods(["POST"])
def delete_items(request):
    item_id = request.POST.get('item_id')
    if item_id:
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            w.items = Item.objects.all()
            
            messages.success(request,'Item Deleted successfuly!')
        except ObjectDoesNotExist:
            messages.error(request, 'Item not found.')
        except Exception as e:
            messages.error(request, f'Error deleting item: {e}')
    else:
        messages.error(request, 'No item ID provided.')
    return redirect('admin')

@require_http_methods(["POST"])
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
        messages.error(request, 'Item not found.')
    except Exception as e:
        messages.error(request, f'Failed to edit item. Error: {e}')
    return redirect('admin')
        
def render_page(request, name):
    if name == 'home':
        return redirect('home')
    elif name == 'favicon.ico':
        return HttpResponse(status=404)

    template_path = f'd_bazar_App/{name}.html'
    try:
        return render(request, template_path)
    except:
        return redirect('home')
