from rest_framework import serializers
from karaoke.models import Karaoke, Post, Line, Genre


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = ('text', 'start_time', 'end_time')


class KaraokeSerializer(serializers.ModelSerializer):
    lyrics = serializers.SerializerMethodField(required=False)

    def get_lyrics(self, obj):
        lyrics = obj.line_set.all().order_by('start_time')
        response = [LineSerializer(x).data for x in lyrics]
        return response

    class Meta:
        model = Karaoke
        fields = ('id', 'name', 'file', 'rate', 'rate_count', 'cover_photo', 'lyrics')






