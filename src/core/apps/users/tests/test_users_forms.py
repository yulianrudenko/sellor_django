import pytest
from django.forms import ValidationError

from core.apps.users.forms import (
    RegistrationForm,
    LoginForm,
    UserEditForm,
    UserChangePasswordForm,
    ReportForm
)
from tests.models_setup import ModelsSetUp


@pytest.mark.parametrize(
    'email, first_name, last_name, password1, password2, phone, gender, valid',
    [
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '', 'M', True),
        ('mikeowen@gmail.com', 'Mike1', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '', 'M', False),  # invalid first name
        ('mikeowen@gmail.com', 'Mike', 'Owen2', 'zaq1@WSX', 'zaq1@WSX', '', 'M', False),  # invalid last name
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '12345', 'M', False),  # invalid phone(too short)
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'zaq1@WSX', '+481234567', 'M', False),  # invalid phone(must be defined with digits only)
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'zaq1@WSX', 'new', '', 'M', False),  # password do not much
        ('mikeowen@gmail.com', 'Mike', 'Owen', 'short', 'short', '', 'M', False),  # password is too short
    ],
)
@pytest.mark.django_db
def test_registration_form(email, first_name, last_name, password1, password2, phone, gender, valid, city):
    registration_form = RegistrationForm(data={
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password1': password1,
        'password2': password2,
        'phone': phone,
        'gender': gender,
        'location': city
    })
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
    login_form = LoginForm(data={
        'email': email,
        'password': password,
    })
    assert login_form.is_valid() is valid


@pytest.mark.django_db
def test_edit_form(user_account, city):
    edit_form = UserEditForm(data={
        'first_name': 'newname',
        'last_name': user_account.last_name,
        'location': city
    }, instance=user_account)
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
    change_password_form = UserChangePasswordForm(data={
        'current_password': current_password,
        'new_password': new_password,
        'verify_new_password': verify_new_password,
        'user': user_account
    })
    assert change_password_form.is_valid() == valid


# @pytest.mark.parametrize(
#     'reported_message, reason, confirmation, valid',
#     [
#         ('1', '',  'x', False),
#         ('1', None,  'YES', True),
#         (None, 'some reason for user report',  'YES', True),
#     ],
# )

class ReportFormTests(ModelsSetUp):
    def test_report_form1(self):
        report_form = ReportForm(data={
            'reported_message': self.message.id,
            'reason': None,
            'confirmation': '...'
        })
        assert report_form.is_valid() == False
    
    def test_report_form2(self):
        report_form = ReportForm(data={
            'reported_message': self.message.id,
            'reason': None,
            'confirmation': 'YES'
        })
        assert report_form.is_valid() == True
    
    def test_report_form3(self):
        report_form = ReportForm(data={
            'reported_message': None,
            'reason': 'some good reason to report',
            'confirmation': 'YES'
        })
        assert report_form.is_valid() == True
    
    def test_report_form4(self):
        report_form = ReportForm(data={
            'reported_message': None,
            'reason': 'tooshortreason',
            'confirmation': 'YES'
        })
        assert report_form.is_valid() == False
