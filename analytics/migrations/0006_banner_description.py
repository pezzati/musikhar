# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-04 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_useraction_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
