from rest_framework import serializers
from .models import Board, Column, TeamMember


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'
        read_only_fields = ('board',)


class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = TeamMember
        fields = '__all__'
        read_only_fields = ('board',)


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('created_by',)
