# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-06 21:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('refId', models.CharField(blank=True, max_length=100, null=True)),
                ('authority', models.CharField(blank=True, max_length=40, null=True)),
                ('amount', models.IntegerField()),
                ('state', models.CharField(choices=[('created', 'ساخته شده'), ('in_progress', 'ارجاع به بانک'), ('returned', 'بازگشت از بانک'), ('failed', 'خطا در بانک'), ('success', 'اتمام'), ('verify_failed', 'خطا در تایید')], default='created', max_length=20)),
                ('bank_status', models.CharField(blank=True, max_length=4, null=True)),
                ('package_applied', models.BooleanField(default=False)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financial.BusinessPackage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
