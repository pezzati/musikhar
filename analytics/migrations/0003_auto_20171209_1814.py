# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-09 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20171111_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='content_type',
            field=models.CharField(choices=[('multi', 'Multiple objects'), ('single', 'Single object'), ('redirect', 'redirect to Web')], default='single', max_length=10),
        ),
    ]
