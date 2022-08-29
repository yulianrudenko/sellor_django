from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('resend-activation-email/<slug:user_id>', views.resend_activation_email, name='resend_activation'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/upvote', views.upvote_feedback, name='upvote_feedback'),
    path('feedback/delete', views.delete_feedback, name='delete_feedback'),

    path('<int:pk>', views.user_profile, name='profile'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit-profile/remove-image', views.remove_image, name='remove_image'),

    path('change-password/', views.change_password, name='change_password'),
    path('change-to-new-password/<uidb64>/<uidb64_2>/<token>', views.change_to_new_password, name='confirm_new_password'),

    path('my-wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<slug:product_id>', views.add_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<slug:product_id>', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('<int:user_reported_id>/report', views.report_user, name='report'),
    path('<slug:user_reported_id>_<slug:message_id>/report', views.report_user, name='report'),

    path('blocked_users/', views.blocked_users, name='blocked'),
    path('blocked_users/remove/<int:user_id>', views.unblock_user, name='unblock'),
]
