import os
import json

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.db.models import Q


def available_products(request, products):
    user = request.user
    if user.is_authenticated:
        # exclude products posted by users that blocked me and users that are blocked by me
        return products.exclude(
            Q(user__in=user.blocked_by_others.all().values_list('owner')) | \
                Q(user__in=user.blacklist.blocked_users.all())
        )
    return products.all()


def redirect_home_if_authenticated(function, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:home')
        return function(request, *args, **kwargs)
    return wrapper


def previous_url_or_other(request, other_url):
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url)
    return redirect(other_url)


def get_fixtures_directory() -> str:
    '''
    Return fixture directory where fixtures (json files) with models' data are stored
    '''
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')) + '/fixtures'


def create_or_update_fixture_signal(sender, instance, created, raw: bool, fixture_file_dir: str, fields: tuple,  *args, **kwargs):
    if raw == False:
        objects_list = json.load(open(fixture_file_dir))
        sender_str = sender.__name__.lower()
        if created:
            obj_fields = dict()
            for field in fields:
                obj_fields[field] = str(getattr(instance, field))
            new_object_dict = {
                "model": f"{sender._meta.app_label}.{sender_str}",  # e.g. "products.category"
                "pk": instance.id,
                "fields": obj_fields
            }
            objects_list.append(new_object_dict)
            objects_json = json.dumps(objects_list, indent=4)
            with open(fixture_file_dir, 'w') as fixture_file:
                fixture_file.write(objects_json)

        else:
            obj_fields = dict()
            for field in fields:
                obj_fields[field] = str(getattr(instance, field))
            new_object_dict = {
                "model": f"{sender._meta.app_label}.{sender_str}",  # e.g. "products.category"
                "pk": instance.id,
                "fields": obj_fields
            }
            for ind, obj in enumerate(objects_list):
                if obj['pk'] == instance.pk:
                    objects_list[ind] = new_object_dict
                    break
            objects_json = json.dumps(objects_list, indent=4)
            with open(fixture_file_dir, 'w+') as fixture_file:
                fixture_file.write(objects_json)


def delete_fixture_signal(sender, instance, fixture_file_dir: str,  *args, **kwargs):
    objects_list = json.load(open(fixture_file_dir))
    for ind, obj in enumerate(objects_list):
        if obj['pk'] == instance.pk:
            objects_list.pop(ind)
            break
    objects_json = json.dumps(objects_list, indent=4)
    with open(fixture_file_dir, 'w+') as fixture_file:
        fixture_file.write(objects_json)



def get_choices_from_fixture(fixture_name_plural: str, choice_field_name: str) -> list:
    '''
    Retrieve and return all values of instances' field that is used in one of model's field with choices
    from json-fixture

    For example:
    Model Category has name as Varchar field with choices
    To get all the choices for category.name field from 'fixtures/categories_fixture.json' you should do:
        ----------------------------------------------------------------
        CATEGORY_CHOICES = get_choices_from_fixture(fixture_name_plural='categories', choice_field_name='name')
        ----------------------------------------------------------------
    '''
    CHOICES = []
    fixture_directory = get_fixtures_directory() + f'/{fixture_name_plural}_fixture.json'
    with open(fixture_directory, 'r') as fixture_file:
        instance_list = json.loads(fixture_file.read())
        for instance in instance_list:
            choice_field_value = instance.get('fields').get(choice_field_name)
            CHOICES.append((choice_field_value, choice_field_value.capitalize()))
    return CHOICES