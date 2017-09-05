from rest_framework import serializers
from rest_framework.reverse import reverse

from karaoke.models import Karaoke, Post, Genre, Poem
from loginapp.serializers import ArtistSerializer


class SingleGenreSerializer(serializers.ModelSerializer):
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


class GenreSerializer(serializers.ModelSerializer):
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


class PostSerializer(serializers.ModelSerializer):
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
            'name',
            'desc',
            'cover_photo',
            'created_date',
            'type',
            'content'
        )


class PoemSerializer(serializers.ModelSerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    # lyrics = serializers.SerializerMethodField(required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-poem-list'), obj.id)

    # def get_lyrics(self, obj):
    #     # if self.context.get('detailed'):
    #     lines = obj.lyrics()
    #     serializered = LineSerializer(lines, many=True)
    #     return serializered.data
    #     # return []

    class Meta:
        model = Poem
        fields = (
            'name',
            'poet',
            'link',
            'text',
            'desc',
            'cover_photo',
            'created_date',
        )


class KaraokeSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    like = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    related_poem = PoemSerializer(many=False, required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-karaoke-list'), obj.id)

    def get_like(self, obj):
        return obj.like_set.count()

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(KaraokeSerializer, self).to_representation(instance=instance)

    class Meta:
        model = Karaoke
        fields = (
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





