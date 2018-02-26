# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-21 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import mediafiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('mediafiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsyncTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(default='new_async_task', max_length=128)),
                ('type', models.CharField(choices=[('karaokes', 'Upload Karaokes')], default='karaokes', max_length=128)),
                ('file', models.FileField(blank=True, null=True, upload_to=mediafiles.models.get_task_path)),
                ('error_file', models.FileField(blank=True, null=True, upload_to='')),
                ('state', models.CharField(choices=[('added', 'Task Added'), ('processing', 'In Progress'), ('done', 'Done'), ('error', 'error occurred, check error file')], default='added', max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='type',
            field=models.CharField(choices=[('song', 'song file'), ('poem', 'poem file'), ('video', 'video file'), (('cover',), 'cover photo file'), ('karaoke', 'Karaoke File')], default='song', max_length=20),
        ),
    ]