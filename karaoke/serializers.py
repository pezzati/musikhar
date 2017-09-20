from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from analytics.models import Like
from analytics.serializers import TagSerializer
from karaoke.models import Song, Post, Genre, Poem, OwnerShip
from loginapp.serializers import ArtistSerializer, UserInfoSerializer
from mediafiles.models import MediaFile
from mediafiles.serializers import MediaFileSerializer
from musikhar.abstractions.serializers import MySerializer


class SingleGenreSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    files_link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-genre-list'), obj.id)

    def get_files_link(self, obj):
        return 'http://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                               obj.id)

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name')


class GenreSerializer(MySerializer):
    children = SingleGenreSerializer(many=True, required=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    files_link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-genre-list'), obj.id)

    def get_files_link(self, obj):
        return 'http://{}{}{}/songs'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                               obj.id)

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name', 'children')


class PostSerializer(MySerializer):
    type = serializers.SerializerMethodField(required=False, read_only=True)
    content = serializers.SerializerMethodField(required=False, read_only=True)
    owner = serializers.SerializerMethodField(read_only=True, required=False)
    liked_it = serializers.SerializerMethodField(read_only=True, required=False)

    def get_type(self, obj):
        return obj.subclass_type

    def get_content(self, obj):
        if obj.subclass_type == Poem.SONG_TYPE:
            return SongSerializer(instance=obj.karaoke,
                                  context={'caller': Song, 'request': self.context.get('request')}).data
        if obj.subclass_type == Poem.POEM_TYPE:
            return PoemSerializer(instance=obj.poem,
                                  context={'caller': Poem, 'request': self.context.get('request')}).data

    def get_owner(self, obj):
        return UserInfoSerializer(instance=obj.user,
                                  context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

    def get_liked_it(self, obj):
        if self.context.get('request') and self.context.get('request').user:
            return Like.user_liked_post(user=self.context.get('request').user, post=obj)
        return False

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'description',
            'cover_photo',
            'created_date',
            'type',
            'content',
            'owner',
            'liked_it'
        )


class PoemSerializer(MySerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    owner = serializers.SerializerMethodField(required=False, read_only=True)
    liked_it = serializers.SerializerMethodField(read_only=True, required=False)
    tags = TagSerializer(many=True, required=False)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-poem-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-poem-list'), obj.id)

    def get_owner(self, obj):
        return UserInfoSerializer(instance=obj.user,
                                  context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

    def get_liked_it(self, obj):
        if self.context.get('request') and self.context.get('request').user:
            return Like.user_liked_post(user=self.context.get('request').user, post=obj)
        return False

    class Meta:
        model = Poem
        fields = (
            'id',
            'name',
            'poet',
            'link',
            'text',
            'description',
            'cover_photo',
            'created_date',
            'owner',
            'liked_it',
            'tags'
        )


class SongSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    like = serializers.SerializerMethodField(required=False, read_only=True)
    liked_it = serializers.SerializerMethodField(read_only=True, required=False)
    owner = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    related_poem = PoemSerializer(many=False, required=False)
    tags = TagSerializer(many=True, required=False)
    file = MediaFileSerializer(many=False, required=False)
    cover_photo = MediaFileSerializer(many=False, required=False)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-song-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-song-list'), obj.id)

    def get_like(self, obj):
        return obj.like_set.count()

    def get_owner(self, obj):
        return UserInfoSerializer(instance=obj.user,
                                  context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

    def get_liked_it(self, obj):
        if self.context.get('request') and self.context.get('request').user:
            return Like.user_liked_post(user=self.context.get('request').user, post=obj)
        return False

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(SongSerializer, self).to_representation(instance=instance)

    def create(self, validated_data):
        obj = Song(subclass_type=Post.SONG_TYPE)
        if self.context.get('request'):
            obj.user = self.context.get('request').user
        else:
            obj.user = self.context.get('user')
        obj.name = validated_data.get('name')
        obj.ownership_type = OwnerShip.USER_OWNER
        obj.poet = validated_data.get('poet')
        obj.related_poem = validated_data.get('related_poem')
        obj.singer = validated_data.get('singer')
        obj.composer = validated_data.get('composer')
        obj.file = validated_data.get('file')
        obj.cover_photo = validated_data.get('cover_photo')
        obj.description = validated_data.get('description')
        obj.save()
        obj.add_tags(validated_data.get('tags'))
        return obj

    class Meta:
        model = Song
        fields = (
            'id',
            'owner',
            'link',
            'name',
            'file',
            'like',
            'poet',
            'genre',
            'composer',
            'singer',
            'related_poem',
            'description',
            'cover_photo',
            'created_date',
            'liked_it',
            'tags'
        )
