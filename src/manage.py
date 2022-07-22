#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellor.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)

    # check for categories to insert into DB for every migration
    if len(sys.argv) == 2 and sys.argv[1] == 'migrate':
        # script that updates or creates 'fixtures/products_categories'.json with all the settings.CATEGORY_CHOICES
        execute_from_command_line(['manage.py', 'runscript', 'get_categories_to_fixture'])
        # performs the data load with data from previoulsy updated/created 'products_categories.json'
        execute_from_command_line(['manage.py', 'loaddata', 'products_categories.json'])


if __name__ == '__main__':
    main()
