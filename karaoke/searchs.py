from karaoke.models import Genre, Post, Karaoke
from musikhar.abstractions.search import ModelSearch


class PostSearch(ModelSearch):
    model = Post
    model_has_tags = True
    search_fields = ('name', 'description')


class KaraokeSearch(ModelSearch):
    model = Post
    model_has_tags = True
    search_fields = ('name', 'description', 'karaoke__artist__name', 'karaoke__lyric__text')


class GenreSearch(ModelSearch):
    model = Genre
    search_fields = ('name',)
