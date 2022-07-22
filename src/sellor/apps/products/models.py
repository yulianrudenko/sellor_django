import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from django.conf import settings
from sellor.apps.orders.models import Order

CATEGORY_CHOICES = settings.CATEGORY_CHOICES
TAG_CHOICES = settings.TAG_CHOICES


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name=_('title'), max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(verbose_name=_('description'), max_length=300 ,null=True, blank=True) 
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload an image"),
        upload_to="images/products",
        default="../static/images/blank.jpg"
    )
    tags = models.ManyToManyField('Tag', blank=True)
    order = models.ForeignKey(Order, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    # @property
    # def rating(self):
    #     reviews = self.reviews.all()
    #     if reviews.count() == 0:
    #         return 0
    #     average_rating = sum([review.rating for review in reviews]) / reviews.count()
    #     return int(average_rating)
    
    @property
    def discount_percentage(self):
        discount_in_percent = 100 - (self.discount_price * 100 / self.price)
        return "%.1f" % discount_in_percent
    
    @property
    def current_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.id])

    def save(self, *args, **kwargs) -> None:
        self.title: str = self.title.capitalize()
        if self.description:
            self.description: str = self.description.title()
        if self.discount_price:
            if self.discount_price >= self.price:
                raise ValueError('Discount price cannot be higher than regular.')
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField(verbose_name=_('category name'), choices=CATEGORY_CHOICES, max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('products:category', args=[self.name])

    def __str__(self) -> str:
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(verbose_name=_('tag name'), choices=TAG_CHOICES, max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class CouponCode(models.Model):
    code = models.CharField(verbose_name=_('coupon code'), max_length=16, unique=True)
    reduce_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.code}'


# class Review(models.Model):
#     product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.SET_NULL, null=True)
#     text = models.CharField(verbose_name=_('review text content'), max_length=200, null=True, blank=True)
#     rating = models.IntegerField(
#         default=1,
#         validators=[MaxValueValidator(10), MinValueValidator(0)]
#     )
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-date_created']

#     def __str__(self) -> str:
#         return f'{self.author} for {self.product.title}'