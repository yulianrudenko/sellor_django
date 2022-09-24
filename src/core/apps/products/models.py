import uuid
import json

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    post_delete
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.apps.users.models import UserAccount
from core.utils import (
    get_fixtures_directory,
    create_or_update_fixture_signal,
    delete_fixture_signal
)


fixtures_directory = get_fixtures_directory()


class ActiveProductsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(purchased_by=None)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name=_('title'), max_length=40, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.PROTECT, default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(verbose_name=_('description'), max_length=300, blank=True)
    if settings.DEBUG:
        image = models.ImageField(
            verbose_name=_("image"),
            help_text=_("Upload an image"),
            upload_to="images/products",
            default="../static/images/blank.jpg"
        )
    else:
        image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload an image"),
        upload_to="images/products",
        default=None,
        null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)
    pub_date = models.DateTimeField(verbose_name=_('publication date'), auto_now_add=True, editable=False)
    purchased_by = models.ForeignKey(UserAccount, related_name='purchased_products', on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()
    active_products = ActiveProductsManager()

    class Meta:
        ordering = ['-pub_date']

    @property
    def get_image(self):
        if not settings.DEBUG and not self.image:
            return 'https://sellorbucket.s3.amazonaws.com/static/images/blank.jpg'
        return self.image.url

    @property
    def is_active(self):
        if self.purchased_by == None:
            return True
        return False

    @property
    def discount_percentage(self):
        discount_in_percent = 100 - (self.discount_price * 100 / self.price)
        return "%.1f" % discount_in_percent
    
    @property
    def current_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def __str__(self) -> str:
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.id])

    def save(self, *args, **kwargs) -> None:
        self.title: str = self.title.capitalize()
        if self.description:
            self.description: str = self.description.title()
        if self.discount_price:
            if self.discount_price >= self.price:
                raise ValueError(_('Discount price cannot be higher than regular.'))
        return super().save(*args, **kwargs)

@receiver(post_save, sender=Product)
def product_created_handler(sender, instance, created, *args, **kwargs):
    if instance.purchased_by != None:
        instance.wishlists.clear()


class Category(models.Model):
    name = models.CharField(verbose_name=_('category name'), max_length=50, unique=True)
    slug = models.SlugField(unique=True, help_text='no polish special chars allowed')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('products:category', args=[self.slug])


categories_fixture_file_dir = fixtures_directory + '/categories_fixture.json'

@receiver(post_save, sender=Category)
def category_created_handler(sender, instance, created, *args, **kwargs):
    create_or_update_fixture_signal(sender, instance, created, raw=kwargs.pop('raw'), \
        fixture_file_dir=categories_fixture_file_dir, fields=('name', 'slug', 'name_pl'), *args, **kwargs)

@receiver(post_delete, sender=Category)
def category_deleted_handler(sender, instance, *args, **kwargs):
    delete_fixture_signal(sender, instance, fixture_file_dir=categories_fixture_file_dir, *args, **kwargs)


class Tag(models.Model):
    name = models.CharField(verbose_name=_('tag name'), max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}'

tags_fixture_file_dir = fixtures_directory + '/tags_fixture.json'

@receiver(post_save, sender=Tag)
def tag_created_handler(sender, instance, created, *args, **kwargs):
    create_or_update_fixture_signal(sender, instance, created, raw=kwargs.pop('raw'), \
        fixture_file_dir=tags_fixture_file_dir, fields=('name',), *args, **kwargs)

@receiver(post_delete, sender=Tag)
def tag_deleted_handler(sender, instance, *args, **kwargs):
    delete_fixture_signal(sender, instance, fixture_file_dir=tags_fixture_file_dir, *args, **kwargs)
