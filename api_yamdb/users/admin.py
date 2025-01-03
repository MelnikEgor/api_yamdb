from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role',
        'confirmation_code'
    )

# UserAdmin.fieldsets += (
#     ('Extra Fields', {'fields': ('bio', 'role',)}),
# )

# admin.site.register(MyUser, UserAdmin)
