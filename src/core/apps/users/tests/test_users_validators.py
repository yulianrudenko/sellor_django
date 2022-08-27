import pytest

from django.test import TestCase
from django.forms import ValidationError

from core.apps.users.validators import password_validator

@pytest.mark.parametrize(
    'password, error_text, valid',
    [
        ('123456', '', True),
        ('123 456', 'Password must <em>not</em> contain spaces.', False),
        ('12345', 'The password must be 6-30 characters', False),
        ('1234567890123456789012345678901', 'The password must be 6-30 characters', False),
    ],
)
def test_password_validator(password, error_text, valid):
    if valid:
        assert password_validator(password) == password
    else:
        with pytest.raises(ValidationError) as error:
            password_validator(password)
        assert str(error.value.message) == error_text 
