# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-29 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mediafiles', '0001_initial'),
        ('karaoke', '0005_auto_20171119_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='karaoke',
            name='full_file',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_full_karaoke', to='mediafiles.MediaFile'),
        ),
    ]
