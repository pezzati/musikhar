from rest_framework import serializers
from loginapp.models import User, Device, Token, Artist
from musikhar.utils import get_not_none


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'gender', 'birth_date', 'image', 'mobile', 'email')

    def update(self, instance, validated_data):
        instance.gender = get_not_none(validated_data, 'gender', instance.gender)
        instance.birth_date = get_not_none(validated_data, 'birth_date', instance.birth_date)
        instance.mobile = get_not_none(validated_data, 'mobile', instance.mobile)
        if validated_data.get('email'):
            instance.email = validated_data.get('email')
        instance.save()
        return instance


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

    def get_poetried(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.poetried.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True)
        return serializer.data

    def get_composed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.composed.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True)
        return serializer.data

    def get_singed(self, obj):
        if self.context.get('caller') != self.Meta.model:
            return []
        from karaoke.serializers import KaraokeSerializer
        karaokes = obj.singed.all()[:10]
        serializer = KaraokeSerializer(karaokes, many=True)
        return serializer.data

    class Meta:
        model = Artist
        fields = ('name', 'poetried', 'composed', 'singed')
