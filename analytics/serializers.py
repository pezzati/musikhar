from django.conf import settings

from rest_framework.fields import empty
from rest_framework import serializers
from rest_framework.reverse import reverse

from analytics.models import Tag, Banner, Event
from musikhar.abstractions.serializers import MySerializer


class TagSerializer(MySerializer):
    identifier = 'name'
    create_on_validation = True

    def run_validation(self, data=empty):
        if data and data != empty and data.get(self.identifier) and data.get(self.identifier) != 0:
            data[self.identifier] = u'#' + data[self.identifier]
        return super(TagSerializer, self).run_validation(data=data)

    class Meta:
        model = Tag
        fields = ('name',)


class BannerSerializer(MySerializer):
    file = serializers.SerializerMethodField(required=False, read_only=True)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_file(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, settings.MEDIA_URL, obj.file.name)
        return '{}{}'.format(settings.MEDIA_URL, obj.file.name)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('analysis:get-banners-list'),
                                          obj.id)
        return '{}{}'.format(reverse('analysis:get-banners-list'), obj.id)

    class Meta:
        model = Banner
        fields = ('title', 'file', 'link', 'content_type')


class NotificationSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    post_link = serializers.SerializerMethodField(required=False, read_only=True)
    user_link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('analysis:get-notifs-list'),
                                          obj.id)
        return '{}{}'.format(reverse('analysis:get-notifs-list'), obj.id)

    def get_post_link(self, obj):
        if obj.type != Event.LIKE:
            return ''
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'),
                                          obj.post.id)
        return '{}{}'.format(reverse('songs:get-post--list'), obj.post.id)

    def get_user_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}/user/users/{}'.format(self.context.get('request').domain, obj.user.username)
        return '/user/users/{}'.format(self.context.get('request').domain, obj.user.username)

    class Meta:
        model = Event
        fields = ('id', 'creation_date', 'text', 'type', 'link', 'post_link', 'user_link')
