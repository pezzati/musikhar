from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView


# .media_type: multipart/form-data
class UploadMediaFile(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, type, format=None):
        if MediaFile.type_is_valid(type=type):
            try:
                my_file = request.FILES["file"]
                media_file = MediaFile.objects.create(user=request.user,
                                                      type=type)
                media_file.file = my_file
                media_file.save()
                return Response(status=status.HTTP_201_CREATED, data={'upload_id': media_file.id})
            except:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
