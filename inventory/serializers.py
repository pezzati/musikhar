from inventory.models import PostProperty
from karaoke.models import Post
from karaoke.serializers import PostSerializer
from rest_framework import serializers
# from musikhar.abstractions.serializers import MySerializer


class PostPropertySerializer(PostSerializer):
    user_count = serializers.SerializerMethodField(required=False, read_only=True)

    def get_user_count(self, obj):
        return obj.postproerty_set.get(inventory=self.context.get('request'))

    def get_field_names(self, declared_fields, info):
        field_names = super(PostPropertySerializer, self).get_field_names(declared_fields, info)
        field_names.append('user_count')

    class Meta:
        models = Post
