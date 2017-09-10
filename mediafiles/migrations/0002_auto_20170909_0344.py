# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-08 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediafiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='type',
            field=models.CharField(choices=[('song', 'karaoke file'), ('poem', 'poem file'), ('video', 'video file'), ('cover', 'cover photo file')], default='song', max_length=20),
        ),
    ]