from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

# Inline display for UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend the existing User admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Display UserProfile fields inline

    def date_of_birth(self, obj):
        return obj.userprofile.date_of_birth
    date_of_birth.short_description = 'DOB'

    # Method to display UserProfile 'phone_number' in the user list
    def phone_number(self, obj):
        return obj.userprofile.phone_number
    phone_number.short_description = 'Phone Number'

    # Customize list_display to show User and UserProfile fields
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'date_of_birth', 'phone_number')
    list_select_related = ('userprofile',)  # Optimize query

# Unregister the existing User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

