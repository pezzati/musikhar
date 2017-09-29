from loginapp.models import User, Artist
from musikhar.abstractions.search import ModelSearch


class UserSearch(ModelSearch):
    model = User
    search_fields = ('username', 'first_name', 'last_name', 'emial', 'mobile')


class ArtistSearch(ModelSearch):
    model = Artist
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'name')
