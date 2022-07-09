from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from sellor.apps.products.views import product_all

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    
    path('', product_all, name='home'),
    path('products/', include('sellor.apps.products.urls', namespace='products')),

    path('users/', include('sellor.apps.users.urls', namespace='users')),
    path('cart/', include('sellor.apps.cart.urls', namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)

