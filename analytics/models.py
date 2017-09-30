from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.core.urlresolvers import resolve, Resolver404


from karaoke.models import Post
from loginapp.models import User


class Like(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        Like.objects.get()
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)

    @classmethod
    def user_liked_post(cls, user, post):
        try:
            cls.objects.get(user=user, post=post)
            return True
        except cls.DoesNotExist:
            return False


class Favorite(models.Model):

    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, null=True, blank=True)
    time = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return '{}-{}:{}'.format(self.user.username, self.post.subclass_type, self.post)

    @classmethod
    def user_favorite_post(cls, user, post):
        try:
            cls.objects.get(user=user, post=post)
            return True
        except cls.DoesNotExist:
            return False


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.replace(' ', '_')
        if self.name[0] != '#':
            self.name = '#{}'.format(self.name)
        super(Tag, self).save(force_insert=force_insert,
                              force_update=force_update,
                              using=using,
                              update_fields=update_fields)


class TagPost(models.Model):
    tag = models.ForeignKey(Tag)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.tag.name, self.post.name)


class UserFileHistory(models.Model):
    requested_user = models.ForeignKey(User, related_name='requested_files_history', null=True, blank=True)
    owner_user = models.ForeignKey(User, null=True, blank=True, related_name='is_requested_files_history')
    file_path = models.CharField(max_length=150, default='')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.requested_user.username, self.date, self.file.name)


def get_path(instance, filename):
    filename = filename.lower()
    time = timezone.now()
    return 'banners/{}_{}/{}_{}'.format(time.year, time.month, time.date(), filename)


class Banner(models.Model):
    POST_TYPE = 'post'
    SONG_TYPE = 'song'
    POEM_TYPE = 'poem'
    TYPE_CHOICES = (
        (POST_TYPE, 'post object'),
        (SONG_TYPE, 'song object'),
        (POEM_TYPE, 'poem object')
    )

    file = models.FileField(upload_to=get_path)
    title = models.CharField(max_length=100, help_text='Persian text that will be shown ti user')
    link = models.CharField(max_length=100, null=True, blank=True)
    clicked_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SONG_TYPE)
    index = models.IntegerField(default=1)

    class Meta:
        ordering = ['index']

    def __str__(self):
        return self.title

    @atomic
    def clicked(self):
        self.clicked_count += 1
        self.save()
        return self

    def get_redirect_url(self, request=None):
        if self.link:
            if request:
                return 'http://{}{}'.format(request.domain, self.link)
            else:
                return self.link
        return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.link and not self.link.startswith('http://') and not self.link.startswith('https://'):
            if self.link[0] != '/':
                self.link = '/{}'.format(self.link)
            while self.link.__contains__('//'):
                self.link = self.link.replace('//', '/')
            try:
                resolve(self.link)
            except Resolver404:
                if self.link[-1] != '/':
                    self.link = '{}/'.format(self.link)
                try:
                    resolve(self.link)
                except Resolver404:
                    self.is_active = False
                    self.link = 'this url: <{}> does not exists'.format(self.link)
        super(Banner, self).save(force_insert=force_insert,
                                 force_update=force_update,
                                 using=using,
                                 update_fields=update_fields)

    @classmethod
    def active_banners(cls):
        time = timezone.now()
        return cls.objects.filter(is_active=True, start_time__lte=time, end_time__gte=time)
