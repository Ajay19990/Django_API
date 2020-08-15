from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.PhoneOTP)
admin.site.register(models.ServiceCategories)
admin.site.register(models.Service)
