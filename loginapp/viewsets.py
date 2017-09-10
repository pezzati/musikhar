from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from karaoke.serializers import SongSerializer, PoemSerializer
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import Artist
from loginapp.serializers import ArtistSerializer
from musikhar.abstractions.views import PermissionModelViewSet


class ArtistViewSet(PermissionModelViewSet):
    serializer_class = ArtistSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Artist.objects.all()

    @detail_route()
    def full_singer(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        return self.do_pagination(queryset=artist.singed.all(), serializer_class=SongSerializer)

    @detail_route()
    def full_song_poems(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        return self.do_pagination(queryset=artist.song_poems.all(), serializer_class=SongSerializer)

    @detail_route()
    def full_poems(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        return self.do_pagination(queryset=artist.poem_set.all(), serializer_class=PoemSerializer)

    @detail_route()
    def full_composed(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        return self.do_pagination(queryset=artist.composed.all(), serializer_class=SongSerializer)
