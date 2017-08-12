from rest_framework import serializers
from karaoke.models import Karaoke, Post, Line, Genre


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ('text', 'start_time', 'end_time')


class KaraokeSerializer(serializers.ModelSerializer):
    lyrics = serializers.SerializerMethodField(required=False, read_only=True)

    def get_lyrics(self, obj):
        lyrics = obj.lyrics
        response = [LineSerializer(x).data for x in lyrics]
        return response

    class Meta:
        model = Karaoke
        fields = ('id', 'name', 'file', 'rate', 'rate_count', 'cover_photo', 'lyrics')


class SingleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(required=False, read_only=True)

    def get_children(self, obj):
        children = obj.children.all()
        return [GenreSerializer(instance=x).data for x in children]

    class Meta:
        model = Genre
        fields = ('id', 'name', 'children')
