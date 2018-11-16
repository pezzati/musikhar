from django.db import models
from django.db.transaction import atomic
from django.db.models import Q
from django.utils import timezone

from loginapp.models import User
from karaoke.models import Post


class Property(models.Model):
    POST_PROPERTY = 'post'
    TYPES = (
        (POST_PROPERTY, 'Post Property'),
    )
    property_type = models.CharField(max_length=8, choices=TYPES, default=POST_PROPERTY)
    inventory = models.ForeignKey('inventory.Inventory')
    creation_date = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    tran = models.ForeignKey('financial.CoinTransaction', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}'.format(self.property_type)


class PostProperty(Property):
    post = models.ForeignKey(Post)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.post.name, self.count)

    @atomic
    def use(self):
        self.count -= 1
        if self.count == 0:
            self.is_deleted = True
        self.save(update_fields=['count', 'is_deleted'])
        return self


class Inventory(models.Model):
    user = models.OneToOneField(User)
    posts = models.ManyToManyField(Post, through=PostProperty)

    def __str__(self):
        return self.user.username

    def add_post(self, post, tran=None):
        if not tran:
            PostProperty.objects.create(post=post, count=post.count, inventory=self)
        else:
            PostProperty.objects.create(post=post, count=post.count, inventory=self, tran=tran)

    def get_valid_posts(self):
        posts = self.postproperty_set.filter(property_type=PostProperty.POST_PROPERTY,
                                             is_deleted=False,
                                             # exp_date__gt=timezone.now(),
                                             count__gt=0)#.values('post__id')
        # return self.posts.filter(id__in=posts_ids)
        return posts

    def is_in_inventory(self, post):
        posts = self.postproperty_set.filter(property_type=PostProperty.POST_PROPERTY,
                                             is_deleted=False,
                                             post=post,
                                             # exp_date__gt=timezone.now(),
                                             count__gt=0)
        if posts.count() > 0:
            return posts.first()
        return None
