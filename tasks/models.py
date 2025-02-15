import uuid
from django.db import models
from users.models import User
from boards.models import Board, Column


class Task(models.Model):
    STATUSES = [
        ('todo', 'Todo'),
        ('inProgress', 'In Progress'),
        ('done', 'Done')
    ]

    PRIORITIES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks')
    column = models.ForeignKey(
        Column, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='todo')
    priority = models.CharField(
        max_length=20, choices=PRIORITIES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list)  # Use ArrayField if using PostgreSQL
    assignees = models.ManyToManyField(
        User, related_name='assigned_tasks', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
