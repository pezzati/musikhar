# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-07 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0019_auto_20180907_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
