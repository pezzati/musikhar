# -*- coding: utf-8 -*-
import uuid

from datetime import timedelta, datetime

from django.db import models
from django.db.transaction import atomic


class BusinessPackage(models.Model):
    name = models.CharField(max_length=64, default=u'بسته‌ی جدید', blank=True)
    icon = models.FileField(upload_to='default_icons', null=True, blank=True)
    serial_number = models.CharField(max_length=16, unique=True, db_index=True, blank=True, null=True,
                                     help_text=u'این مقدار بایستی منحصر بفرد باشد، در صورت خالی گذاشتن مقدار دهی خواهد شد')

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

    def apply_package(self, user):
        tran = UserPaymentTransaction.objects.create(user=user, amount=self.price, days=self.total_days)
        tran.apply()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_days = self.to_days()
        if not self.serial_number:
            self.serial_number = str(uuid.uuid4().int)[:12]
        super(BusinessPackage, self).save(force_insert=force_insert,
                                          force_update=force_update,
                                          using=using,
                                          update_fields=update_fields)

    @classmethod
    def get_package(cls, code):
        try:
            return cls.objects.get(serial_number=code, active=True)
        except cls.DoesNotExist:
            return None


class UserPaymentTransaction(models.Model):
    user = models.ForeignKey('loginapp.User')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    applied = models.BooleanField(default=False)

    def __str__(self):
        return '< {} - {} - {} >'.format(self.user.username, self.amount, self.days)

    @atomic
    def apply(self):
        if self.user.is_premium:
            self.user.premium_time = self.user.premium_time + timedelta(days=self.days)
            self.user.save(update_fields=['premium_time'])
            self.applied = True
            self.save()
        else:
            self.user.premium_time = datetime.now().date() + timedelta(days=self.days)
            self.user.is_premium = True
            self.user.save(update_fields=['is_premium', 'premium_time'])
            self.applied = True
            self.save()
        return


class BankTransaction(models.Model):
    CREATED = 'created'
    SENT_TO_BANK = 'in_progress'
    RETURNED = 'returned'
    FAILED_BANK = 'failed'
    SUCCESS = 'success'
    CHECK_FAILED = 'verify_failed'

    STATE_TYPE_CHOICES = (
        (CREATED, u'ساخته شده'),
        (SENT_TO_BANK, u'ارجاع به بانک'),
        (RETURNED, u'بازگشت از بانک'),
        (FAILED_BANK, u'خطا در بانک'),
        (SUCCESS, u'اتمام'),
        (CHECK_FAILED, u'خطا در تایید')
    )

    creation_date = models.DateTimeField(auto_now=True)
    refId = models.CharField(max_length=100, null=True, blank=True)
    authority = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey('loginapp.User')
    package = models.ForeignKey(BusinessPackage, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()
    state = models.CharField(max_length=20, choices=STATE_TYPE_CHOICES, default=CREATED)
    bank_status = models.CharField(max_length=4, null=True, blank=True)
    package_applied = models.BooleanField(default=False)

    @atomic
    def apply_package(self):
        if not self.package_applied:
            self.package.apply_package(user=self.user)
            self.package_applied = True
            self.save()
