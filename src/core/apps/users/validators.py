from django.forms import forms
from django.utils.translation import gettext_lazy as _

from .models import UserAccount


def password_validator(password):
    if ' ' in password:
        raise forms.ValidationError(_("Password must <em>not</em> contain spaces."))
    if len(password) < 6 or len(password) > 30:
        raise forms.ValidationError(_("The password must be 6-30 characters"))
    return password
