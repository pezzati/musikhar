
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from karaoke.serializers import KaraokeSerializer, GenreSerializer, PoemSerializer
from karaoke.models import Karaoke, Genre, Poem
from loginapp.auth import CsrfExemptSessionAuthentication
from musikhar.abstractions.views import PermissionReadOnlyModelViewSet


class KaraokeViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = KaraokeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        return Karaoke.objects.all()

    def get_object(self):
        obj = super(KaraokeViewSet, self).get_object()
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def check_object_permissions(self, request, obj):
        pass

    @list_route()
    def popular(self, request):
        return self.do_pagination(queryset=Karaoke.get_popular())

    @list_route()
    def news(self, request):
        return self.do_pagination(queryset=Karaoke.get_new())


class GenreViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Genre.objects.filter(parent__isnull=True)

    @detail_route()
    def karaokes(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        return self.do_pagination(queryset=genre.karaoke_set.all(), serializer_class=KaraokeSerializer)


class PoemViewSet(PermissionReadOnlyModelViewSet):
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

