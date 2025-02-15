from rest_framework import serializers
from .models import Task
from boards.models import Board
from columns.models import Column


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'board', 'column', 'title', 'description', 'status', 'priority',
            'due_date', 'tags', 'assignees', 'created_by', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def get_created_by(self, obj):
        """
        Return the full name of the user who created the task.
        """
        return obj.created_by.full_name

    def validate_board(self, value):
        """
        Validate that the board belongs to the authenticated user.
        """
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError(
                "You do not have permission to add a task to this board.")
        return value

    def validate_column(self, value):
        """
        Validate that the column belongs to the authenticated user's board.
        """
        user = self.context['request'].user
        if value.board.created_by != user:
            raise serializers.ValidationError(
                "You do not have permission to add a task to this column.")
        return value
