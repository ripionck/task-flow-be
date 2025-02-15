from django.db import models
import uuid
from users.models import User
from boards.models import Board


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

    class Meta:
        unique_together = ('user', 'board')

    def __str__(self):
        return f"{self.user.username} - {self.board.title}"
