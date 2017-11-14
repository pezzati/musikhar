from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db import models

from analytics.models import Like, Favorite
from karaoke.models import Song, Post, Genre, Poem, PostOwnerShip
from loginapp.serializers import ArtistSerializer, UserInfoSerializer
from mediafiles.serializers import MediaFileSerializer
from musikhar.abstractions.serializers import MySerializer
from analytics.serializers import TagSerializer

from rest_framework.fields import empty


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
    link = serializers.SerializerMethodField(required=False, read_only=True)
    type = serializers.SerializerMethodField(required=False)
    content = serializers.SerializerMethodField(required=False)
    owner = serializers.SerializerMethodField(read_only=True, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    tags = TagSerializer(many=True, required=False)
    cover_photo = MediaFileSerializer(many=False, required=False)

    liked_it = serializers.SerializerMethodField(read_only=True, required=False)
    like = serializers.SerializerMethodField(required=False, read_only=True)
    is_favorite = serializers.SerializerMethodField(required=False, read_only=True)

    def get_type(self, obj):
        return obj.subclass_type

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-song-list'), obj.id)

    def get_content(self, obj):
        if obj.subclass_type == Post.SONG_TYPE:
            return SongSerializer(instance=obj.song,
                                  context={'caller': Song, 'request': self.context.get('request')}).data
        if obj.subclass_type == Post.POEM_TYPE:
            return PoemSerializer(instance=obj.poem,
                                  context={'caller': Poem, 'request': self.context.get('request')}).data

    def get_owner(self, obj):
        return UserInfoSerializer(instance=obj.user,
                                  context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

    def get_like(self, obj):
        return obj.like_set.count()

    def get_liked_it(self, obj):
        if self.context.get('request') and self.context.get('request').user:
            return Like.user_liked_post(user=self.context.get('request').user, post=obj)
        return False

    def get_is_favorite(self, obj):
        if self.context.get('request') and self.context.get('request').user:
            return Favorite.user_favorite_post(user=self.context.get('request').user, post=obj)
        return False

    def create(self, validated_data):
        obj = Post()
        if self.context.get('request'):
            obj.user = self.context.get('request').user
        else:
            obj.user = self.context.get('user')
        obj.name = validated_data.get('name')
        obj.ownership_type = PostOwnerShip.USER_OWNER
        obj.cover_photo = validated_data.get('cover_photo')
        obj.description = validated_data.get('description')
        obj.save()
        obj.add_tags(validated_data.get('tags'))

        validated_data['content']['post'] = obj
        if validated_data.get('type') == Post.SONG_TYPE:
            serializer = SongSerializer(data=validated_data.get('content'))
        elif validated_data.get('type') == Post.POEM_TYPE:
            serializer = PoemSerializer(data=validated_data.get('content'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return obj

    def run_validation(self, data=empty):
        value = super(PostSerializer, self).run_validation(data=data)
        value['content'] = data.get('content')
        value['type'] = data.get('type')
        return value

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
            'liked_it',
            'tags',
            'cover_photo',
            'link',
            'like',
            'is_favorite',
            'genre',
            'tags',
            'cover_photo'
        )


class PoemSerializer(MySerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-song-list'), obj.id)

    def create(self, validated_data):
        post = validated_data.get('post')
        obj = Poem(post=post)
        obj.poet = validated_data.get('poet')
        obj.text = validated_data.get('text')
        obj.save()
        return obj

    def run_validation(self, data=empty):
        value = super(PoemSerializer, self).run_validation(data=data)
        if not self.context.get('caller') or self.context.get('caller') != SongSerializer.Meta.model:
            value['post'] = data.get('post')
        return value

    class Meta:
        model = Poem
        fields = (
            'poet',
            'text',
            'link'
        )


class SongSerializer(MySerializer):
    length = serializers.SerializerMethodField(required=False, read_only=True)
    file_url = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    related_poem = PoemSerializer(many=False, required=False)
    file = MediaFileSerializer(many=False, required=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-song-list'), obj.id)

    def get_file_url(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}/file'.format(self.context.get('request').domain, reverse('songs:get-post-list'), obj.id)
        return '{}{}/file'.format(reverse('songs:get-song-list'), obj.id)

    def get_length(self, obj):
        if obj.duration:
            return '{}:{}'.format(int(obj.duration / 60), int(obj.duration % 60))
        return ''

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(SongSerializer, self).to_representation(instance=instance)

    def create(self, validated_data):
        post = validated_data.get('post')
        obj = Song(post=post)
        obj.poet = validated_data.get('poet')
        obj.related_poem = validated_data.get('related_poem')
        obj.singer = validated_data.get('singer')
        obj.composer = validated_data.get('composer')
        obj.file = validated_data.get('file')
        obj.save()
        return obj

    def run_validation(self, data=empty):
        value = super(SongSerializer, self).run_validation(data=data)
        value['post'] = data.get('post')
        return value

    class Meta:
        model = Song
        fields = (
            'file',
            'poet',
            'composer',
            'singer',
            'related_poem',
            'length',
            'file_url',
            'link'
        )
