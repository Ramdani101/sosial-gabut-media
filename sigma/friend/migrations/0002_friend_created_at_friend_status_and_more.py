# Generated by Django 5.2.1 on 2025-05-29 04:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='friend',
            name='accepted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friend_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_received', to='friend.user'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_sent', to='friend.user'),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('user', 'friend_username')},
        ),
    ]
