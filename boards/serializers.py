from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    cover_image = serializers.URLField(allow_null=True, required=False)
    created_by = serializers.SerializerMethodField()
    tags = serializers.CharField(allow_blank=True,  required=False)

    class Meta:
        model = Board
        fields = (
            'id', 'title', 'description', 'cover_image', 'tags',
            'created_by', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'created_by', 'created_at', 'updated_at'
        )

    def get_created_by(self, obj):
        """
        Return the full name of the user who created the board.
        """
        return obj.created_by.full_name

    def to_internal_value(self, data):
        """
        Convert tags from a comma-separated string to a list before saving to the database.
        """
        if 'tags' in data and isinstance(data['tags'], str):
            data['tags'] = data['tags'].strip()
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Convert tags from a comma-separated string to a list in the API response.
        """
        representation = super().to_representation(instance)
        if 'tags' in representation and isinstance(representation['tags'], str):
            representation['tags'] = representation['tags'].split(
                ',') if representation['tags'] else []
        return representation

    def create(self, validated_data):
        """
        Create and return a new Board instance, given the validated data.
        """
        # Set the created_by field to the authenticated user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
