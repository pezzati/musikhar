from django.db import models

from loginapp.models import User
from karaoke.models import Post


class Property(models.Model):
    POST_PROPERTY = 'post'
    TYPES = (
        (POST_PROPERTY, 'Post Property'),
    )
    user = models.ForeignKey(User, related_name='inventory')
    property_type = models.CharField(max_length=8, choices=TYPES, default=POST_PROPERTY)
    creation_date = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.property_type)


class PostProperty(Property):
    owner = models.OneToOneField(Property)
    post = models.ForeignKey(Post)
    count = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}-{}'.format(self.owner.__str__(), self.post.name, self.count)

