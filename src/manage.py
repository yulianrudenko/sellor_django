import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dir.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)

    # check for fixture-data to insert into DB for every migration
    if len(sys.argv) == 2 and sys.argv[1] == 'migrate':
        execute_from_command_line([
            'manage.py', 'loaddata',
            'categories_fixture.json',
            'tags_fixture.json'])


if __name__ == '__main__':
    main()
