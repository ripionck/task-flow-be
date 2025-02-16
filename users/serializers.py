from rest_framework import serializers
from .models import User


class SettingsSerializer(serializers.Serializer):
    """
    Serializer for user settings.
    """
    email_notifications = serializers.BooleanField()
    desktop_notifications = serializers.BooleanField()
    theme_mode = serializers.CharField()
    accent_color = serializers.CharField(allow_null=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    avatar = serializers.ImageField(allow_null=True, required=False)
    # Use the User instance as the source
    settings = SettingsSerializer(source='*', required=False)

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'email', 'role', 'avatar', 'settings',
            'email_notifications', 'desktop_notifications', 'theme_mode',
            'accent_color', 'last_login', 'date_joined', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }
        # Fields that cannot be updated
        read_only_fields = ('last_login', 'date_joined')

    def to_representation(self, instance):
        """
        Customize the response format.
        """
        representation = super().to_representation(instance)

        # Define settings-related fields
        settings_fields = ['email_notifications',
                           'desktop_notifications', 'theme_mode', 'accent_color']

        # Move settings-related fields under the 'settings' key
        representation['settings'] = {
            field: representation.pop(field)
            for field in settings_fields
            if field in representation  # Check if the field exists
        }

        return representation

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)  # Hash the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance, given the validated data.
        """
        password = validated_data.pop('password', None)

        # Update fields dynamically
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password if provided
        if password:
            instance.set_password(password)

        instance.save()
        return instance
