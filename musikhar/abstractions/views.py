from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView

from loginapp.auth import CsrfExemptSessionAuthentication


class IgnoreCsrfAPIView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
