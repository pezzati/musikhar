# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20170928_1830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ['-time']},
        ),
    ]