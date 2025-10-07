from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Item
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

import os
# Create your views here.

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
            special=request.POST.get('special') or None # Handle empty string for optional field
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


