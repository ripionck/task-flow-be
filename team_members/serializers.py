from rest_framework import serializers
from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'user', 'board', 'role')
        read_only_fields = ('id',)
