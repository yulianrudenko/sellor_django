from rest_framework import serializers

from core.apps.products.models import Product
from core.apps.users.models import UserAccount


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='users:profile')
    location = serializers.CharField(source='location.name')
    joined = serializers.DateTimeField(source='date_created', read_only=True, format="%d.%m.%Y")
    total_sold = serializers.IntegerField(source='sold_count')
    total_purchased = serializers.IntegerField(source='purchased_count')
    active_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'user_url',
            'first_name',
            'last_name',
            'location',
            'gender',
            'joined',
            'total_sold',
            'total_purchased',
            'active_products'
        ]
        extra_kwargs = {
            'user_url': {'view_name': 'users:profile', 'lookup_field': 'pk'},
        }
    
    def get_active_products(self, obj):
        user = obj
        products_qs = user.products.filter(purchased_by=None)
        return UserProductsInlineSerializer(instance=products_qs, many=True, context=self.context).data

class UserProductsInlineSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.HyperlinkedIdentityField(view_name='api:products-detail', lookup_field='pk', read_only=True)
        

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.CharField(source='category.name')
    product_url = serializers.HyperlinkedIdentityField(view_name='products:detail')
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Product
        fields = [
            'product_url',
            'title',
            'category',
            'user',
            'current_price',
            'description',
        ]
        extra_kwargs = {
            'user': {'view_name': 'api:users-detail'},
        }
