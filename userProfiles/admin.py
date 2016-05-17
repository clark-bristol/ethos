"""
Adds new stuff at the bottom of the admin page of the user's profile
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from userProfiles.models import StandardUser

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class StandardUserInline(admin.StackedInline):
    model = StandardUser
    can_delete = False
    verbose_name_plural = 'Standard User'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StandardUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)