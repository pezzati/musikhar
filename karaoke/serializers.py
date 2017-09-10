from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from karaoke.models import Song, Post, Genre, Poem, OwnerShip
from loginapp.serializers import ArtistSerializer, UserProfileSerializer
from mediafiles.models import MediaFile
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
        return 'http://{}{}{}/karaokes'.format(self.context.get('request').domain, reverse('songs:get-genre-list'),
                                               obj.id)

    class Meta:
        model = Genre
        fields = ('link', 'files_link', 'name', 'children')


# class LineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Line
#         fields = ('text', 'start_time', 'end_time')


class PostSerializer(MySerializer):
    type = serializers.SerializerMethodField(required=False, read_only=True)
    content = serializers.SerializerMethodField(required=False, read_only=True)
    owner = serializers.SerializerMethodField(read_only=True, required=False)

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
        if obj.type == Post.SYSTEM_OWNER:
            return ''
        return UserProfileSerializer(instance=obj.user,
                                     context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

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
            'owner'
        )


class PoemSerializer(MySerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    owner = serializers.SerializerMethodField(required=False, read_only=True)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-poem-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-poem-list'), obj.id)

    def get_owner(self, obj):
        if obj.type == Post.SYSTEM_OWNER:
            return ''
        return UserProfileSerializer(instance=obj.user,
                                     context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

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
            'owner'
        )


class SongSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    like = serializers.SerializerMethodField(required=False, read_only=True)
    owner = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    related_poem = PoemSerializer(many=False, required=False)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-song-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-song-list'), obj.id)

    def get_like(self, obj):
        return obj.like_set.count()

    def get_owner(self, obj):
        if obj.type == Post.SYSTEM_OWNER:
            return ''
        return UserProfileSerializer(instance=obj.user,
                                     context={'request': self.context.get('request'), 'caller': self.Meta.model}).data

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
        obj.type = OwnerShip.USER_OWNER
        obj.poet = validated_data.get('poet')
        obj.related_poem = validated_data.get('related_poem')
        obj.singer = validated_data.get('singer')
        obj.composer = validated_data.get('composer')
        obj.file = validated_data.get('file')
        obj.save()
        return obj

    def run_validation(self, data=empty):
        if data and data != empty and data.get('file'):
            try:
                data['file'] = MediaFile.objects.get(id=data['file']).file
            except MediaFile.DoesNotExist:
                raise Exception(MediaFile)
            if data.get('cover_photo'):
                try:
                    data['cover_photo'] = MediaFile.objects.get(id=data['cover_photo']).file
                except MediaFile.DoesNotExist:
                    raise Exception(MediaFile)

        return super(SongSerializer, self).run_validation(data=data)

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
        )





