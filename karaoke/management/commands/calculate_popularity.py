from django.core.management import BaseCommand
from django.utils import timezone

from karaoke.models import Post
from musikhar.middlewares import error_logger
from musikhar.utils import app_logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        app_logger.info('[CRONJOB_POPULARITY] start_time: {}'.format(timezone.now()))
        posts = Post.objects.filter(subclass_type=Post.KARAOKE_TYPE)
        updated_count = 0
        for post in posts:
            try:
                weeks = int((timezone.now() - post.created_date).days / 7)
                if weeks == 0:
                    weeks = 1
                post.popularity_rate = int(post.popularity / int(pow(weeks, 1 / 2)))
                post.save(update_fields=['popularity_rate', 'popularity'])
                updated_count += 1
            except Exception as e:
                error_logger.info('[CRONJOB_POPULARITY_ERROR] time: {}, post: {}, error: {}'.format(timezone.now(),
                                                                                                    post.id,
                                                                                                    str(e))
                                  )
        app_logger.info('[CRONJOB_POPULARITY] end_time: {}, updated_posts: {}'.format(timezone.now(), updated_count))
