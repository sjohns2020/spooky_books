from django.contrib import admin

# Register your models here for Admin Portal.

from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
