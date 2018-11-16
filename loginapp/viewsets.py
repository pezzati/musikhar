from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# from inventory.models import Property
# from karaoke.serializers import SingleGenreSerializer
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import Artist, User
from loginapp.searchs import UserSearch, ArtistSearch
from loginapp.serializers import ArtistSerializer, UserSerializer
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet


class UserViewSet(PermissionReadOnlyModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    search_class = UserSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        user = request.user
        return Response(data=self.serializer_class(instance=user, context=self.get_serializer_context()).data)

    def get_queryset(self):
        return User.objects.all()

    @list_route()
    def my_poems(self, request):
        from karaoke.serializers import PoemSerializer
        return self.do_pagination(queryset=request.user.poems, serializer_class=PoemSerializer)

    @list_route()
    def my_songs(self, request):
        from karaoke.serializers import SongSerializer
        return self.do_pagination(queryset=request.user.songs, serializer_class=SongSerializer)

    @list_route()
    def inventory(self, request):
        posts = request.user.inventory.get_valid_posts()
        res = dict(posts=[{'id': x.post.id, 'count': x.count} for x in posts])
        return Response(data=res)

    @detail_route()
    def poems(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request=request, obj=user)

        from karaoke.serializers import PoemSerializer
        return self.do_pagination(queryset=user.poems, serializer_class=PoemSerializer)

    @detail_route()
    def songs(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request=request, obj=user)

        from karaoke.serializers import SongSerializer
        return self.do_pagination(queryset=user.songs, serializer_class=SongSerializer)


class ArtistViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = ArtistSerializer
    search_class = ArtistSearch
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Artist.objects.all()

    @detail_route()
    def full_singer(self, request, pk):
        artist = Artist.objects.get(pk=pk)

        from karaoke.serializers import SongSerializer
        return self.do_pagination(queryset=artist.singed.all(), serializer_class=SongSerializer)

    @detail_route()
    def full_song_poems(self, request, pk):
        artist = Artist.objects.get(pk=pk)

        from karaoke.serializers import SongSerializer
        return self.do_pagination(queryset=artist.song_poems.all(), serializer_class=SongSerializer)

    @detail_route()
    def full_poems(self, request, pk):
        artist = Artist.objects.get(pk=pk)

        from karaoke.serializers import PoemSerializer
        return self.do_pagination(queryset=artist.poem_set.all(), serializer_class=PoemSerializer)

    @detail_route()
    def full_composed(self, request, pk):
        artist = Artist.objects.get(pk=pk)

        from karaoke.serializers import SongSerializer
        return self.do_pagination(queryset=artist.composed.all(), serializer_class=SongSerializer)
