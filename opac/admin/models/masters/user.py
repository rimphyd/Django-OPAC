from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from opac.models.masters.user import User


admin.site.register(User, UserAdmin)
