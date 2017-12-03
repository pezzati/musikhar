from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from musikhar.abstractions.views import IgnoreCsrfAPIView


class Verify(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()
