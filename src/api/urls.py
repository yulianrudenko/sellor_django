from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<slug:pk>', views.ProductDetail.as_view(), name='product_detail'),

    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
]
