from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role'
    )
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['bio', 'role']}),)
    add_fieldsets = UserAdmin.add_fieldsets \
        + ((None, {"fields": ['bio', 'role']}),)
