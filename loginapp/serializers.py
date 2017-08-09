from rest_framework import serializers

from loginapp.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'gender', 'age', 'image')
