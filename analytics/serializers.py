from django.conf import settings

from rest_framework import serializers
from rest_framework.reverse import reverse

from loginapp.serializers import UserInfoSerializer
from karaoke.serializers import PostSerializer
from analytics.models import Like, Favorite, Tag, Banner
from musikhar.abstractions.serializers import MySerializer


class LikeSerializer(MySerializer):
    user = UserInfoSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    class Meta:
        model = Like
        fields = (
            'user',
            'time',
            'post'
        )


class FavoriteSerializer(MySerializer):
    user = UserInfoSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    class Meta:
        model = Favorite
        fields = (
            'user',
            'time',
            'post'
        )


class TagSerializer(MySerializer):
    identifier = 'name'
    create_on_validation = True

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
