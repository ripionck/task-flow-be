from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'cover_image', 'tags', 'columns',
                  'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'columns', 'created_by',
                            'created_at', 'updated_at')
