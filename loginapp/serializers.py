from rest_framework import serializers
from loginapp.models import User, Device, Token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'gender', 'age', 'image')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
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
