
from rest_framework import  viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from karaoke.karaoke_serializer import KaraokeSerializer
from karaoke.models import Karaoke
from loginapp.auth import CsrfExemptSessionAuthentication


class GetKaraokeSerializer(viewsets.ReadOnlyModelViewSet):
    serializer_class = KaraokeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return Karaoke.objects.all()
