# Generated by Django 5.1.6 on 2025-02-15 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='accentColor',
            new_name='accent_color',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='desktopNotifications',
            new_name='desktop_notifications',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='emailNotifications',
            new_name='email_notifications',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='themeMode',
            new_name='theme_mode',
        ),
    ]
