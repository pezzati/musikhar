# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-06 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0017_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='order_by',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
