from rest_framework import serializers
from rest_framework.reverse import reverse

from karaoke.models import Karaoke, Post, Line, Genre, Poem
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


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ('text', 'start_time', 'end_time')


class PoemSerializer(serializers.ModelSerializer):
    poet = ArtistSerializer(required=False, many=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    lyrics = serializers.SerializerMethodField(required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-poem-list'), obj.id)

    def get_lyrics(self, obj):
        # if self.context.get('detailed'):
        lines = obj.lyrics()
        serializered = LineSerializer(lines, many=True)
        return serializered.data
        # return []

    class Meta:
        model = Poem
        fields = (
            'name',
            'poet',
            'link',
            'lyrics'
        )


class KaraokeSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField(required=False, read_only=True)
    poet = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)
    genre = SingleGenreSerializer(many=False, required=False)
    poem = PoemSerializer(many=False, required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-karaoke-list'), obj.id)

    def to_representation(self, instance):
        self.context['caller'] = self.Meta.model
        return super(KaraokeSerializer, self).to_representation(instance=instance)

    class Meta:
        model = Karaoke
        fields = (
            'link',
            'name',
            'file',
            'rate',
            'rate_count',
            'cover_photo',
            'poet',
            'genre',
            'composer',
            'singer',
            'poem',
        )





