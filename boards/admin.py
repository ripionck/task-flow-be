from django.contrib import admin
from .models import Board, Column, TeamMember


class ColumnInline(admin.TabularInline):
    model = Column


class TeamMemberInline(admin.TabularInline):
    model = TeamMember


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ColumnInline, TeamMemberInline]


admin.site.register(Column)
admin.site.register(TeamMember)
