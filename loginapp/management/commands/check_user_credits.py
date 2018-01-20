from datetime import datetime

from django.core.management import BaseCommand

from loginapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=False, is_staff=False, is_premium=True)
        for user in users:
            if datetime.now().date() > user.premium_time:
                print('{} changed'.format(user.username))
                user.is_premium = False
                user.save(update_fields=['is_premium'])
