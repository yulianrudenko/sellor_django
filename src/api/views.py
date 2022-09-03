from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from core.apps.products.models import Product
from core.apps.users.models import UserAccount
from .serializers import ProductSerializer, UserSerializer


class ListProducts(APIView):
    def get(self, request, pk=None):
        if pk:
            qs = get_object_or_404(Product.active_products.all(), pk=pk)
            serializer = ProductSerializer(qs, context={'request': self.request})
        else:
            qs = Product.active_products.all().select_related('user', 'category').prefetch_related('tags')
            serializer = ProductSerializer(qs, many=True, context={'request': self.request})
        return Response(serializer.data)


class ListUsers(APIView):
    def get(self, request, pk=None):
        if pk:
            qs = get_object_or_404(UserAccount, pk=pk, is_activated=True)
            serializer = UserSerializer(qs, context={'request': self.request})
        else:
            qs = UserAccount.objects.filter(is_activated=True).select_related('location')
            serializer = UserSerializer(qs, many=True, context={'request': self.request})
        return Response(serializer.data)