import json
import path
import sys
import os

from django.conf import settings


def categories_list_to_json(categories_list):
    categories_fixtures = list()
    # Inserting categories data as dictionary 
    for pk, category_name in enumerate(categories_list, start=1):
        categories_fixtures.append({
            'model': 'products.category',
            'pk': pk,
            'fields': {"name": category_name}
        })
    return categories_fixtures


def tags_list_to_json(tags_list):
    tags_fixtures = list()
    # Inserting categories data as dictionary 
    for pk, tag_name in enumerate(tags_list, start=1):
        tags_fixtures.append({
            'model': 'products.tag',
            'pk': pk,
            'fields': {"name": tag_name}
        })
    return tags_fixtures


def shippings_list_to_json(shippings_list):
    shippings_fixtures = list()
    # Inserting shippings data as dictionary
    for pk, shipping_obj in enumerate(shippings_list, start=1):
        shippings_fixtures.append({
            'model': 'orders.shipping',
            'pk': pk,
            'fields': {
                "type": shipping_obj.type,
                "description": shipping_obj.description,
                "price": shipping_obj.price
            }
        })
    return shippings_fixtures


def run():
    # declare sellor.settings before accessing to prevent errors
    src_directory = path.Path(__file__).abspath().parent.parent
    sys.path.append(src_directory)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'sellor.settings'

    categories_list = [category1 for category1, category2 in settings.CATEGORY_CHOICES]
    fixtures_list = categories_list_to_json(categories_list)
    
    tags_list = [tag1 for tag1, tag2 in settings.TAG_CHOICES]
    fixtures_list = [*fixtures_list, *tags_list_to_json(tags_list)]

    shippings_list = settings.SHIPPINGS
    fixtures_list = [*fixtures_list, *shippings_list_to_json(shippings_list)]

    # Serializing json
    fixtures_json = json.dumps(fixtures_list, indent=4)

    # Creating products_fixtures.json, writing categories and tags to it
    with open(f'{src_directory}/fixtures/products_fixtures.json', 'w') as f:
        f.write(fixtures_json)
