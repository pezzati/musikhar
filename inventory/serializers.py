from inventory.models import PostProperty, Inventory
from karaoke.models import Post
from karaoke.serializers import PostSerializer
from rest_framework import serializers
# from musikhar.abstractions.serializers import MySerializer
from musikhar.abstractions.serializers import MySerializer


class PostPropertySerializer(PostSerializer):
    user_count = serializers.SerializerMethodField(required=False, read_only=True)

    def get_user_count(self, obj):
        return obj.postproerty_set.get(inventory=self.context.get('request'))

    def get_field_names(self, declared_fields, info):
        field_names = super(PostPropertySerializer, self).get_field_names(declared_fields, info)
        field_names.append('user_count')

    class Meta:
        models = Post


class InventorySerializer(MySerializer):
    posts = serializers.SerializerMethodField(required=False, read_only=True)
    coins = serializers.SerializerMethodField(required=False, read_only=True)
    days = serializers.SerializerMethodField(required=False, read_only=True)

    def get_posts(self, obj):
        posts = obj.get_valid_posts()
        return [{'id': x.post.id, 'count': x.count} for x in posts]

    def get_coins(self, obj):
        obj.user.refresh_from_db()
        return obj.user.coins

    def get_days(self, obj):
        return obj.user.premium_days

    class Meta:
        model = Inventory
        fields = ('posts', 'coins', 'days')
