
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'content', 'is_read', 'created_at')
    list_filter = ('user', 'type', 'is_read')
    search_fields = ('content',)
    readonly_fields = ('created_at',)
