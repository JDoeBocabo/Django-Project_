from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

from . models import *


admin.site.unregister(Group)

admin.site.register(Profile)
admin.site.register(Blog)
