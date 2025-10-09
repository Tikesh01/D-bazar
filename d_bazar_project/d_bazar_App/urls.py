from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('items/add',views.add_items, name='add_items'),
    path('signup', views.signup, name='signup'),
    path('verify-otp', views.verify_otp, name='verify_otp'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('items/delete',views.delete_items, name='delete_items'),
    path('items/edit',views.edit_items, name='edit_items'),
    # path('<name>',views.render_page, name='<name>')
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve media files in production
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
