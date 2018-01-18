from karaoke.models import Genre, Post
from musikhar.abstractions.search import ModelSearch


class PostSearch(ModelSearch):
    model = Post
    model_has_tags = True
    search_fields = ('name', 'description')


class GenreSearch(ModelSearch):
    model = Genre
    search_fields = ('name',)
