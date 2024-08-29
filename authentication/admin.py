from django.contrib import admin
from django.contrib import admin
from .models import UserProfile


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    # Display additional fields in the admin panel
    list_display = ('phone_number', 'date_of_birth')

admin.site.register(UserProfile, UserProfileAdmin)

