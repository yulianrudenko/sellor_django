from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from . import models

@admin.register(models.Category)
class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(models.Product)
admin.site.register(models.Tag)
