from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'type', 'content',
                  'related_item_id', 'is_read', 'created_at')
        read_only_fields = ('id', 'user', 'type', 'content',
                            'related_item_id', 'created_at')
