import uuid
from django.db import models
from columns.models import Column
from users.models import User
from boards.models import Board


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
        Column(), on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='todo')
    priority = models.CharField(
        max_length=20, choices=PRIORITIES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list)
    assignees = models.ManyToManyField(
        User, related_name='assigned_tasks', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
