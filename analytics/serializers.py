from loginapp.serializers import UserInfoSerializer
from karaoke.serializers import PostSerializer
from analytics.models import Like, Favorite, Tag
from musikhar.abstractions.serializers import MySerializer


class LikeSerializer(MySerializer):
    user = UserInfoSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    class Meta:
        model = Like
        fields = (
            'user',
            'time',
            'post'
        )


class FavoriteSerializer(MySerializer):
    user = UserInfoSerializer(required=False, many=False)
    post = PostSerializer(required=False, many=False)

    class Meta:
        model = Favorite
        fields = (
            'user',
            'time',
            'post'
        )


class TagSerializer(MySerializer):
    identifier = 'name'
    create_on_validation = True

    class Meta:
        model = Tag
        fields = ('name',)
