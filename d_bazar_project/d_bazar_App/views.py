from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Item

import os
# Create your views here.

class web:
    def __init__(self):
        self.pages = (page.replace('.html', '') for page in os.listdir('d_bazar_App/templates/d_bazar_App') if page.endswith('.html'))
        self.pagesNotToView = ('admin','base')
        self.pagesToView = [page for page in self.pages if page not in self.pagesNotToView]
        self.db = Item.objects.all()
w = web()
context = {'web':w}
def home(request):
    return render(request,'d_bazar_App/home.html', context)

def admin(request):
    return render(request,'d_bazar_App/admin.html', context)

def add_items(request):
    if request.method == 'GET':
        pos = request.GET.get('pos')
        img = request.GET.get('image')
        tit = request.GET.get('title')
        des = request.GET.get('description')
        pricing = request.GET.get('price')
        amt = request.GET.get('amount')
        spec = request.GET.get('special')
        
        items = Item.objects.create(pos=pos, image=img, title=tit, description=des, price=pricing, amount=amt, special=spec)
        items.save()
        
        messages.success(request,'Item added successfuly!')

    return redirect('admin')

def delete_items(request):
    if request.method == 'GET':
        id = request.GET.get('item_id')
        
        items = Item.objects.get(id=id)
        items.delete()
        items.save()
        messages.success(request,'Item Deleted successfuly!')

    return redirect('admin')
        
def render_page(request, name):
    if name=='home':
        return redirect('home')
    elif name in w.pages:
        return render(request, f'd_bazar_App/{name}.html', context)
    else:
        redirect('home')
    return render(request, f'd_bazar_App/{name}.html', context)
    