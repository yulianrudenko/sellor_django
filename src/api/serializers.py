from rest_framework.serializers import Serializer, ModelSerializer

from sellor.apps.products.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title']
