from django.db import models
import uuid
from boards.models import Board


class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name
