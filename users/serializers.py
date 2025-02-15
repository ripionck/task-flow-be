from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, blank=True)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'role', 'avatar', 'email_notifications',
                  'desktop_notifications', 'theme_mode', 'accent_color')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
