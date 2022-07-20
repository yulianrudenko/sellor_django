from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import ProductSerializer
from sellor.apps.products.models import Product


class ProductsListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()