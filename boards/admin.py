from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description', 'tags')
    list_filter = ('created_by', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'cover_image', 'tags')}),
        ('Creator Information', {'fields': ('created_by',)}),
        ('Date Information', {'fields': ('created_at', 'updated_at')}),
    )
