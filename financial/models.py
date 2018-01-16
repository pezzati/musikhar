# -*- coding: utf-8 -*-

from django.db import models


class BusinessPackage(models.Model):
    name = models.CharField(max_length=64, default=u'بسته‌ی جدید', blank=True)

    days = models.IntegerField(default=0, blank=True)
    weeks = models.IntegerField(default=0, blank=True)
    months = models.IntegerField(default=0, blank=True)
    years = models.IntegerField(default=0, blank=True)
    total_days = models.IntegerField(default=0, help_text=u'نیازی به پر کردن این مقدار نیست', blank=True)

    price = models.IntegerField(default=0)

    active = models.BooleanField(default=True)

    def __str__(self):
        return '<{} - {}>'.format(self.total_days, self.price)

    def to_days(self):
        return self.total_days if self.total_days else self.days + self.weeks * 7 + self.months * 31 + self.months * 366

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_days = self.to_days()
        super(BusinessPackage, self).save(force_insert=force_insert,
                                          force_update=force_update,
                                          using=using,
                                          update_fields=update_fields)


class UserPaymentTransaction(models.Model):
    user = models.ForeignKey('loginapp.User')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
