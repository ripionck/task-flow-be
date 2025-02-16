from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'task', 'user', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_task(self, value):
        """
        Validate that the task belongs to a board owned by the authenticated user.
        """
        user = self.context['request'].user
        if value.board.created_by != user:
            raise serializers.ValidationError(
                "You do not have permission to add a comment to this task.")
        return value
