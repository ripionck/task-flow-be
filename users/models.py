from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    ROLES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member')
    ]

    THEMES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('system', 'System')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(
        _('full name'), max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    avatar = models.URLField(blank=True, null=True)
    emailNotifications = models.BooleanField(default=True)
    desktopNotifications = models.BooleanField(default=True)
    themeMode = models.CharField(max_length=20, default='system')
    accentColor = models.CharField(max_length=7, blank=True, null=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.first_name + " " + \
                self.last_name if self.first_name and self.last_name else None
        super().save(*args, **kwargs)
