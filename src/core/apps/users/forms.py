import requests
from django import forms
from django.conf import settings
from django.contrib.auth.hashers import check_password

from .models import City, UserAccount, ReportUser, GENDER_CHOICES
from .validators import password_validator


class ValidateFirstNameSecondNamePhoneLocation():
    def clean_first_name(self):
        first_name: str = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('First name must contain only letters')
        return first_name
    
    def clean_last_name(self):
        last_name: str = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must contain only letters')
        return last_name
    
    def clean_phone(self):
        phone: str = self.cleaned_data['phone']
        if phone:
            if len(phone) < 6:
                raise forms.ValidationError('Please enter real number')
            for char in phone:
                if not char.isdigit():
                    raise forms.ValidationError('Please enter real number')
        return phone


class RegistrationForm(ValidateFirstNameSecondNamePhoneLocation, forms.ModelForm):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=True, initial='X')
    password1 = forms.CharField(label='Password*', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password*', widget=forms.PasswordInput, required=True)
    location = forms.ModelChoiceField(queryset=City.objects.all())
    image = forms.FileField(label='Profile picture', widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['phone'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['gender'].widget.attrs['class'] ='form-check-input mx-2'
        self.fields['location'].widget.attrs['class'] ='form-select'
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].widget.attrs["class"] = 'form-control form-control-lg'
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat password"
        self.fields["password2"].widget.attrs["class"] = 'form-control form-control-lg'
        self.fields['image'].widget.attrs['id'] ='profileImageInput'
        self.fields['image'].widget.attrs['accept'] ='.jpg,.jpeg,.png'
        self.fields['image'].widget.attrs['onchange'] ='readURL(this); validateFileType()'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not settings.DEBUG:
            api_key = settings.EMAIL_VALIDATION_API_KEY
            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params = {'email': email}, headers = {'Authorization': "Bearer " + api_key })
        else:
            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params = {'email': email})
        status = response.json()['status']
        if status != "valid":
            raise forms.ValidationError("Please enter an existing email.")
        return email

    def clean_password2(self):
        password = self.cleaned_data["password1"]
        if password != self.cleaned_data["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters length.")
        return self.cleaned_data["password2"]


    class Meta:
        model = UserAccount
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'gender',
            'location',
            'image'
        )


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields["password"].widget.attrs["class"] = 'form-control form-control-lg'

    def clean_email(self):
        email = self.cleaned_data['email']
        if not UserAccount.objects.filter(email=email).exists():
            raise forms.ValidationError("User with given email doesn't exist.")
        return self.cleaned_data['email']


class UserEditForm(forms.ModelForm, ValidateFirstNameSecondNamePhoneLocation):
    location = forms.ModelChoiceField(queryset=City.objects.all())
    image = forms.FileField(label='Profile picture', widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['phone'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['location'].widget.attrs['class'] ='form-select'
        self.fields['image'].widget.attrs['id'] ='profileImageInput'
        self.fields['image'].widget.attrs['accept'] ='.jpg,.jpeg,.png'
        self.fields['image'].widget.attrs['onchange'] ='readURL(this); validateFileType()'

    class Meta:
        model = UserAccount
        fields = (
            'image',
            'first_name',
            'last_name',
            'phone',
            'location',
        )


class UserChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[password_validator])
    verify_new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['current_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password'].widget.attrs['class'] = 'form-control'
        self.fields['verify_new_password'].widget.attrs['class'] = 'form-control'
    
    def clean_current_password(self):
        user = self.data['user']
        password = self.cleaned_data['current_password']
        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')
        return password
    
    def clean_verify_new_password(self):
        if not self.errors:
            password1 = self.cleaned_data['new_password']
            password2 = self.cleaned_data['verify_new_password']
            if password1 == password2:
                return password2
        raise forms.ValidationError("Passwords do not match.")


class ReportForm(forms.ModelForm):
    reported_message = forms.CharField(widget=forms.HiddenInput(), required=False)
    reason = forms.CharField(widget=forms.Textarea, required=False, max_length=200)
    confirmation = forms.CharField(required=True)

    class Meta:
        model = ReportUser
        fields = (
            'reported_message',
            'reason',
        )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['reported_message'].widget.attrs['readonly'] = True
        self.fields['reason'].widget.attrs['class'] = 'form-control'
        self.fields['reason'].widget.attrs['placeholder'] = 'Explain what happend (200 characters max)'
        self.fields['confirmation'].widget.attrs['class'] = 'form-control'
        self.fields['confirmation'].widget.attrs['id'] = 'confirmation'
        self.fields['confirmation'].widget.attrs['placeholder'] = 'Type YES'
    
    def clean(self):
        if self.cleaned_data.get('confirmation') != 'YES':
            self.add_error('confirmation', 'Please type YES to confirm the report!')
        if not self.cleaned_data.get('reported_message'):
            reason = self.cleaned_data.get('reason')
            if len(reason) < 15:
                self.add_error('reason', 'Provide reason with at least 15 characters please!')
        return super().clean()