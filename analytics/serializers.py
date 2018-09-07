from django.conf import settings

from rest_framework.fields import empty
from rest_framework import serializers
from rest_framework.reverse import reverse

from analytics.models import Tag, Banner, Event, UserAction
from loginapp.serializers import UserSerializer
from musikhar.abstractions.serializers import MySerializer


class TagSerializer(MySerializer):
    identifier = 'name'
    key_identifier = 'name'
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
        if obj.content_type == Banner.REDIRECT:
            return obj.link
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('analysis:get-banners-list'),
                                          obj.id)
        return '{}{}'.format(reverse('analysis:get-banners-list'), obj.id)

    class Meta:
        model = Banner
        fields = ('title', 'file', 'link', 'content_type', 'description')


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


class UserActionSerializer(MySerializer):
    user = UserSerializer(read_only=True, many=False)

    def create(self, validated_data):
        user = self.context['request'].user
        obj, created = self.Meta.model.objects.get_or_create(user=user,
                                                             timestamp=validated_data.get('timestamp'),
                                                             action=validated_data.get('action'),
                                                             detail=validated_data.get('detail'),
                                                             session=validated_data.get('session')
                                                             )
        return obj

    class Meta:
        model = UserAction
        fields = ('timestamp', 'action', 'detail', 'user', 'session')
