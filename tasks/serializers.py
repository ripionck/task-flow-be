from rest_framework import serializers
from users.models import User
from .models import Task, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'task')


class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    assignees = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_by', 'board', 'column')

    def validate_assignees(self, value):
        board = self.context['board']
        team_members = board.team_members.values_list('user', flat=True)
        for user in value:
            if user.id not in team_members:
                raise serializers.ValidationError(
                    "Assignee must be a team member"
                )
        return value
