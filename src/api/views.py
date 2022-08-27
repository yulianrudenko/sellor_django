from rest_framework import viewsets

from .serializers import ProductSerializer, UserSerializer
from core.apps.products.models import Product
from core.apps.users.models import UserAccount


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.active_products.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = UserAccount.objects.all()