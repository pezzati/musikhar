from rest_framework import serializers
from rest_framework.reverse import reverse

from karaoke.models import Karaoke, Post, Line, Genre
from loginapp.serializers import ArtistSerializer


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ('text', 'start_time', 'end_time')


class KaraokeSerializer(serializers.ModelSerializer):
    lyrics = LineSerializer(many=True, required=False)
    link = serializers.SerializerMethodField(required=False, read_only=True)
    poem = ArtistSerializer(many=False, required=False)
    composer = ArtistSerializer(many=False, required=False)
    singer = ArtistSerializer(many=False, required=False)

    def get_link(self, obj):
        return 'http://{}{}{}'.format(self.context.get('request').domain, reverse('songs:get-karaoke-list'), obj.id)

    class Meta:
        model = Karaoke
        fields = (
            'link',
            'name',
            'file',
            'rate',
            'rate_count',
            'cover_photo',
            'poem',
            'genre',
            'composer',
            'singer',
            'lyrics',
        )


class SingleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    children = SingleGenreSerializer(many=True, required=False)

    class Meta:
        model = Genre
        fields = ('id', 'name', 'children')
