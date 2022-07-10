from django.urls import path

from . import views


app_name = 'products'

urlpatterns = [
    path('', views.product_all, name='home'),

    path('add', views.product_add, name='add'),
    path('<slug:uid>', views.product_detail, name='detail'),
    path('<slug:uid>/edit', views.product_edit, name='edit'),
    path('<slug:uid>/remove', views.product_remove, name='remove'),

    path('category/<int:id>', views.category, name='category'),
]
