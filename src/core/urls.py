from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

from core.apps.products.views import product_all
from core.apps.users.views import about_page

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/auth/', include('rest_framework.urls')),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns += i18n_patterns(
    path('', product_all, name='home'),
    path('about/', about_page, name='about_page'),
    path('products/', include('core.apps.products.urls', namespace='products')),
    path('users/', include('core.apps.users.urls', namespace='users')),
    path('chats/', include('core.apps.chats.urls', namespace='chats')),
    path('search/', include('core.apps.search.urls', namespace='search')),
    prefix_default_language=False
)

handler404 = 'core.views.custom_handler404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [
        *urlpatterns,
        path('__debug__/', include('debug_toolbar.urls'))
    ]
else:
    urlpatterns += re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
