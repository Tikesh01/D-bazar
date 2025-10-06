from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('add-items',views.add_items, name='add_items'),
    path('delete-items',views.delete_items, name='delete_items'),
    path('<name>',views.render_page, name='<name>')
]