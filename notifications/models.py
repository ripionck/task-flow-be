import uuid
from django.db import models
from users.models import User


class Notification(models.Model):
    TYPES = [
        ('assignment', 'Assignment'),
        ('deadline', 'Deadline'),
        ('comment', 'Comment'),
        ('mention', 'Mention')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPES)
    content = models.TextField()
    related_item_id = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
