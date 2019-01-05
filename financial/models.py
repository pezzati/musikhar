# -*- coding: utf-8 -*-
import uuid

from datetime import timedelta, datetime
from django.utils import timezone

from django.db import models
from django.db.transaction import atomic

from financial.services import BazzarClient


class BusinessPackage(models.Model):
    TIME_PACKAGE = 'time'
    COIN_PACKAGE = 'coin'

    PACKAGE_TYPES = (
        (TIME_PACKAGE, 'time package'),
        (COIN_PACKAGE, 'coin package')
    )

    ios = 'ios'
    android = 'android'
    PlatformChoices = (
        (ios, 'iOS'),
        (android, 'Android')
    )

    name = models.CharField(max_length=64, default=u'بسته‌ی جدید', blank=True)
    icon = models.FileField(upload_to='default_icons', null=True, blank=True)
    package_type = models.CharField(max_length=8, choices=PACKAGE_TYPES, default=TIME_PACKAGE)
    platform_type = models.CharField(max_length=10, choices=PlatformChoices, default=ios)
    serial_number = models.CharField(max_length=32, unique=True, db_index=True, blank=True, null=True,
                                     help_text=u'این مقدار بایستی منحصر بفرد باشد، در صورت خالی گذاشتن مقدار دهی خواهد شد')

    days = models.IntegerField(default=0, blank=True)
    weeks = models.IntegerField(default=0, blank=True)
    months = models.IntegerField(default=0, blank=True)
    years = models.IntegerField(default=0, blank=True)
    total_days = models.IntegerField(default=0, help_text=u'نیازی به پر کردن این مقدار نیست', blank=True)

    coins = models.IntegerField(default=0, blank=True)

    price = models.IntegerField(default=0)

    active = models.BooleanField(default=True)

    def __str__(self):
        return '<{} - {}>'.format(self.total_days, self.price)

    def to_days(self):
        return self.total_days if self.total_days else self.days + self.weeks * 7 + self.months * 31 + self.years * 366

    def apply_package(self, user):
        if self.package_type == BusinessPackage.TIME_PACKAGE:
            tran = UserPaymentTransaction.objects.create(user=user, amount=self.price, days=self.total_days)
        else:
            tran = CoinTransaction.objects.create(user=user, amount=self.price, coins=self.coins)
        tran.apply()
        return tran

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.package_type == BusinessPackage.TIME_PACKAGE:
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
    transaction_info = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return '< {} - {} - {} >'.format(self.user.username, self.amount, self.days)

    @atomic
    def apply(self):
        if self.applied:
            return
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


class BazzarTransaction(models.Model):
    CREATED = 'created'
    SENT_TO_APP = 'in_progress'
    RETURNED = 'returned'
    SUCCESS = 'success'
    CHECK_FAILED = 'verify_failed'
    STATE_TYPE_CHOICES = (
        (CREATED, u'ساخته شده'),
        (SENT_TO_APP, u'به اپ ارسال شده'),
        (RETURNED, u'بازگشت از اپ'),
        (SUCCESS, u'اتمام'),
        (CHECK_FAILED, u'خطا در تایید')
    )

    user = models.ForeignKey('loginapp.User')
    package = models.ForeignKey(BusinessPackage, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_TYPE_CHOICES, default=CREATED)
    serial_number = models.CharField(max_length=24)
    ref_id = models.CharField(max_length=48, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(null=True, blank=True)
    package_applied = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.serial_number:
            self.serial_number = str(uuid.uuid4().int)[:16]
        self.last_update_date = timezone.now()
        super(BazzarTransaction, self).save(force_insert=force_insert,
                                            force_update=force_update,
                                            using=using,
                                            update_fields=update_fields)

    def is_valid(self):
        if self.package_applied:
            return True
        self.state = BazzarTransaction.RETURNED
        self.save(update_fields=['state'])

        bazzar_api = BazzarClient()
        is_valid, time = bazzar_api.check_purchase(purchase_id=self.ref_id,
                                                   product_id=self.package.serial_number)
        if is_valid:
            # self.last_update_date = time
            self.state = BazzarTransaction.SUCCESS
            self.save(update_fields=['state'])
            return True

        self.state = BazzarTransaction.CHECK_FAILED
        self.save(update_fields=['state'])
        return False

    @atomic
    def apply_package(self):
        if not self.package_applied:
            coin_tran = self.package.apply_package(user=self.user)
            self.package_applied = True
            self.save()
            coin_tran.transaction = self
            coin_tran.save()


class CoinTransaction(models.Model):
    user = models.ForeignKey('loginapp.User')
    coins = models.IntegerField(default=0)
    amount = models.IntegerField(null=True, blank=True, help_text='Amount of currency paid for this coins')
    applied = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    serial_number = models.CharField(max_length=24)
    transaction = models.ForeignKey(BazzarTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    # desc = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return '<{}-{}-{}>'.format(self.user.username, self.coins, self.applied)

    @atomic
    def apply(self):
        if not self.applied:
            self.user.coins = self.user.coins + self.coins
            if self.user.coins < 0:
                raise Exception('Low budget')
            self.user.save(update_fields=['coins'])
            self.applied = True
            self.save()

    @classmethod
    def buy_post(cls, user, post):
        if not post.can_buy(user=user):
            raise Exception('Insufficient_Budget')

        c_tran = cls.objects.create(user=user, coins=-1 * post.price)

        try:
            c_tran.apply()
        except Exception as e:
            raise Exception('Try_later')

        post_property = user.inventory.add_post(post=post, tran=c_tran)

        posts = user.inventory.get_valid_posts()
        user.refresh_from_db(fields=['coins'])
        return dict(posts=[{'id': x.post.id, 'count': x.count} for x in posts],
                    coins=user.coins), post_property

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.serial_number:
            self.serial_number = str(uuid.uuid4().int)[:16]
        super(CoinTransaction, self).save(force_insert=force_insert,
                                          force_update=force_update,
                                          using=using,
                                          update_fields=update_fields)
