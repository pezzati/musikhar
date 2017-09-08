from rest_framework import serializers
from rest_framework.reverse import reverse
from loginapp.serializers import UserProfileSerializer
from karaoke.serializers import PostSerializer
from analytics.models import Like, Favorite


class LikeSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField(required=False, read_only=True)
    user = UserProfileSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('analysis:get-like-list'), obj.id)

    class Meta:
        model = Like
        fields = (
            'link',
            'time'
        )


class FavoriteSerializer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField(required=False, read_only=True)
    user = UserProfileSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('analysis:get-favorite-list'), obj.id)

    class Meta:
        model = Like
        fields = (
            'link',
            'time'
        )
