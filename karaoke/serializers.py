from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.reverse import reverse

from karaoke.models import Karaoke, Post, Genre, Poem, OwnerShip
from loginapp.models import Artist
from loginapp.serializers import ArtistSerializer
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

    def get_type(self, obj):
        return obj.subclass_type

    def get_content(self, obj):
        if obj.subclass_type == Poem.KARAOKE_TYPE:
            return KaraokeSerializer(instance=obj.karaoke,
                                     context={'caller': Karaoke, 'request': self.context.get('request')}).data
        if obj.subclass_type == Poem.POEM_TYPE:
            return PoemSerializer(instance=obj.poem,
                                  context={'caller': Poem, 'request': self.context.get('request')}).data

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'desc',
            'cover_photo',
            'created_date',
            'type',
            'content'
        )


class PoemSerializer(MySerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    # lyrics = serializers.SerializerMethodField(required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-poem-list'), obj.id)

    class Meta:
        model = Poem
        fields = (
            'id',
            'name',
            'poet',
            'link',
            'text',
            'desc',
            'cover_photo',
            'created_date',
        )


class KaraokeSerializer(MySerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    like = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    related_poem = PoemSerializer(many=False, required=False)

    def get_link(self, obj):
        if self.context.get('request') and self.context.get('request') is not None:
            return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-karaoke-list'), obj.id)
        return '{}{}'.format(reverse('songs:get-karaoke-list'), obj.id)

    def get_like(self, obj):
        return obj.like_set.count()

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(KaraokeSerializer, self).to_representation(instance=instance)

    def create(self, validated_data):
        obj = Karaoke(subclass_type=Post.KARAOKE_TYPE)
        obj.name = validated_data.get('name', 'SHIT name')
        obj.type = OwnerShip.USER_OWNER
        obj.poet = validated_data.get('poet')
        obj.related_poem = validated_data.get('related_poem')
        obj.singer = validated_data.get('singer')
        obj.composer = validated_data.get('composer')
        obj.save()
        return obj

    class Meta:
        model = Karaoke
        fields = (
            'id',
            'link',
            'name',
            'file',
            'like',
            'poet',
            'genre',
            'composer',
            'singer',
            'related_poem',
            'desc',
            'cover_photo',
            'created_date',
        )





