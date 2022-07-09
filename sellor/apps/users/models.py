from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sellor.apps.products.models import Product


MALE = "M"
FEMALE = "F"
UNKNOWN = "X"
GENDER_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (UNKNOWN, "Unknown"),
]


class UserAccountManager(BaseUserManager):
    def create_user(self, email: str, password: str, first_name: str, last_name: str, **other_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email=email)
        if not type(first_name) is str or not type(last_name) is str:
            raise ValueError(_('Either first and last name must be valid.'))
        if not first_name.isalpha() or not last_name.isalpha():
            raise ValueError(_('Either first and last name must be valid.'))
        if len(password) < 6:
            raise ValueError(_('Password must be at least 6 chars length.'))
        user = self.create(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str, first_name: str, last_name: str, **other_fields):
        other_fields.setdefault('is_superuser', True)
        if other_fields['is_superuser'] is not True:
            raise ValueError(_('Superuser\'s "is_superuser" must be set to True'))
        other_fields.setdefault('is_staff', True)
        if other_fields['is_staff'] is not True:
            raise ValueError(_('Superuser\'s "is_staff" must be set to True'))
        return self.create_user(email, password, first_name, last_name, **other_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100)
    location = models.CharField(verbose_name=_("location(country and/or city)"), max_length=255, null=True, blank=True)
    phone = models.CharField(verbose_name=_("phone"), max_length=20, unique=True, null=True, blank=True)
    gender = models.CharField(verbose_name=_("gender"), choices=GENDER_CHOICES, default="X", max_length=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload an avatar"),
        upload_to="images/profile_pics",
        default="images/blank.jpg"
    )
    wishlist = models.ManyToManyField(Product)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.lower().capitalize()
        if self.location:
            self.location = self.location.lower().title()
        return super(UserAccount, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.id])

    def __str__(self) -> str:
        return f"{self.email}"
