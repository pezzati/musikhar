from rest_framework.fields import empty

from mediafiles.models import MediaFile
from musikhar.abstractions.serializers import MySerializer

from rest_framework import serializers


class MediaFileSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False)

    def get_link(self, obj):
        return obj.__str__()

    class Meta:
        model = MediaFile
        fields = (
            'link',
            'id'
        )
