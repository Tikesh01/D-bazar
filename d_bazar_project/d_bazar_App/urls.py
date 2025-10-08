from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('items/add',views.add_items, name='add_items'),
    path('items/delete',views.delete_items, name='delete_items'),
    path('items/edit',views.edit_items, name='edit_items'),
    path('<name>',views.render_page, name='<name>')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)