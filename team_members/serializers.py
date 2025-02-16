from rest_framework import serializers
from .models import TeamMember
from boards.models import Board


class TeamMemberSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    class Meta:
        model = TeamMember
        fields = ('id', 'user', 'board', 'role')
        read_only_fields = ('id',)

    def validate_board(self, value):
        """
        Validate that the board belongs to the authenticated user.
        """
        user = self.context['request'].user
        if value.created_by != user:
            raise serializers.ValidationError(
                "You do not have permission to add a team member to this board.")
        return value
