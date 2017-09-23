from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from karaoke.searchs import SongSearch
from karaoke.serializers import SongSerializer, GenreSerializer, PoemSerializer, PostSerializer
from karaoke.models import Song, Genre, Poem, Post
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionModelViewSet, PermissionReadOnlyModelViewSet


class PostViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Post.objects.all()


class SongViewSet(PermissionModelViewSet):
    serializer_class = SongSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    search_class = SongSearch()

    def get_queryset(self):
        user = self.request.user
        return Song.objects.all()

    def check_object_permissions(self, request, obj):
        pass

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Song.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Song.get_new())


class GenreViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        genres = Genre.objects.filter(parent__isnull=True)
        return self.do_pagination(queryset=genres)

    def get_queryset(self):
        return Genre.objects.all()

    @detail_route()
    def songs(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        return self.do_pagination(queryset=genre.song_set.all(), serializer_class=SongSerializer)


class PoemViewSet(PermissionModelViewSet):
    serializer_class = PoemSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Poem.objects.all()

    @detail_route()
    def full(self, request, pk):
        poem = Poem.objects.get(id=pk)
        serialized = self.serializer_class(instance=poem, context={'request': self.request, 'detailed': True})
        return Response(serialized.data)

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Poem.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Poem.get_new())

