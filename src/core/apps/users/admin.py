from django.contrib import admin

from . import models


admin.site.register(models.Visitor)
admin.site.register(models.City)
admin.site.register(models.UserAccount)
admin.site.register(models.ReportUser)
admin.site.register(models.Blacklist)
admin.site.register(models.Feedback)
