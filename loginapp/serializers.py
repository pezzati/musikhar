from rest_framework import serializers
from rest_framework.reverse import reverse

from loginapp.models import User, Device, Token, Artist
from musikhar.utils import get_not_none


class UserProfileSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    follower_count = serializers.CharField(max_length=10, required=False)
    following_count = serializers.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ('username', 'gender', 'birth_date', 'image', 'mobile', 'email', 'bio',
                  'first_name', 'last_name', 'follower_count', 'following_count', 'post_count')

    def update(self, instance, validated_data):
        instance.gender = get_not_none(validated_data, 'gender', instance.gender)
        instance.birth_date = get_not_none(validated_data, 'birth_date', instance.birth_date)
        instance.mobile = get_not_none(validated_data, 'mobile', instance.mobile)
        instance.bio = get_not_none(validated_data, 'bio', instance.bio)
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        instance.save()
        return instance

    def get_first_name(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []

        first_name = obj.first_name
        return first_name

    def get_last_name(self, obj):

        if self.context.get('caller') != self.Meta.model:
            return []
        last_name = obj.first_name
        return last_name

    def get_follower_count(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        follower_count = obj.get_followers().count()
        return follower_count

    def get_following_count(self, obj):

        if self.context.get('caller') != self.Meta.model:
            return []
        following_count = obj.get_following().count()
        return following_count

    def get_post_count(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        post_count = obj.get_post_count
        return post_count




class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'udid', 'user', 'type', 'os_version')

    def update(self, instance, validated_data):
        instance.udid = validated_data.get('udid', instance.udid)
        instance.user = validated_data.get('user', instance.user)
        instance.type = validated_data.get('type', instance.type)
        instance.os_version = validated_data.get('os_version', instance.os_version)
        instance.save()
        return instance


class ArtistSerializer(serializers.ModelSerializer):
    poetried = serializers.SerializerMethodField(required=False)
    composed = serializers.SerializerMethodField(required=False)
    singed = serializers.SerializerMethodField(required=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('users:get-artist-list'), obj.id)

    def get_poetried(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.poetried.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True,
                                       context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    def get_composed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.composed.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True,
                                       context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    def get_singed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.singed.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True,
                                       context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    class Meta:
        model = Artist
        fields = ('name', 'link', 'poetried', 'composed', 'singed')
