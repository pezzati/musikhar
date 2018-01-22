from datetime import datetime

from django.core.management import BaseCommand

from loginapp.models import User
from musikhar.utils import app_logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_logger.info('[CRONJOB_CHECK_USER_PREMIUM] time: {}'.format(datetime.now()))
        users = User.objects.filter(is_superuser=False, is_staff=False, is_premium=True)
        user_list = []
        for user in users:
            if datetime.now().date() > user.premium_time:
                user.is_premium = False
                user.save(update_fields=['is_premium'])
                user_list.append(user.username)
        app_logger.info('[CRONJOB_CHECK_USER_PREMIUM] time: {}, user_count: {}, users:{}'.format(datetime.now(),
                                                                                                 len(user_list),
                                                                                                 user_list)
                        )
