from django.urls import path

from . import views


app_name = 'products'

urlpatterns = [
    path('', views.product_all, name='home'),

    path('add', views.product_add, name='add'),
    path('<slug:pk>', views.product_detail, name='detail'),
    path('<slug:pk>/edit', views.product_edit, name='edit'),
    path('<slug:pk>/edit/remove-image', views.remove_image, name='remove_image'),
    path('<slug:pk>/remove', views.product_remove, name='remove'),

    path('category/<str:category_name>', views.category, name='category'),
]
