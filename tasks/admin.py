from django.contrib import admin
from .models import Task, Comment


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'status', 'priority')
    list_filter = ('status', 'priority')
    inlines = [CommentInline]


admin.site.register(Comment)
