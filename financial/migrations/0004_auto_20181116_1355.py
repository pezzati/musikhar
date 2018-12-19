# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-16 10:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial', '0003_userpaymenttransaction_transaction_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coins', models.IntegerField(default=0)),
                ('amount', models.IntegerField(blank=True, help_text='Amount of currency paid for this coins', null=True)),
                ('applied', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='businesspackage',
            name='coins',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='businesspackage',
            name='package_type',
            field=models.CharField(choices=[('time', 'time package'), ('coin', 'coin package')], default='time', max_length=8),
        ),
        migrations.AddField(
            model_name='businesspackage',
            name='platform_type',
            field=models.CharField(choices=[('ios', 'iOS'), ('android', 'Android')], default='ios', max_length=10),
        ),
    ]