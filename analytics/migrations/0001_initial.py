# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('karaoke', 'Karaoke')], default='karaoke', max_length=20)),
            ],
        ),
    ]
