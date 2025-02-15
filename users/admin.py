from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'user_type', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'full_name', 'avatar')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active')}),
    )


admin.site.register(User, CustomUserAdmin)
