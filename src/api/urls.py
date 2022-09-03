from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ListProducts.as_view(), name='product_all'),
    path('products/<slug:pk>', views.ListProducts.as_view(), name='product_detail'),

    path('users/', views.ListUsers.as_view(), name='user_all'),
    path('users/<int:pk>', views.ListUsers.as_view(), name='user_detail'),
]
