from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),

    path('my-wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('add-to-wishlist/<slug:product_id>', views.add_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<slug:product_id>', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('<int:id>', views.user_profile, name='profile'),
]
