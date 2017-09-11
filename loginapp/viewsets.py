from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from karaoke.serializers import SongSerializer, PoemSerializer
from loginapp.auth import CsrfExemptSessionAuthentication
from loginapp.models import Artist, User
from loginapp.serializers import ArtistSerializer, UserSerializer
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet


class UserViewSet(PermissionReadOnlyModelViewSet):
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        user = request.user
        return Response(data=self.serializer_class(instance=user, context=self.get_serializer_context()).data)

    def get_queryset(self):
        return User.objects.all()

    # def check_object_permissions(self, request, obj):
    #     if not obj.user_has_access(user=request.user):
    #         raise PermissionDenied
    #     pass

    @detail_route()
    def poems(self, request, pk):
        try:
            user = User.objects.get(username=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request=request, obj=user)
        return self.do_pagination(queryset=user.poems, serializer_class=PoemSerializer)

    @detail_route()
    def songs(self, request, pk):
        try:
            user = User.objects.get(username=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(request=request, obj=user)
        return self.do_pagination(queryset=user.songs, serializer_class=SongSerializer)


class ArtistViewSet(PermissionReadOnlyModelViewSet):
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
