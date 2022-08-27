import json

from django.shortcuts import render
from django.conf import settings

from core.apps.products.models import Product, Tag
from core.utils import available_products
from .forms import ProductSearchForm


def main(request):
    data = request.GET
    form = ProductSearchForm(data)

    if request.user.is_authenticated:
        products_qs =  available_products(request, Product.objects)
    else:
        products_qs = Product.active_products.all()

    if data.get('location'):
        products_qs = products_qs.filter(user__location__in=data.getlist('location'))

    if data.get('category'):
        categories = [int(id) for id in data.getlist('category')]
        products_qs = products_qs.filter(category__in=categories)

    if data.get('tags'):
        tags = [int(id) for id in data.getlist('tags')]
        tags = Tag.objects.filter(id__in=tags)
        temp_qs = Product.objects.none()
        for tag in tags:
            temp_qs |= products_qs & tag.products.all()
        products_qs = temp_qs

    title = data.get('title')
    if title:
        if settings.DEBUG:
            products_qs = products_qs.filter(title__search=title)
        else:
            from django.contrib.postgres.search import TrigramDistance
            products_qs = products_qs.annotate(
                distance=TrigramDistance('title', title),
            ).filter(distance__lte=0.8).order_by('distance')
        # from django.contrib.postgres.search import TrigramWordSimilarity
        # products_qs = products_qs.annotate(
        #     similarity=TrigramWordSimilarity(title, 'title'),
        # ).filter(similarity__gt=0.7).order_by('-similarity')
    
    context = {'form': form, 'products_qs': products_qs}
    return render(request, 'search/search.html', context)
