import datetime

from rest_framework import serializers
from django.urls import reverse

from core.apps.products.models import Product, Category, Tag
from core.apps.users.models import UserAccount


class ProductSerializer(serializers.Serializer):
    website_url = serializers.HyperlinkedIdentityField(view_name='products:detail')
    api_url = serializers.HyperlinkedIdentityField(view_name='api:product_detail')
    title = serializers.CharField()
    category = serializers.CharField(source='category.name')
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='api:user_detail')
    current_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    description = serializers.CharField()
    tags = serializers.SerializerMethodField()
    publicated = serializers.SerializerMethodField()

    def get_tags(self, obj):
        tags = ''
        for tag in obj.tags.all():
            tags += f'{tag.name}, '
        if tags:
            return tags[:-2]
        return tags

    def get_publicated(self, obj):
        return obj.pub_date.strftime('%d.%m.%Y')

    def create(self, validated_data, *args, **kwargs):
        print(validated_data, args, kwargs)
        # take out category
        try:
            category = Category.objects.get(name=validated_data.pop('category').get('name')) 
        except:
            raise serializers.ValidationError(({'category': 'Please enter valid category name.'}), code=400)
        validated_data['category'] = category
        # take out tags
        if validated_data.get('tags'):
            try:
                tags = Tag.objects.filter(name__in=validated_data.pop('tags').get('name')) 
            except:
                raise serializers.ValidationError(({'tags': 'Please enter valid tag name'}), code=400)
        # validate price
        if not validated_data.get('price'):
            raise serializers.ValidationError({'price': 'Please enter price.'}, code=400)
        try:
            price = Category.objects.get(name=validated_data.pop('tags').get('name')) 
        except:
            raise serializers.ValidationError(({'tags': 'Please enter valid tag name'}), code=400)
        if validated_data.get('discount_price'):
            try:
                category = Category.objects.get(name=validated_data.pop('tags').get('name')) 
            except:
                raise serializers.ValidationError(({'tags': 'Please enter valid tag name'}), code=400)
        return Product.objects.create(**validated_data)

class UserSerializer(serializers.Serializer):
    website_url = serializers.HyperlinkedIdentityField(view_name='users:profile')
    api_url = serializers.HyperlinkedIdentityField(view_name='api:user_detail')
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    location = serializers.CharField(source='location.name')
    gender = serializers.CharField()
    sold = serializers.SerializerMethodField()
    purchased = serializers.SerializerMethodField()
    joined = serializers.DateTimeField(source='date_created', read_only=True, format="%d.%m.%Y")
    active_products = serializers.HyperlinkedRelatedField(view_name='api:product_detail', many=True, read_only=True)

    def get_sold(self, obj):
        return obj.sold_count

    def get_purchased(self, obj):
        return obj.purchased_count
