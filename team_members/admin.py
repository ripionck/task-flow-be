
from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'board', 'role')
    list_filter = ('role', 'board')
    search_fields = ('user__username', 'board__title')
    readonly_fields = ('id',)

    fieldsets = (
        (None, {'fields': ('user', 'board', 'role')}),
    )
