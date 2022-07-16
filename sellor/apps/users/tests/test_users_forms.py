import pytest
from django.forms import ValidationError

from sellor.apps.users.forms import (
    RegistrationForm,
    LoginForm,
    UserEditForm,
    UserChangePasswordForm
)


@pytest.mark.parametrize(
    'email, first_name, last_name, password1, password2, phone, gender, location, valid',
    [
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '', 'M', '', True),
        ('mikeowen@gmail.com', 'Mike1', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '', 'M', '', False),  # invalid first name
        ('mikeowen@gmail.com', 'Mike', 'Owen2', 'zaq1@WSX', 'zaq1@WSX', '', 'M', '', False),  # invalid last name
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '12345', 'M', '', False),  # invalid phone(too short)
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '+481234567', 'M', '', False),  # invalid phone(must be defined with digits only)
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'new', '', 'M', '', False),  # password do not much
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'short', 'short', '', 'M', '', False),  # password is too short
    ],
)
@pytest.mark.django_db
def test_registration_form(email, first_name, last_name, password1, password2, phone, gender, location, valid):
    registration_form = RegistrationForm(
        data={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password1': password1,
            'password2': password2,
            'phone': phone,
            'gender': gender,
            'location': location
        }
    )
    assert registration_form.is_valid() is valid


@pytest.mark.parametrize(
    'email, password, valid',
    [
        ('mikeowen@gmail.com',  'zaq1@WSX', False),
        ('user@gmail.com',  '123456', True),
    ],
)
@pytest.mark.django_db
def test_login_form(email, password, valid, user_account):
    login_form = LoginForm(
        data={
            'email': email,
            'password': password,
        }
    )
    assert login_form.is_valid() is valid



# @pytest.mark.parametrize(
#     'email, password, valid',
#     [
#         ('mikeowen@gmail.com',  'zaq1@WSX', True),
#     ],
# )
@pytest.mark.django_db
def test_edit_form(user_account):
    edit_form = UserEditForm(
        data={
            'first_name': 'newname',
            'last_name': user_account.last_name,
        },
        instance=user_account
    )
    assert edit_form.is_valid() == True
    edit_form.save()
    assert user_account.first_name == 'Newname'


@pytest.mark.parametrize(
    'current_password, new_password, verify_new_password, valid',
    [
        ('123456', 'new_valid_password',  'new_valid_password', True),
        ('wrong_current_password', 'new_valid_password',  'new_valid_password', False),
        ('123456', 'new_valid_password',  'new_but_invalid_password', False),
    ],
)
@pytest.mark.django_db
def test_change_password_form(user_account, current_password, new_password, verify_new_password, valid):
    from sellor.apps.users.models import UserAccount
    print(user_account.password)
    change_password_form = UserChangePasswordForm(
        data={
            'current_password': current_password,
            'new_password': new_password,
            'verify_new_password': verify_new_password,
            'user': user_account
        },
    )
    assert change_password_form.is_valid() == valid
