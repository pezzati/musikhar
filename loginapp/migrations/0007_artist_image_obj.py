# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-20 21:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mediafiles', '0005_auto_20180622_1917'),
        ('loginapp', '0006_auto_20180616_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mediafiles.MediaFile'),
        ),
    ]
