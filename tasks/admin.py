from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'column', 'status',
                    'priority', 'due_date', 'created_by', 'created_at')
    list_filter = ('board', 'column', 'status', 'priority', 'created_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    filter_horizontal = ('assignees',)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'board', 'column')}),
        ('Status & Priority', {'fields': ('status', 'priority', 'due_date')}),
        ('Assignees & Tags', {'fields': ('assignees', 'tags')}),
    )
