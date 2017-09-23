from rest_framework.fields import empty

from mediafiles.models import MediaFile
from musikhar.abstractions.serializers import MySerializer

from rest_framework import serializers


class MediaFileSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False)

    def get_link(self, obj):
        if obj.resource_type == MediaFile.LOCAL_RESOURCE and \
                self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}'.format(self.context.get('request').domain, obj.__str__())
        return obj.__str__()

    class Meta:
        model = MediaFile
        fields = (
            'link',
            'id'
        )
