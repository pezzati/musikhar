# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-22 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0008_remove_post_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='text',
            field=models.TextField(default='', max_length=3000),
        ),
    ]