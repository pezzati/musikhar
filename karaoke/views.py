
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from karaoke.serializers import KaraokeSerializer, GenreSerializer
from karaoke.models import Karaoke, Genre
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
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def check_object_permissions(self, request, obj):
        pass

    @list_route()
    def popular(self, request):
        response = [KaraokeSerializer(x).data for x in Karaoke.get_popular()]
        return Response(data=response)

    @list_route()
    def news(self, request):
        response = [KaraokeSerializer(x).data for x in Karaoke.get_new()]
        return Response(data=response)


class GenreViewSet(PermissionReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Genre.objects.filter(parent__isnull=True)

    @detail_route()
    def karaokes(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        karakoies = genre.karaoke_set.all()[:10]
        response = [KaraokeSerializer(x).data for x in karakoies]
        return Response(data=response)

