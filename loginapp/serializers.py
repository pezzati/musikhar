from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from loginapp.models import User, Device, Token, Artist
from musikhar.abstractions.serializers import MySerializer
from musikhar.utils import get_not_none


class UserProfileSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField(read_only=True, required=False)
    following_count = serializers.SerializerMethodField(read_only=True, required=False)
    post_count = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'gender', 'birth_date', 'image', 'mobile', 'email', 'bio',
                  'first_name', 'last_name', 'follower_count', 'following_count', 'post_count')

    def update(self, instance, validated_data):
        instance.gender = get_not_none(validated_data, 'gender', instance.gender)
        instance.birth_date = get_not_none(validated_data, 'birth_date', instance.birth_date)
        instance.mobile = get_not_none(validated_data, 'mobile', instance.mobile)
        instance.bio = get_not_none(validated_data, 'bio', instance.bio)
        instance.first_name = get_not_none(validated_data, 'first_name', instance.first_name)
        instance.last_name = get_not_none(validated_data, 'last_name', instance.last_name)
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        instance.save()
        return instance

    def get_follower_count(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return ''
        return obj.get_followers().count()

    def get_following_count(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return ''
        return obj.get_following().count()

    def get_post_count(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return ''
        return obj.ownerships.count()


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


class ArtistSerializer(MySerializer):
    song_poems = serializers.SerializerMethodField(required=False, read_only=True)
    poems = serializers.SerializerMethodField(required=False, read_only=True)
    composed = serializers.SerializerMethodField(required=False, read_only=True)
    singed = serializers.SerializerMethodField(required=False, read_only=True)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('users:get-artist-list'), obj.id)

    def get_song_poems(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import SongSerializer
        songs = obj.song_poems.all()[:10]
        serializer = SongSerializer(songs, many=True,
                                    context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    def get_poems(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import PoemSerializer
        poems = obj.poem_set.all()[:10]
        serializer = PoemSerializer(poems, many=True,
                                    context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    def get_composed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import SongSerializer
        karaokes = obj.composed.all()[:10]
        serializer = SongSerializer(karaokes, many=True,
                                    context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    def get_singed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import SongSerializer
        songs = obj.singed.all()[:10]
        serializer = SongSerializer(songs, many=True,
                                    context={'request': self.context.get('request'), 'caller': self.Meta.model})
        return serializer.data

    class Meta:
        model = Artist
        fields = ('id', 'name', 'link', 'image', 'song_poems', 'poems', 'composed', 'singed')
