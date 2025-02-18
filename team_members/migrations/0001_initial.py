# Generated by Django 5.1.6 on 2025-02-15 19:11

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0003_remove_teammember_board_remove_teammember_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('member', 'Member')], default='member', max_length=20)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_members', to='boards.board')),
            ],
        ),
    ]
