from django.urls import path

from api.views import ProductsListAPIView

app_name = 'api'

urlpatterns = [
    path('products/', ProductsListAPIView.as_view(), name='products'),
]