from django.forms import forms

from .models import UserAccount


def password_validator(password):
    if ' ' in password:
        raise forms.ValidationError("Password must <em>not</em> contain spaces.")
    if len(password) < 6 or len(password) > 30:
        raise forms.ValidationError("The password must be 6-30 characters")
    return password
