import json
from rest_framework import serializers
from rest_framework.reverse import reverse
#from django.utils import timezone

from analytics.models import Like, Favorite
from karaoke.models import Song, Post, Genre, Poem, PostOwnerShip, Karaoke, Feed
from loginapp.serializers import ArtistSerializer, UserInfoSerializer
from mediafiles.serializers import MediaFileSerializer
from musikhar.abstractions.serializers import MySerializer
from analytics.serializers import TagSerializer

from rest_framework.fields import empty


class SingleGenreSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    files_link = serializers.SerializerMethodField(required=False, read_only=True)
    liked_it = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-genre-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-genre-list'), obj.id)

    def get_files_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                                   obj.id)
        return '{}{}/karaokes'.format(reverse('songs:get-genre-list'), obj.id)

    def get_liked_it(self, obj):
        if self.context.get('request'):
            if obj in self.context.get('request').user.genres.all():
                return True
        return False

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name', 'cover_photo', 'liked_it')


class GenreSerializer(MySerializer):
    children = SingleGenreSerializer(many=True, required=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    files_link = serializers.SerializerMethodField(required=False, read_only=True)
    liked_it = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-genre-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-genre-list'), obj.id)

    def get_files_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                                   obj.id)
        return '{}{}/karaokes'.format(reverse('songs:get-genre-list'), obj.id)

    def get_liked_it(self, obj):
        if self.context.get('request'):
            if obj in self.context.get('request').user.genres.all():
                return True
        return False

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name', 'children', 'cover_photo', 'liked_it')


class GenrePostSerializer(MySerializer):
    query_count = 10
    link = serializers.SerializerMethodField(required=False, read_only=True)
    files_link = serializers.SerializerMethodField(required=False, read_only=True)
    posts = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-genre-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-genre-list'), obj.id)

    def get_files_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                                   obj.id)
        return '{}{}/karaokes'.format(reverse('songs:get-genre-list'), obj.id)

    def get_posts(self, obj):
        return PostSerializer(obj.post_set.filter(subclass_type=Post.KARAOKE_TYPE)[:self.query_count], many=True,
                              context=self.context).data

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name', 'cover_photo', 'posts')


class PostSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    content = serializers.SerializerMethodField(required=False)

    artist = serializers.SerializerMethodField(required=False, read_only=True)
    cover_photo = serializers.SerializerMethodField(required=False, read_only=True)

    def get_artist(self, obj):
        if obj.subclass_type == Post.KARAOKE_TYPE:
            return ArtistSerializer(obj.karaoke.artist, context=self.context).data
        return ''

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-post-list'), obj.id)

    def get_content(self, obj):
        if self.context.get('full_data'):
            if obj.subclass_type == Post.SONG_TYPE:
                return SongSerializer(instance=obj.song,
                                      context={'caller': Song, 'request': self.context.get('request')}).data
            elif obj.subclass_type == Post.POEM_TYPE:
                return PoemSerializer(instance=obj.poem,
                                      context={'caller': Poem, 'request': self.context.get('request')}).data
            elif obj.subclass_type == Post.KARAOKE_TYPE:
                return KaraokeSerializer(instance=obj.karaoke,
                                         context={'caller': Karaoke, 'request': self.context.get('request')}).data
        return ''

    def get_cover_photo(self, obj):
        photo = obj.get_cover()
        if photo:
            return MediaFileSerializer(photo).data
        return

    def create(self, validated_data):
        if validated_data.get('type') == Post.KARAOKE_TYPE:
            raise Exception('Can not create Karaoke post')
        obj = Post()
        if self.context.get('request'):
            obj.user = self.context.get('request').user
        else:
            obj.user = self.context.get('user')
        obj.name = validated_data.get('name')
        obj.ownership_type = PostOwnerShip.USER_OWNER
        obj.cover_photo = validated_data.get('cover_photo')
        obj.description = validated_data.get('description')
        obj.genre = validated_data.get('genre')
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
            'cover_photo',
            'content',
            'link',
            'is_premium',
            'artist',
            'price',
            'count'
        )


class PoemSerializer(MySerializer):
    identifier = 'post__id'
    key_identifier = 'id'

    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'),
                                          obj.post.id)
        return '{}{}'.format(reverse('songs:get-post-list'), obj.post.id)

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


class KaraokeSerializer(MySerializer):
    identifier = 'post__id'
    key_identifier = 'id'

    artist = ArtistSerializer(many=False, required=False)
    lyric = PoemSerializer(many=False, required=False)

    link = serializers.SerializerMethodField(required=False, read_only=True)
    karaoke_file_url = serializers.SerializerMethodField(required=False, read_only=True)
    original_file_url = serializers.SerializerMethodField(required=False, read_only=True)
    length = serializers.SerializerMethodField(required=False, read_only=True)
    midi = serializers.SerializerMethodField(required=False, read_only=True)

    def get_midi(self, obj):
        if obj.mid:
            try:
                return json.loads(obj.mid)
            except:
                pass
        return ''

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'),
                                          obj.post.id)
        return '{}{}'.format(reverse('songs:get-post-list'), obj.post.id)

    def get_karaoke_file_url(self, obj):
        redirect, url = obj.file.get_download_path()
        if not redirect:
            url += '?post={}'.format(obj.post.id)
            if self.context.get('request') and self.context.get('request') is not None:
                return 'https://{}{}'.format(self.context.get('request').domain, url)
        return url

    def get_original_file_url(self, obj):
        if obj.full_file:
            redirect, url = obj.full_file.get_download_path()
            if not redirect:
                url += '?post={}'.format(obj.post.id)
                if self.context.get('request') and self.context.get('request') is not None:
                    return 'https://{}{}'.format(self.context.get('request').domain, url)
            return url
        return ''

    def get_length(self, obj):
        if obj.duration:
            return '{}:{}'.format(int(obj.duration / 60), int(obj.duration % 60))
        return ''

    class Meta:
        model = Karaoke
        fields = (
            'artist',
            'lyric',
            'karaoke_file_url',
            'original_file_url',
            'link',
            'length',
            'midi'
        )


class SongSerializer(MySerializer):
    identifier = 'post__id'
    key_identifier = 'id'

    length = serializers.SerializerMethodField(required=False, read_only=True)
    file_url = serializers.SerializerMethodField(required=False, read_only=True)
    thumbnail = serializers.SerializerMethodField(required=False, read_only=True)
    karaoke = serializers.SerializerMethodField(required=False, read_only=True)
    file = MediaFileSerializer(many=False, required=True)
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_karaoke(self, obj):
        # if self.context.get('request') and self.context.get('request') is not None:
        #     karaoke_link = 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'),
        #                                            obj.karaoke.post.id)
        # else:
        #     karaoke_link = '{}{}'.format(reverse('songs:get-post-list'), obj.karaoke.post.id)

        res = dict(
            artist=obj.karaoke.artist.name,
            id=obj.karaoke.post.id
        )
        return res

    def get_thumbnail(self, obj):
        return MediaFileSerializer(obj.thumbnail).data['link'] if obj.thumbnail else ''

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-post-list'),
                                          obj.post.id)
        return '{}{}'.format(reverse('songs:get-post-list'), obj.post.id)

    def get_file_url(self, obj):
        redirect, url = obj.file.get_download_path()
        if not redirect:
            url += '?post={}'.format(obj.post.id)
            if self.context.get('request') and self.context.get('request') is not None:
                return 'https://{}{}'.format(self.context.get('request').domain, url)
        return url

    def get_length(self, obj):
        return obj.duration if obj.duration else 0.0

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(SongSerializer, self).to_representation(instance=instance)

    def create(self, validated_data):
        post = validated_data.get('post')
        obj = Song(post=post)
        obj.karaoke = validated_data.get('karaoke')
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
            'length',
            'file_url',
            'link',
            'karaoke',
            'thumbnail'
        )


class FeedSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'https://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-feed-list'),
                                          obj.code)
        return '{}{}/karaokes'.format(reverse('songs:get-feed-list'), obj.code)

    class Meta:
        model = Feed
        fields = ('name', 'link',)
