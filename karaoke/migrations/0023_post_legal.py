# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-02-04 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0022_auto_20190127_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='legal',
            field=models.BooleanField(default=True),
        ),
    ]
