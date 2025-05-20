from django.contrib import admin
from .models import User

# Optionally, customize the User admin display


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'user_type', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'user_type')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff')

admin.site.register(User, UserAdmin)
