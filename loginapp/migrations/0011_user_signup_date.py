# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-08 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0010_user_is_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
