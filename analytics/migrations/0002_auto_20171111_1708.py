# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-11 13:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0001_initial'),
        ('karaoke', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfilehistory',
            name='owner_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_requested_files_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userfilehistory',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='download_history', to='karaoke.Post'),
        ),
        migrations.AddField(
            model_name='userfilehistory',
            name='requested_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_files_history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tagpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='karaoke.Post'),
        ),
        migrations.AddField(
            model_name='tagpost',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.Tag'),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='karaoke.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favorite',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='karaoke.Post'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='karaoke.Post'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='triggered_event', to=settings.AUTH_USER_MODEL),
        ),
    ]