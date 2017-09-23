from karaoke.models import Song
from musikhar.abstractions.search import ModelSearch


class SongSearch(ModelSearch):
    model = Song
    search_fields = ('name', 'description')
