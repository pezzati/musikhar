from karaoke.models import Song, Genre
from musikhar.abstractions.search import ModelSearch


class PostSearch(ModelSearch):
    model = Song
    model_has_tags = True
    search_fields = ('name', 'description')


class GenreSearch(ModelSearch):
    model = Genre
    search_fields = ('name',)
