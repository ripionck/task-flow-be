from rest_framework import serializers
from .models import Column
from boards.models import Board


class ColumnSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Column
        fields = ('id', 'board', 'name', 'color', 'creator')
        read_only_fields = ('id', 'creator')

    def get_creator(self, obj):
        """
        Return the full name of the user who created the column.
        """
        return obj.creator.full_name

    def validate_board(self, value):
        """
        Validate that the board belongs to the authenticated user.
        """
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError(
                "You do not have permission to add a column to this board.")
        return value
