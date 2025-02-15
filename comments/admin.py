from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user', 'content', 'created_at')
    list_filter = ('task', 'user', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('id', 'created_at', 'updated_at')
