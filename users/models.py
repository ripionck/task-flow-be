from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    username = models.CharField(_("username"), max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='user')
    avatar = models.ImageField(
        upload_to='users/avatars/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class UserSettings(models.Model):
    THEME_MODES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System')
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    desktop_notifications = models.BooleanField(default=True)
    theme_mode = models.CharField(
        max_length=20, choices=THEME_MODES, default='system')
    accent_color = models.CharField(max_length=7, default='#2563eb')
