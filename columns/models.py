from django.db import models
import uuid
from boards.models import Board
from users.models import User


class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, blank=True, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_columns', blank=True, null=True)

    def __str__(self):
        return self.name
