from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


MALE = "M"
FEMALE = "F"
UNKNOWN = "X"
GENDER_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (UNKNOWN, "Other"),
]


class Visitor(models.Model):
    ip = models.CharField(max_length=55, unique=True, null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.ip)


class City(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    
    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


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
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('location', City.objects.first())
        if other_fields['is_superuser'] is not True:
            raise ValueError(_('Superuser\'s "is_superuser" must be set to True'))
        other_fields.setdefault('is_staff', True)
        if other_fields['is_staff'] is not True:
            raise ValueError(_('Superuser\'s "is_staff" must be set to True'))
        return self.create_user(email, password, first_name, last_name, is_activated=True, **other_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("email address"), unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100)
    location = models.ForeignKey(City, verbose_name=_("location(city)"), max_length=35, on_delete=models.CASCADE, null=False, blank=False)
    phone = models.CharField(verbose_name=_("phone"), max_length=20, unique=True, null=True, blank=True)
    gender = models.CharField(verbose_name=_("gender"), choices=GENDER_CHOICES, default="X", max_length=1)
    is_staff = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    if settings.DEBUG:
        image = models.ImageField(
            verbose_name=_("image"),
            help_text=_("Upload an avatar"),
            upload_to="images/profile_pics",
            default="../static/images/blank.jpg")
    else:
        image = models.ImageField(
            verbose_name=_("image"),
            help_text=_("Upload an avatar"),
            upload_to="images/profile_pics",
            default=None,
            null=True, blank=True)
    wishlist = models.ManyToManyField('products.Product', related_name='wishlists', blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ['-date_created']

    @property
    def get_image(self):
        if not settings.DEBUG and not self.image:
            return 'https://sellorbucket.s3.amazonaws.com/static/images/blank.jpg'
        return self.image.url

    @property
    def fullname(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def active_products(self):
        return self.products.filter(purchased_by=None)

    @property
    def sold_count(self) -> int:
        return self.products.exclude(purchased_by=None).count()
    
    @property
    def sold_total(self) -> int:
        total = 0
        for product in self.products.exclude(purchased_by=None):
            total += product.current_price
        return total
    
    @property
    def purchased_count(self) -> int:
        return self.purchased_products.count()
    
    @property
    def purchased_total(self) -> int:
        total = 0
        for product in self.purchased_products.all():
            total += product.current_price
        return total
    
    @property
    def chats_count(self) -> int:
        return str(self.customer_chats.count() + self.seller_chats.count())
    
    @property
    def unseen_messages_count(self) -> int:
        count = sum(chat.sellers_unseen_messages_count for chat in self.seller_chats.all())
        count += sum(chat.customers_unseen_messages_count for chat in self.customer_chats.all())
        return count

    def __str__(self) -> str:
        return f"{self.email}"

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.lower().capitalize()
        return super(UserAccount, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile', args=[self.id])

    def is_blocked_by(self, user):
        if self in user.blacklist.blocked_users.all():
            return True
        return False
    
    def has_blocked(self, user):
        if user in self.blacklist.blocked_users.all():
            return True
        return False
    

@receiver(post_save, sender=UserAccount)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Blacklist.objects.create(owner=instance)


class ReportUser(models.Model):
    '''
    Hint: user could be reported for message
    or other reasons (with explanation from author, what caused the report)
    '''
    report_author = models.ForeignKey(UserAccount, related_name='reports_author', on_delete=models.CASCADE)
    user_reported = models.ForeignKey(UserAccount, related_name='reports_subject', on_delete=models.CASCADE)
    reported_message = models.OneToOneField('chats.Message', related_name='report', unique=True, null=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'User Report'
        verbose_name_plural = 'User Reports'

    def __str__(self) -> str:
        return f"{self.user_reported}"


class Blacklist(models.Model):
    owner = models.OneToOneField(UserAccount, primary_key=True, related_name='blacklist', on_delete=models.CASCADE)
    blocked_users = models.ManyToManyField(UserAccount, related_name='blocked_by_others', blank=True)

    def __str__(self) -> str:
        return f'{self.owner}'
    

class Feedback(models.Model):
    user = models.ForeignKey(UserAccount, related_name='feedbacks', on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=250, blank=False, null=False)
    upvoted_by = models.ManyToManyField(UserAccount, related_name='upvoted_posts', blank=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return f'{self.text}'
