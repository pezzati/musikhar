from rest_framework import serializers
from karaoke.models import Karaoke, Post, Line, Genre


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ('text', 'start_time', 'end_time')


class KaraokeSerializer(serializers.ModelSerializer):
    lyrics = LineSerializer(many=True, required=False)

    class Meta:
        model = Karaoke
        fields = ('id', 'name', 'file', 'rate', 'rate_count', 'cover_photo', 'lyrics')


class SingleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    children = SingleGenreSerializer(many=True, required=False)

    class Meta:
        model = Genre
        fields = ('id', 'name', 'children')
