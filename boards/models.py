import uuid
from django.db import models
from users.models import User


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_image = models.URLField(blank=True)
    tags = models.JSONField(default=list)  # Use ArrayField if using PostgreSQL
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)


class TeamMember(models.Model):
    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='team_memberships')
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='team_members')
    role = models.CharField(max_length=20, choices=ROLES, default='member')
