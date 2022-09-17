from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Prefetch

from core.apps.products.models import Product
from core.apps.users.models import UserAccount
from .serializers import ProductSerializer, UserSerializer
from .permissions import IsProductOwner


def home(request, *args, **kwargs):
    return redirect('api:product_list')


class ProductList(APIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        qs = Product.active_products.all().select_related('user', 'category').prefetch_related('tags')
        serializer = ProductSerializer(qs, many=True, context={'request': self.request})
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data={**request.data, **kwargs})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(Product.active_products.all(), pk=pk)
        serializer = ProductSerializer(qs, context={'request': self.request})
        return Response(serializer.data)


class UserList(APIView):
    def get(self, request):
        qs = UserAccount.objects.filter(is_activated=True).select_related('location')
        serializer = UserSerializer(qs, many=True, context={'request': self.request})
        return Response(serializer.data)


class UserDetail(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(UserAccount, pk=pk, is_activated=True)
        serializer = UserSerializer(qs, context={'request': self.request})
        return Response(serializer.data)