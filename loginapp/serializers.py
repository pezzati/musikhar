from datetime import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from loginapp.models import User, Device, Artist, Avatar
from musikhar.abstractions.serializers import MySerializer
from musikhar.utils import get_not_none


class AvatarSerializer(MySerializer):
    create_on_validation = False
    link = serializers.SerializerMethodField(required=False, read_only=True)
    identifier = 'id'

    class Meta:
        model = Avatar
        fields = ('link', 'id')

    def get_link(self, obj):
        if obj.image:
            return 'https://{}{}{}'.format(self.context.get('request').domain, settings.MEDIA_URL, obj.image.name)
        return ''


class UserInfoSerializer(MySerializer):
    create_on_validation = False
    # follower_count = serializers.SerializerMethodField(read_only=True, required=False)
    # following_count = serializers.SerializerMethodField(read_only=True, required=False)
    # post_count = serializers.SerializerMethodField(read_only=True, required=False)
    # is_following = serializers.SerializerMethodField(read_only=True, required=False)
    premium_days = serializers.SerializerMethodField(read_only=True, required=False)
    avatar = AvatarSerializer()

    class Meta:
        model = User
        fields = ('username',
                  # 'gender',
                  # 'birth_date',
                  'image',
                  'mobile',
                  'email',
                  # 'bio',
                  'first_name',
                  'last_name',
                  # 'is_public',
                  # 'follower_count',
                  # 'following_count',
                  # 'post_count',
                  # 'is_following',
                  # 'is_premium',
                  'premium_days',
                  'coins',
                  'avatar')

    def update(self, instance, validated_data):
        instance.username = get_not_none(validated_data, 'username', instance.username)
        instance.gender = get_not_none(validated_data, 'gender', instance.gender)
        instance.birth_date = get_not_none(validated_data, 'birth_date', instance.birth_date)
        instance.bio = get_not_none(validated_data, 'bio', instance.bio)
        instance.first_name = get_not_none(validated_data, 'first_name', instance.first_name)
        instance.last_name = get_not_none(validated_data, 'last_name', instance.last_name)
        instance.is_public = get_not_none(validated_data, 'is_public', instance.is_public)
        instance.avatar = get_not_none(validated_data, 'avatar', instance.avatar)

        if validated_data.get('mobile'):
            if not instance.mobile or instance.mobile != validated_data.get('mobile'):
                instance.mobile_confirmed = False
                instance.send_mobile_verification()
            instance.mobile = validated_data.get('mobile')

        if validated_data.get('email'):
            if not instance.email or instance.email != validated_data.get('email'):
                instance.email_confirmed = False
                instance.send_email_verification()
            instance.email = validated_data.get('email')

        instance.save()
        return instance

    # def get_follower_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.get_followers().count()
    #
    # def get_following_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.get_following().count()
    #
    # def get_post_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.ownerships.count()
    #
    # def get_is_following(self, obj):
    #     if self.context.get('request') and self.context.get('request').user:
    #         return obj.is_follower(self.context.get('request').user)
    #     return False

    @staticmethod
    def get_premium_days(obj):
        if obj.is_premium:
            return (obj.premium_time - datetime.now().date()).days
        else:
            return 0


class UserSerializer(serializers.ModelSerializer):
    premium_days = serializers.SerializerMethodField(read_only=True, required=False)
    avatar = AvatarSerializer(read_only=True, required=False)

    # follower_count = serializers.SerializerMethodField(read_only=True, required=False)
    # following_count = serializers.SerializerMethodField(read_only=True, required=False)
    # post_count = serializers.SerializerMethodField(read_only=True, required=False)
    # is_following = serializers.SerializerMethodField(read_only=True, required=False)
    # songs = serializers.SerializerMethodField(required=False, read_only=True)
    # poems = serializers.SerializerMethodField(required=False, read_only=True)

    # def get_is_following(self, obj):
    #     if self.context.get('request') and self.context.get('request').user:
    #         return obj.is_follower(self.context.get('request').user)
    #     return False
    #
    # def get_follower_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.get_followers().count()
    #
    # def get_following_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.get_following().count()
    #
    # def get_post_count(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return 0
    #     return obj.ownerships.count()
    #
    # def get_songs(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return None
    #     if self.context.get('request') and self.context.get('request').user:
    #         if not obj.user_has_access(self.context.get('request').user):
    #             return None
    #     from karaoke.serializers import SongSerializer
    #     songs = obj.songs[:10]
    #     return SongSerializer(songs, many=True, context=self.context).data
    #
    # def get_poems(self, obj):
    #     if self.context.get('caller') != self.Meta.model:
    #         return None
    #     if self.context.get('request') and self.context.get('request').user:
    #         if not obj.user_has_access(self.context.get('request').user):
    #             return None
    #     from karaoke.serializers import PoemSerializer
    #     poems = obj.poems[:10]
    #     return PoemSerializer(poems, many=True, context=self.context).data

    @staticmethod
    def get_premium_days(obj):
        if obj.is_premium:
            return (obj.premium_time - datetime.now().date()).days
        else:
            return 0

    class Meta:
        model = User
        fields = ('username',
                  # 'gender',
                  # 'birth_date',
                  'image',
                  'mobile',
                  'email',
                  # 'bio',
                  # 'is_public',
                  'first_name',
                  'last_name',
                  # 'follower_count',
                  # 'following_count',
                  # 'post_count',
                  # 'poems',
                  # 'songs',
                  # 'is_following',
                  'premium_days',
                  'coins',
                  'avatar'
                  )


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
    # song_poems_count = serializers.SerializerMethodField(required=False, read_only=True)
    poems_count = serializers.SerializerMethodField(required=False, read_only=True)
    # composed_count = serializers.SerializerMethodField(required=False, read_only=True)
    # singed_count = serializers.SerializerMethodField(required=False, read_only=True)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('users:get-artist-list'), obj.id)

    # def get_song_poems_count(self, obj):
    #     return obj.song_poems.all().count()

    def get_poems_count(self, obj):
        return obj.poem_set.all().count()

    # def get_composed_count(self, obj):
    #     return obj.composed.all().count()

    # def get_singed_count(self, obj):
    #     return obj.singed.all().count()

    class Meta:
        model = Artist
        fields = ('id',
                  'name',
                  'link',
                  'image',
                  # 'song_poems_count',
                  'poems_count',
                  # 'composed_count',
                  # 'singed_count'
                  )
