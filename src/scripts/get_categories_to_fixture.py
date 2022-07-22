import json
import path
import sys
import os

from django.conf import settings


def run():
    # declare sellor.settings before accessing to prevent errors
    src_directory = path.Path(__file__).abspath().parent.parent
    sys.path.append(src_directory)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'sellor.settings'

    categories = [category1 for category1, category2 in settings.CATEGORY_CHOICES]
    categories_fixtures = list()

    # Inserting categories data as dictionary 
    for pk, category_name in enumerate(categories, start=1):
        categories_fixtures.append({
            'model': 'products.category',
            'pk': pk,
            'fields': {"name": category_name}
        })

    # Serializing json
    json_object = json.dumps(categories_fixtures, indent=4)

    # Writing to sample.json
    with open(f'{src_directory}/fixtures/products_categories.json', 'w') as f:
        f.write(json_object)
