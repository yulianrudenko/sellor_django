import os
import json

def get_fixtures_directory() -> str:
    '''
    Return fixture directory where fixtures (json files) with models' data are stored
    '''
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')) + '/fixtures'


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