# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-23 07:13
from __future__ import unicode_literals

from django.db import migrations, models
import loginapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=loginapp.models.get_avatar_path),
        ),
    ]
