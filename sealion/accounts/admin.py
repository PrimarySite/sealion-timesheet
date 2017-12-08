# -*- coding: utf-8 -*-
"""Admin for User account."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Local
from .models import User, Organization, Repository, Event, Membership


class AuthUserAdmin(UserAdmin):
    """Customize the user admin."""

    readonly_fields = ('uid', )
    list_display = (
        'username',
        'email',
        'uid',
        'first_name',
        'last_name',
        'is_staff')

    fieldsets = UserAdmin.fieldsets + ((
        'Extra', {'fields': ('uid', )},
    ), )


admin.site.register(User, AuthUserAdmin)
admin.site.register(Membership)
admin.site.register(Organization)
admin.site.register(Repository)
admin.site.register(Event)
