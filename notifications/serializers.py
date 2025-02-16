from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'type', 'content',
                  'related_item_id', 'is_read', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def validate_user(self, value):
        """
        Validate that the user is the authenticated user.
        """
        user = self.context['request'].user
        if value != user:
            raise serializers.ValidationError(
                "You do not have permission to create a notification for this user.")
        return value
